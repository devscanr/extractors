from dataclasses import dataclass
import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Token
from typing import Any, cast, Literal, Sequence
from ..patterns import to_patterns2
from ..utils import get_cons_heads, get_cons_words, get_nlp, get_prec_words, get_root, is_word
from .data import LABELED_PHRASES

__all__ = ["Categorized", "CategoryExtractor", "Role"]

IN, LOWER, ORTH, POS = "IN", "LOWER", "ORTH", "POS"

type Role = Literal["Dev", "Nondev", "Org", "Student"]

@dataclass
class Categorized:
  role: Role | None
  is_freelancer: bool | None
  is_lead: bool | None
  is_remote: bool | None
  is_hireable: bool | None

class CategoryExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.nlp = get_nlp(name)
    ruler: EntityRuler = cast(Any, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name="entity_ruler"))
    # self.nlp.add_pipe("merge_entities") # UPDATE entity merging is bug prone (can't check for exact words anymore) TODO so why I continue to work like ENT tokens are not merged?! @_@
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
    # print("Debug tokens:", list(self.nlp.tokenizer.explain(text_or_doc)))
    # print("Debug poss:", list((token, token.pos_) for token in doc if not token.is_punct))
    # print("Debug deps:")
    # pprint(list({"token": token, "pos": token.pos_, "dep": token.dep_, "head": token.head} for token in doc if not token.is_punct))
    # print("Debug ents:", list(ent.label_ for ent in doc.ents))
    role: Role | None = None
    is_freelancer, is_lead, is_remote, is_hireable = None, None, None, None
    for ent in doc.ents:
      token = doc[ent.start:ent.end].root
      r: Role | None
      if role is None and (r := check_dev(ent.label_, token)):
        role = r
      elif role is None and (r := check_student(ent.label_, token)):
        role = r
      elif role is None and (r := check_org(ent.label_, token)):
        role = r
      if is_freelancer is None:
        is_freelancer = check_freelancer(ent.label_, token)
      if is_lead is None:
        is_lead = check_lead(ent.label_, token)
      if is_remote is None:
        is_remote = check_remote(ent.label_, token)
      if is_hireable is None:
        is_hireable = check_hireable(ent.label_, token)
    return Categorized(
      role = role,
      is_freelancer = is_freelancer,
      is_lead = is_lead,
      is_remote = is_remote,
      is_hireable = is_hireable,
    )

def check_dev(label: str, token: Token) -> Literal["Student", "Dev", "Nondev", None]:
  if label in {"DEV", "NONDEV"}:
    prec_words = get_prec_words(token)
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
    j = cast(int, token._.i)
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
    j = cast(int, token._.i)
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

def is_hashtagged(token: Token) -> bool:
  j = cast(int, token._.i)
  return j > 0 and token.sent[j - 1].lower_ == "#"

def is_negated(token: Token) -> bool:
  j = cast(int, token._.i)
  if j > 0:
    if token.sent[j - 1].lower_ in EX_MARKERS:
      return True
  if j > 1:
    if token.sent[j - 2].lower_ in EX_MARKERS and token.sent[j - 1].is_punct:
      return True
  root_token = token if token.dep_ == "ROOT" else get_root(token.sent)
  # pprint(list({"token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in token.sent if not token.is_punct))
  for tok in token.sent:
    if tok.dep_ == "neg" or tok.lower_ == "non":
      if tok.head == root_token or tok.head == token:
        return True
      if (tok.head.head == root_token or tok.head.head == token) and tok.head.dep_ == "compound":
        return True
  return False

def check_freelancer(label: str, token: Token) -> bool | None:
  if label == "FREELANCER":
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    for tok in token.head.subtree:
      if tok.lower_ in (PAST_MARKERS | FUTURE_MARKERS):
        return False
    MASTER_WORDS = [
      n for n in LABELED_PHRASES["STUDENT"] + LABELED_PHRASES["ORG"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)
    if cons_heads and cons_heads[-1].lower_ in MASTER_WORDS:
      return None
    return True
  return None

def check_lead(label: str, token: Token) -> bool | None:
  if label == "LEAD":
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    for tok in token.head.subtree:
      if tok.lower_ in (PAST_MARKERS | FUTURE_MARKERS):
        return False
    MASTER_WORDS = [
      n for n in LABELED_PHRASES["STUDENT"] + LABELED_PHRASES["ORG"]
      if isinstance(n, str)
    ]
    cons_heads = get_cons_heads(token)
    if cons_heads and cons_heads[-1].lower_ in MASTER_WORDS:
      return None
    return True
  return None

def check_remote(label: str, token: Token) -> bool | None:
  if label == "REMOTE":
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    cons_heads = get_cons_heads(token)
    if any(True for tok in cons_heads if tok.lower_ in REMOTE_JOB_MARKERS):
      return True
    cons_words = get_cons_words(token)
    if not cons_words or cons_words[0] in {"friendly", "only", "online"}:
      return True
    return None
  elif label == "OPEN-TO":
    if not any(True for word in get_cons_words(token) if word in LABELED_PHRASES["REMOTE"]):
      return None
    if is_negated(token):
      return False
    return True
  return None

def check_hireable(label: str, token: Token) -> bool | None:
  if label == "HIREABLE":
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    return True
  elif label == "OPEN-TO":
    if not any(True for word in get_cons_words(token) if word in PROPOSAL_MARKERS):
      return None
    if is_negated(token):
      return False
    return True
  return None

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
  "coder",
  "company",
  "consultant", "consultancy", "consulting",
  "collaboration", "collaborations",
  "developer", "engineer",
  "enthusiast", "freelancer",
  "job", "jobs", "jobseeker",
  "mentor", "mentoring", "mentorship",
  "online",
  "opportunity", "opportunities",
  "position", "positions",
  "programmer",
  "project", "projects",
  "remote", "remotely",
  "role", "roles",
  "seeking", "seeker",
  "startup",
  "teacher",
  "team",
  "work", "worker", "working",
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
PROPOSAL_MARKERS = {
  "challenge", "challenges",
  "collaboration", "collaborations",
  "consulting", "consultancy",
  "enquiry", "enquiries",
  "hire", "hiring", "hired",
  "idea", "ideas",
  "internship", "internships",
  "job", "jobs",
  "offer", "offers",
  "opportunity", "opportunities",
  "option", "options",
  "position", "positions",
  "possibility", "possibilities",
  "project", "projects",
  "proposal", "proposals",
  "relocation",
  "role", "roles",
  "work",
}
