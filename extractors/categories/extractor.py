from dataclasses import dataclass
from pprint import pprint
import re
from spacy import Language
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc, Token
from typing import cast, Literal, Sequence
from ..markers import is_future, is_hashtagged, is_metaphorical, is_negated, is_past
from ..patterns import expand_phrase12
from ..spacyhelpers import ancestors, left_lowerwords, right_ancestors, right_lowerwords, token_level
from ..utils import Pattern, literal
from .data import CANCELING_TAGS, TAGGED_PHRASES

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
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp
    self.matcher = Matcher(self.nlp.vocab)                      # matcher: single word, more verbose syntax than PM but less verbose than DM
    self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER") # phrases: fastest, no flexibility
    self.init_matchers(TAGGED_PHRASES)

  def init_matchers(self, tagged_phrases: dict[str, list[str | Pattern]]) -> None:
    for tag, phrases in tagged_phrases.items():
      # Update matchers with patterns
      for phrase in phrases:
        if isinstance(phrase, str):
          if "<<" in phrase:
            raise Exception("not supported")
          else:
            if re.search("[A-Z]", phrase):
              self.matcher.add(tag, [literal(p) for p in expand_phrase12(phrase)])
            else:
              self.pmatcher.add(tag, [self.nlp(p) for p in expand_phrase12(phrase)])
        elif isinstance(phrase, list):
          self.matcher.add(tag, [phrase])

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> Categorized:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # print("Debug tokenization:", list(self.nlp.tokenizer.explain(text_or_doc)))
    # print("Debug tokens:")
    # pprint([{"token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc if not tok.is_punct])
    # print("Debug ents:", [ent.label_ for ent in doc.ents])

    raw_matches: list[tuple[str, list[int]]] = []
    matches = self.matcher(doc) if len(self.matcher) else []
    pmatches = self.pmatcher(doc) if len(self.pmatcher) else []
    for match in matches:
      # print("match:", match)
      [match_id, start, end] = match # e.g. "hardware" -> (10100372000430808166, 3, 4)
      tag = self.nlp.vocab.strings[match_id]
      raw_matches.append((tag, list(range(start, end))))
    for pmatch in pmatches:
      # print("pmatch:", pmatch)
      [match_id, start, end] = pmatch # e.g. "hardware-designer" -> (10100372000430808166, 3, 6)
      tag = self.nlp.vocab.strings[match_id]
      raw_matches.append((tag, list(range(start, end))))
    # print("raw_matches:", raw_matches)

    # Resolve overriding matches
    distinct_matches: list[tuple[str, list[int]]] = []
    for tag, offsets in raw_matches:
      other_matches: list[tuple[str, list[int]]] = []
      for tg, ofs in raw_matches:
        if ofs == offsets and tg != tag:
          raise Exception(f"anchors {tag!r} and {tg!r} overlap at {offsets!r}")
        else:
          other_matches.append((tg, ofs))
      if not any(
        True for other_match in other_matches
        # Wider alternative exists
        if set(offsets) < set(other_match[1])
      ):
        distinct_matches.append((tag, offsets))
    # print("distinct_matches:", distinct_matches)

    # Convert to sorted tag-token pairs
    tag_tokens = [
      (tag, token)
      for tag, offsets in distinct_matches
      if (token := doc[min(offsets, key=lambda o: token_level(doc[o]))])
    ]
    tag_tokens.sort(key=lambda tag_token: tag_token[1].i)
    # print("tag_tokens:", tag_tokens)

    # Filter tag-token pairs
    tag_tokens2: list[tuple[str, Token]] = []
    for tag, token in tag_tokens:
      positive_nancs = set(
        tok for tok in ancestors(token)
        if tok.pos_ in {"NOUN", "PROPN", "ADJ"} and
           not any(pred(tok) for pred in [is_negated, is_past, is_future, is_metaphorical])
      )
      if not any(
        True for tg, tok in tag_tokens
        if tok in positive_nancs and tg in CANCELING_TAGS[tag] and not is_distant(token, tok)
      ):
        tag_tokens2.append((tag, token))
    # print("tag_tokens2:", tag_tokens2)

    # Extract roles
    role: Role | None = None
    is_freelancer, is_lead, is_remote, is_hireable = None, None, None, None
    for tag, token in tag_tokens2:
      if role is None:
        if tag == "DEV":
          role = self.check_dev(token)
        elif tag == "NONDEV":
          role = self.check_nondev(token)
        elif tag == "STUDENT":
          role = self.check_student(token)
        elif tag == "ORG":
          role = self.check_org(token)
      if is_freelancer is None:
        if tag == "FREELANCER":
          is_freelancer = self.check_freelancer(token)
      if is_lead is None:
        if tag == "LEAD":
          is_lead = self.check_lead(token)
      if is_remote is None:
        if tag == "REMOTE":
          is_remote = self.check_remote(token)
        elif tag == "OPEN-TO":
          is_remote = self.check_opento_remote(token)
      if is_hireable is None:
        if tag == "HIREABLE":
          is_hireable = self.check_hireable(token)
        elif tag == "OPEN-TO":
          is_hireable = self.check_opento_hireable(token)

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
    elif is_metaphorical(token):
      return None
    return "Student"

  def check_org(self, token: Token) -> Literal["Org", None]:
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
    rancs = right_ancestors(token)
    if any(True for tok in rancs if tok.lower_ in REMOTE_JOB_MARKERS):
      return True
    rwords = right_lowerwords(token)
    if not rwords or rwords[0] in {"friendly", "only", "online"}:
      return True
    return None

  def check_opento_remote(self, token: Token) -> bool | None:
    if not any(True for word in right_lowerwords(token) if word in TAGGED_PHRASES["REMOTE"]):
      return None
    if is_negated(token):
      return False
    return True

  def check_hireable(self, token: Token) -> bool | None:
    if is_hashtagged(token):
      return True
    elif is_negated(token):
      return False
    return True

  def check_opento_hireable(self, token: Token) -> bool | None:
    if not any(True for word in right_lowerwords(token) if word in PROPOSAL_MARKERS):
      return None
    if is_negated(token):
      return False
    return True

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
