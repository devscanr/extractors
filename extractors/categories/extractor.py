from spacy.tokens import Doc, Token
from typing import cast, Literal, Sequence
from ..extractor import BaseExtractor, TMatch, detach_maybe
from ..markers import is_future, is_hashtagged, is_negated, is_past
from ..spacyhelpers import ancestors, left_lowerwords
from .categorized import Categorized, Role
from .data import CANCELING_TAGS
from ..utils import includes

class CategoryExtractor(BaseExtractor):
  exclusive_tags = False

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> Categorized:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{
    #   "token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head}
    #   for tok in doc if not tok.is_punct
    # ])

    tmatches, _ = self.find_tmatches(doc)
    tmatches = self.filter_main(tmatches)

    # Filter tag-token pairs
    tmatches2: list[TMatch] = []
    for mname, [token] in tmatches:
      name = detach_maybe(mname)
      ancs = set(
        tok for tok in ancestors(token)
        if (
          tok.pos_ in {"NOUN", "PROPN"} and not any(pred(tok) for pred in [is_negated, is_past, is_future])
          or
          tok.pos_ in {"ADJ", "VERB"}
        )
      )
      if not any(
        True for nam, [tok] in tmatches
        if tok in ancs and (
          name not in CANCELING_TAGS or
          nam in CANCELING_TAGS[name]
        ) and not is_distant(token, tok)
      ):
        tmatches2.append((name, [token]))
    # print("tmatches2:", tmatches2)

    # Extract roles
    role: Role | None = None
    is_freelancer, is_lead, is_remote, is_hireable = None, None, None, None
    for name, [token] in tmatches2:
      if role is None:
        if name == "Dev" or name.startswith("Dev:"):
          role = self.check_dev(token)
        elif name == "Nondev" or name.startswith("Nondev:"):
          role = self.check_nondev(token)
        elif name == "Student":
          role = self.check_student(token)
        elif name == "Org":
          role = self.check_organization(token)
      if is_freelancer is None:
        if name == "Freelancer":
          is_freelancer = self.check_freelancer(token)
      if is_lead is None:
        if name == "Lead":
          is_lead = self.check_lead(token)
      if is_remote is None:
        if name == "Remote":
          is_remote = self.check_remote(token)
      if is_hireable is None:
        if name == "Hireable":
          is_hireable = self.check_hireable(token)
    return Categorized(
      role = role,
      is_freelancer = is_freelancer,
      is_lead = is_lead,
      is_remote = is_remote,
      is_hireable = is_hireable,
    )

  def check_dev(self, token: Token) -> Literal["Student", "Dev", None]:
    if is_hashtagged(token):
      return "Dev"
    elif is_negated(token):
      return None
    elif is_past(token):
      return None
    elif is_future(token):
      return "Student"
    return "Dev"

  def check_nondev(self, token: Token) -> Literal["Student", "Nondev", None]:
    if is_hashtagged(token):
      return "Nondev"
    elif is_negated(token):
      return None
    elif is_past(token):
      return None
    elif is_future(token):
      return "Student"
    if token.lower_ == "head":
      sent = token.sent
      j = cast(int, token._.i)
      if j < sent.end and sent[j + 1].lower_ in {"@", "at", "of"}:
        return "Nondev"
      lwords = left_lowerwords(token)
      if any(True for word in lwords if word in HEAD_MARKERS):
        return "Nondev"
      return None
    return "Nondev"

  def check_student(self, token: Token) -> Literal["Student", None]:
    if is_hashtagged(token):
      return "Student"
    elif is_negated(token):
      return None
    elif is_past(token):
      return None
    elif is_future(token):
      return None
    return "Student"

  def check_organization(self, token: Token) -> Literal["Org", None]:
    root = token.sent.root
    if root == token or root.lemma_ in {"be"}:
      return "Org"
    return None

  def check_freelancer(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    elif is_past(token):
      return False
    elif is_future(token):
      return False
    return True

  def check_lead(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    elif is_past(token):
      return False
    elif is_future(token):
      return False
    return True

  def check_remote(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    lowers = [tok.lower_ for tok in token.sent]
    for combination in [("tool", "for"), ("working", "on")]:
      if includes(lowers, combination):
        return None
    return True

  def check_hireable(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    return True

# REMOTE_JOB_MARKERS = {
#   "coder",
#   "company",
#   "consultant", "consultancy", "consulting",
#   "collaboration", "collaborations",
#   "developer", "engineer",
#   "enthusiast", "freelancer",
#   "job", "jobs", "jobseeker",
#   "mentor", "mentoring", "mentorship",
#   "online",
#   "opportunity", "opportunities",
#   "position", "positions",
#   "programmer",
#   "project", "projects",
#   "remote", "remotely",
#   "role", "roles",
#   "seeking", "seeker",
#   "startup",
#   "teacher",
#   "team",
#   "work", "worker", "working",
# }
HEAD_MARKERS = {
  "design", "devops", "ds", "engineering", "development",
  "growth", "research", "security", "sre", "swe",
  "technology", "training",
}
# PROPOSAL_MARKERS = {
#   "challenge", "challenges",
#   "collaboration", "collaborations",
#   "consulting", "consultancy",
#   "enquiry", "enquiries",
#   "hire", "hiring", "hired",
#   "idea", "ideas",
#   "internship", "internships",
#   "job", "jobs",
#   "offer", "offers",
#   "opportunity", "opportunities",
#   "option", "options",
#   "position", "positions",
#   "possibility", "possibilities",
#   "project", "projects",
#   "proposal", "proposals",
#   "relocation",
#   "role", "roles",
#   "work",
# }

def is_distant(token1: Token, token2: Token) -> bool:
  mini = min(token1.i, token2.i)
  maxi = max(token1.i, token2.i)
  distance: int = 0
  for tok in token1.doc[mini+1:maxi]:
    if tok.text in {";", "|"}:
      distance += 3
    elif tok.text in {"-", ",", "("}:
      distance += 2
    else:
      distance += 1
  return distance >= 6
