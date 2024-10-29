from dataclasses import dataclass
from typing import Literal, Sequence
import spacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc, Token
from ..patterns import to_patterns2
from ..utils import get_nlp
from .labels import LABELED_PHRASES

__all__ = ["Categorized", "Categorizer", "Role"]

IN, LOWER, POS = "IN", "LOWER", "POS"

type Role = Literal["Dev", "Nondev", "Org", "Student"]

@dataclass
class Categorized:
  role: Role | None
  is_freelancer: bool
  is_lead: bool
  is_remote: bool

class Categorizer:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    micronlp = spacy.load(name, exclude=["parser", "tagger", "lemmatizer", "ner"])
    self.nlp = get_nlp(name)

    self.matcher = Matcher(self.nlp.vocab)
    self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")

    for label, phrases in LABELED_PHRASES.items():
      for phrase in phrases:
        if isinstance(phrase, str):
          self.pmatcher.add(label, list(micronlp.pipe(
            to_patterns2(phrase)
          )))
        else:
          phrase, _pos = phrase
          poss: list[str] = []
          match _pos:
            case "NOUN": poss = ["NOUN", "PROPN", "ADJ"]
            case "VERB": poss = ["VERB"]
          self.matcher.add(label, [[{LOWER: phrase, POS: {IN: poss}}]])

  def ents(self, doc: Doc) -> list[tuple[str, Token]]:
    ents: list[tuple[str, Token] | None] = list(None for _ in doc)
    matches = self.matcher(doc)
    pmatches = self.pmatcher(doc)
    for match_id, start in matches + pmatches:
      if ents[start]:
        raise ValueError(f"multi-matcher binding to {start} offset")
      ents[start] = (doc.vocab.strings[match_id], doc[start])
    return [ent for ent in ents if ent]

  def categorize_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.categorize(doc) for doc in docs]

  def categorize(self, text_or_doc: str | Doc) -> Categorized:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    ents = self.ents(doc)

    role: Role | None = None
    is_freelancer = False
    is_lead = False
    is_remote = False

    for label, token in ents:
      r: Role | None
      if role is None and (r := check_dev(label, token, doc)):
        role = r
      elif role is None and (r := check_student(label, token, doc)):
        role = r
      elif role is None and (r := check_org(label, token, doc)):
        role = r
      elif not is_freelancer and check_freelancer(label, token, doc):
        is_freelancer = True
      elif not is_lead and check_lead(label, token, doc):
        is_lead = True
      elif not is_remote and check_remote(label, token, doc):
        is_remote = True

    return Categorized(
      role = role,
      is_freelancer = is_freelancer,
      is_lead = is_lead,
      is_remote = is_remote,
    )

