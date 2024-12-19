from dataclasses import dataclass
import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Token
from typing import Any, cast, Literal, Sequence
from ..patterns import to_patterns2
from ..utils import get_cons_heads, get_nlp, get_prec_words, get_root, is_word
from .data import LABELED_PHRASES

__all__ = ["Categorized", "CategoryExtractor", "Role"]

IN, LOWER, ORTH, POS = "IN", "LOWER", "ORTH", "POS"

type Role = Literal["Dev", "Nondev", "Org", "Student"]

@dataclass
class Categorized:
  role: Role | None
  is_freelancer: bool
  is_lead: bool
  is_remote: bool

class CategoryExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.nlp = get_nlp(name)
    ruler: EntityRuler = cast(Any, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name="entity_ruler"))
    self.nlp.add_pipe("merge_entities") # TODO so why I continue to work like ENT tokens are not merged?! @_@
    self.nlp.add_pipe("index_tokens_by_sents")
    for label, phrases in LABELED_PHRASES.items():
      for item in phrases:
        # TODO refactor like in skills
        if isinstance(item, str):
          ruler.add_patterns([{
            "label": label,
            "pattern": pattern,
          } for pattern in to_patterns2(item)])
        elif isinstance(item, tuple):
          phrase, pos = item
          poss: list[str] = []
          match pos:
            case "NOUN": poss = ["NOUN", "PROPN", "ADJ"]
            case "VERB": poss = ["VERB"]
          ruler.add_patterns([{
            "label": label,
            "pattern": (
              [{ORTH: phrase, POS: {IN: poss}}]
              if re.search(r"[A-Z]", phrase)
              else [{LOWER: phrase, POS: {IN: poss}}]
            )
          }])

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> Categorized:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    role: Role | None = None
    is_freelancer = False
    is_lead = False
    is_remote = False
    for ent in doc.ents:
      token = doc[ent.start] # entity spans are merged by this point
      r: Role | None
      if role is None and (r := check_dev(ent.label_, token)):
        role = r
      elif role is None and (r := check_student(ent.label_, token)):
        role = r
      elif role is None and (r := check_org(ent.label_, token)):
        role = r
      elif not is_freelancer and check_freelancer(ent.label_, token):
        is_freelancer = True
      elif not is_lead and check_lead(ent.label_, token):
        is_lead = True
      elif not is_remote and check_remote(ent.label_, token):
        is_remote = True
    return Categorized(
      role = role,
      is_freelancer = is_freelancer,
      is_lead = is_lead,
      is_remote = is_remote,
    )

def check_dev(label: str, token: Token) -> Literal["Student", "Dev", "Nondev", None]:
  if label in {"DEV", "NONDEV"}:
    prec_words = [token.lower_ for token in get_prec_words(token)]
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
      if any(True for word in prec_words if word in HEAD_MARKERS):
        return "Nondev"
      return None
    # ---
    return "Dev" if label == "DEV" else "Nondev"
  return None

def check_student(label: str, token: Token) -> Literal["Student", None]:
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

def check_org(label: str, token: Token) -> Literal["Org", None]:
  if label == "ORG":
    root = get_root(token.sent)
    master_words = [
      n for n in ["contributor"] + LABELED_PHRASES["STUDENT"] + LABELED_PHRASES["DEV"] + LABELED_PHRASES["NONDEV"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)
    if len(cons_heads) and cons_heads[-1].lower_ in master_words:
      return None
    if root and (root == token or root.lower_ in {"is"}):
      return "Org"
  return None

def check_freelancer(label: str, token: Token) -> Literal["Freelancer", None]:
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

def check_lead(label: str, token: Token) -> bool:
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

def check_remote(label: str, token: Token) -> bool:
  if label == "REMOTE":
    prec_words = [token.lower_ for token in get_prec_words(token)]
    cons_heads = get_cons_heads(token)
    sent = token.sent
    j = token._.i
    if sent[j - 1] == "#":
      return True
    elif token.head.lower_ in REMOTE_JOB_MARKERS:
      return True
    elif prec_words[-2:] == ["open", "to"]:
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
FUTURE_MARKERS = {"aspiring", "future", "upcoming", "wanna", "wannabe"}
METAPHORIC_MARKERS = {
  "always", "constant", "eternal", "everlasting",
  "forever", "frantically", "life", "lifelong", "never",
  "permanent", "perpetual",
}
REMOTE_JOB_MARKERS = {
  "coder", "company", "consultant", "developer", "engineer",
  "enthusiast", "freelancer", "job", "jobs", "mentor",
  "online", "opportunity", "opportunities",
  "position", "positions", "programmer", "project", "projects",
  "remote", "remotely", "role", "roles", "seeking", "startup",
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
