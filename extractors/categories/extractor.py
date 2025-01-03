from dataclasses import dataclass
import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Token
from typing import Any, cast, Literal, Sequence
from ..markers import is_future, is_hashtagged, is_metaphorical, is_negated, is_past
from ..patterns import to_patterns2
from ..utils import Pattern, get_cons_heads, get_cons_words, get_nlp, get_prec_words
from .data import DEV_CANCELING_ROLES, FREELANCER_CANCELING_ROLES, LABELED_PHRASES, LEAD_CANCELING_ROLES, ORG_CANCELING_ROLES, STUDENT_CANCELING_ROLES

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
    for label, phrases in LABELED_PHRASES.items():
      for phrase in phrases:
        if isinstance(phrase, str):
          assert not re.search("[A-Z]", phrase), f"{phrase!r} contains uppercase character(s), use pattern syntax"
          ruler.add_patterns(from_phrase(label, phrase))
        elif isinstance(phrase, list):
          ruler.add_patterns(from_pattern(label, phrase))
    # self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
    # self.pmatcher.add("FUTURE", [self.nlp(m) for m in FUTURE_MARKERS | INTENT_MARKERS])
    # self.pmatcher.add("PAST", [self.nlp(m) for m in PAST_MARKERS])
    # self.pmatcher.add("METAPHORIC", [self.nlp(m) for m in METAPHORIC_MARKERS])

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> Categorized:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # print("Debug tokenization:", list(self.nlp.tokenizer.explain(text_or_doc)))
    # print("Debug poss:", list((token, token.pos_) for token in doc if not token.is_punct))
    # print("Debug tokens:")
    # pprint([{"token": token, "pos": token.pos_, "dep": token.dep_, "head": token.head} for token in doc if not token.is_punct])
    # print("Debug ents:", list(ent.label_ for ent in doc.ents))
    role: Role | None = None
    is_freelancer, is_lead, is_remote, is_hireable = None, None, None, None
    for ent in doc.ents:
      token = doc[ent.start:ent.end].root
      r: Role | None
      if role is None and (r := self.check_dev(ent.label_, token)):
        role = r
      elif role is None and (r := self.check_student(ent.label_, token)):
        role = r
      elif role is None and (r := self.check_org(ent.label_, token)):
        role = r
      if is_freelancer is None:
        is_freelancer = self.check_freelancer(ent.label_, token)
      if is_lead is None:
        is_lead = self.check_lead(ent.label_, token)
      if is_remote is None:
        is_remote = self.check_remote(ent.label_, token)
      if is_hireable is None:
        is_hireable = self.check_hireable(ent.label_, token)
    return Categorized(
      role = role,
      is_freelancer = is_freelancer,
      is_lead = is_lead,
      is_remote = is_remote,
      is_hireable = is_hireable,
    )

  # def pmatch(self, doc_or_span: Doc | Span) -> set[str]:
  #   matches = self.pmatcher(doc_or_span)
  #   matched: set[str] = set()
  #   for match_id, _start, _end in matches:
  #     matched.add(self.nlp.vocab.strings[match_id])
  #   return matched

  def check_dev(self, label: str, token: Token) -> Literal["Student", "Dev", "Nondev", None]:
    # print("@ check_dev", repr(str(token)))
    if label in {"DEV", "NONDEV"}:
      if is_hashtagged(token):
        # print("is_hashtagged")
        return "Dev"
      elif is_negated(token):
        # print("is_negated")
        return None
      elif is_past(token):
        # print("is_past")
        return None
      elif is_future(token):
        # print("is_future")
        return "Student"
      # matches = self.pmatch(token.sent)
      # if "FUTURE" in matches:
      #   return "Student"
      # if "PAST" in matches:
      #   return None
      cons_heads = get_cons_heads(token)
      if len(cons_heads) and cons_heads[-1].lower_ in DEV_CANCELING_ROLES:
        return None
      # Special rules for "Head" ---
      prec_words = get_prec_words(token)
      sent = token.sent
      j = cast(int, token._.i)
      if label == "NONDEV" and token.lower_ == "head":
        if j < sent.end and sent[j + 1].lower_ in {"@", "at", "of"}:
          return "Nondev"
        if any(True for word in prec_words if word in HEAD_MARKERS):
          return "Nondev"
        return None
      # ---
      return "Dev" if label == "DEV" else "Nondev"
    return None

  def check_student(self, label: str, token: Token) -> Literal["Student", None]:
    if label == "STUDENT":
      if is_hashtagged(token):
        return "Student"
      elif is_negated(token):
        return None
      elif is_past(token):
        return None
      elif is_future(token):
        return None
      elif is_metaphorical(token):
        return None
      cons_heads = get_cons_heads(token)
      if len(cons_heads) and cons_heads[-1].lower_ in STUDENT_CANCELING_ROLES:
        return None
      return "Student"
    return None

  def check_org(self, label: str, token: Token) -> Literal["Org", None]:
    if label == "ORG":
      root = token.sent.root
      cons_heads = get_cons_heads(token)
      if len(cons_heads) and cons_heads[-1].lower_ in ORG_CANCELING_ROLES:
        return None
      if root and (root == token or root.lower_ in {"is"}):
        return "Org"
    return None

  def check_freelancer(self, label: str, token: Token) -> bool | None:
    if label == "FREELANCER":
      if is_hashtagged(token):
        return True
      elif is_negated(token):
        return False
      elif is_past(token):
        # print("token:", token, "is_past")
        return False
      elif is_future(token):
        return False
      # matches = self.pmatch(token.sent)
      # if {"PAST", "FUTURE"} & matches:
      #   return False
      cons_heads = get_cons_heads(token)
      if cons_heads and cons_heads[-1].lower_ in FREELANCER_CANCELING_ROLES:
        return None
      return True
    return None

  def check_lead(self, label: str, token: Token) -> bool | None:
    if label == "LEAD":
      if is_hashtagged(token):
        return True
      elif is_negated(token):
        return False
      elif is_past(token):
        return False
      elif is_future(token):
        return False
      # matches = self.pmatch(token.sent)
      # if {"PAST", "FUTURE"} & matches:
      #   return False
      cons_heads = get_cons_heads(token)
      if cons_heads and cons_heads[-1].lower_ in LEAD_CANCELING_ROLES:
        return None
      return True
    return None

  def check_remote(self, label: str, token: Token) -> bool | None:
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

  def check_hireable(self, label: str, token: Token) -> bool | None:
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

def from_pattern(label: str, pattern: Pattern) -> Pattern:
  return [{
    "label": label,
    "pattern": pattern
  }]

def from_phrase(label: str, phrase: str) -> Pattern:
  return [{
    "label": label,
    "pattern": pattern,
  } for pattern in to_patterns2(phrase)]