def check_dev(label: str, token: Token, doc: Doc) -> Literal["Student", "Dev", "Nondev", None]:
  if label in {"DEV", "NONDEV"}:
    preceding = [token.lower_ for token in get_preceding(doc, token)]
    subtree = [
      tok.lower_ for tok in token.head.subtree
      if is_word(tok)
    ]
    master_words = [
      n for n in LABELED_PHRASES["STUDENT"] + LABELED_PHRASES["ORG"] # + LABELED_PHRASES["DEV"] + LABELED_PHRASES["NONDEV"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)
    sent = token.sent
    j = token._.i

    if any(True for word in subtree if word in FUTURE_MARKERS):
      return "Student"
    if any(True for tok in token.lefts if tok.lower_ in NEW_MARKERS):
      return "Student"
    if (
      token.head and token.head.lower_ in {"be", "become"} and
      token.head.head and token.head.head.lower_ in INTENT_MARKERS
    ):
      return "Student"
    if any(True for tok in token.sent if tok.lower_ in PAST_MARKERS):
      return None
    if (
      j > 0 and sent[j - 1].lower_ in EX_MARKERS or
      j > 1 and sent[j - 1].is_punct and sent[j - 2].lower_ in EX_MARKERS
    ):
      return None
    if len(cons_heads) and cons_heads[-1].lower_ in master_words:
      return None
    # Special rules for "Head" ---
    if label == "NONDEV" and token.lower_ == "head":
      if j < sent.end and sent[j + 1].lower_ in {"@", "at", "of"}:
        return "Nondev"
      if any(True for word in preceding if word in HEAD_MARKERS):
        return "Nondev"
      return None
    # ---
    return "Dev" if label == "DEV" else "Nondev"
  return None

def check_student(label: str, token: Token, doc: Doc) -> Literal["Student", None]:
  del doc
  if label == "STUDENT":
    subtree = [
      tok.lower_ for tok in token.head.subtree
      if is_word(tok)
    ]
    master_words = [
      n for n in LABELED_PHRASES["ORG"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)
    sent = token.sent
    j = token._.i

    if any(True for word in subtree if word in PAST_MARKERS | FUTURE_MARKERS | METAPHORIC_MARKERS):
      return None
    if (
      j > 0 and sent[j - 1].lower_ in EX_MARKERS or
      j > 1 and sent[j - 1].is_punct and sent[j - 2].lower_ in EX_MARKERS
    ):
      return None
    if len(cons_heads) and cons_heads[-1].lower_ in master_words:
      return None
    return "Student"
  return None

def check_org(label: str, token: Token, doc: Doc) -> Literal["Org", None]:
  del doc
  if label == "ORG":
    master_words = [
      n for n in LABELED_PHRASES["STUDENT"] + LABELED_PHRASES["DEV"] + LABELED_PHRASES["NONDEV"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)

    if len(cons_heads) and cons_heads[-1].lower_ in master_words:
      return None
    return "Org"
  return None

def check_freelancer(label: str, token: Token, doc: Doc) -> Literal["Freelancer", None]:
  del doc
  if label == "FREELANCER":
    subtree = [
      tok.lower_ for tok in token.head.subtree
      if is_word(tok)
    ]
    master_words = [
      n for n in LABELED_PHRASES["ORG"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)
    sent = token.sent
    j = token._.i

    if any(True for word in subtree if word in PAST_MARKERS | FUTURE_MARKERS):
      return None
    if (
      j > 0 and sent[j - 1].lower_ in EX_MARKERS or
      j > 1 and sent[j - 1].is_punct and sent[j - 2].lower_ in EX_MARKERS
    ):
      return None
    if len(cons_heads) and cons_heads[-1].lower_ in master_words:
      return None
    return "Freelancer"
  return None

def check_lead(label: str, token: Token, doc: Doc) -> bool:
  del doc
  if label == "LEAD":
    subtree = [
      tok.lower_ for tok in token.head.subtree
      if is_word(tok)
    ]
    master_words = [
      n for n in LABELED_PHRASES["STUDENT"] + LABELED_PHRASES["ORG"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)
    sent = token.sent
    j = token._.i

    if any(True for word in subtree if word in PAST_MARKERS | FUTURE_MARKERS):
      return False
    if (
      j > 0 and sent[j - 1].lower_ in EX_MARKERS or
      j > 1 and sent[j - 1].is_punct and sent[j - 2].lower_ in EX_MARKERS
    ):
      return False
    if len(cons_heads) and cons_heads[-1].lower_ in master_words:
      return False
    return True
  return False

def check_remote(label: str, token: Token, doc: Doc) -> bool:
  if label == "REMOTE":
    preceding = [token.lower_ for token in get_preceding(doc, token)]
    cons_heads = get_cons_heads(token)
    sent = token.sent
    j = token._.i

    if sent[j - 1] == "#":
      return True
    elif token.head.lower_ in REMOTE_JOB_MARKERS:
      return True
    elif preceding[-2:] == ["open", "to"]:
      return True
    elif len(cons_heads) and cons_heads[-1].lower_ in REMOTE_JOB_MARKERS:
      return True
    # elif token.pos_ == "PROPN":
    #   right_propns = get_right_propns(doc, token)
    #   for right_propn in right_propns:
    #     if right_propn.lower_ in REMOTE_JOB_MARKERS:
    #       is_remote = True
    #       break
  return False

PAST_MARKERS = {"ago", "former", "formerly", "past", "previous", "previously", "retired"}
EX_MARKERS = {"ex", "ex."}
NEW_MARKERS = {"new"}
FUTURE_MARKERS = {"aspiring", "future", "wanna", "wannabe"}
METAPHORIC_MARKERS = {
  "always", "constant", "eternal", "everlasting",
  "forever", "frantically", "life", "lifelong", "never",
  "permanent", "perpetual",
}
REMOTE_JOB_MARKERS = {
  "coder", "company", "consultant", "developer", "engineer",
  "freelancer", "job", "jobs", "mentor",
  "online", "opportunity", "opportunities", "programmer",
  "seeking", "remote", "remotely", "startup",
  "teacher", "team", "work", "worker", "working",
}
INTENT_MARKERS = {
  "going", "gonna", "strives", "striving",
  "want", "wanting", "wants", "wish", "wishing", "wishes",
}
HEAD_MARKERS = {
  "design", "devops", "ds", "engineering", "development",
  "growth", "research", "security", "sre", "swe",
  "technology", "training",
}

# def get_prev_word(doc: Doc, token: Token, hops: int=None) -> Token | None:
#   h = 0
#   i = token.i - 1
#   while i >= 0 and i >= token.sent.start and (hops and h < hops):
#     curr_token = doc[i]
#     if is_word(curr_token):
#       return curr_token
#     i -= 1
#     h += 1
#   return None

# def get_right_propns(doc: Doc, token: Token) -> list[Token]:
#   result: list[Token] = []
#   i = token.i + 1
#   while i < token.sent.end:
#     curr_token = doc[i]
#     if curr_token.pos_ == "PROPN":
#       result.append(curr_token)
#     else:
#       break
#     i += 1
#   return result

def get_preceding(doc: Doc, token: Token) -> list[Token]:
  return list(doc[token.sent.start : token.i])

def get_consequent(doc: Doc, token: Token) -> list[Token]:
  return list(doc[token.i+1 : token.sent.end])

# def next_word(doc: Doc, token: Token) -> Token | None:
#   j = token.i + 1
#   return doc[j].lower_ if doc[j] and is_word(doc[j]) else None

# def get_consequent_nouns(doc: Doc, token: Token) -> list[Token]:
#   res = []
#   for cons in get_consequent(doc, token):
#     if cons.pos_ in {"NOUN", "PROPN", "ADJ"}:
#       res.append(cons)
#     else:
#       break
#   return res

def get_heads(_token: Token) -> list[Token]:
  token = _token
  tokens: list[Token] = []
  while token != token.head:
    token = token.head
    tokens.append(token)
  return tokens

def get_cons_heads(_token: Token) -> list[Token]:
  token = _token
  tokens: list[Token] = []
  while token != token.head:
    token = token.head
    if token.i > _token.i:
      tokens.append(token)
  return tokens

def is_word(token: Token) -> bool:
  return not token.is_punct and not token.is_space
