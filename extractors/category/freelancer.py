from spacy.language import Language
# from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["FreelancerParser"]

FREELANCER_NOUNS = {"consulting", "consultant", "freelancer", "freelance", "freelancing"}
FREELANCER_VERBS = {"consulting", "freelancing"}

NON_FREELANCER_NOUNS = {
  "cofounder", "cto", "founder",
  "lead", "leader", "svp", "vp",
}

class FreelancerParser:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp

  def are_freelancers(self, ntexts: Iterable[str | Doc]) -> list[bool | None]:
    docs = self.nlp.pipe(ntexts)
    return [
      self.is_freelancer(doc) for doc in docs
    ]

  def is_freelancer(self, ntext: str | Doc) -> bool | None:
    if not ntext:
      return None
    doc = ntext if type(ntext) is Doc else self.nlp(ntext)
     # print([
    #   (token, token.pos_, token.dep_) for token in doc if not token.is_punct
    # ])
    for token in doc:
      if is_freelancer_noun(token):
        return True
      elif is_freelancer_verb(token):
        return True
      elif is_non_freelancer_noun(token):
        return False
    return None

def is_freelancer_noun(token: Token) -> bool:
  return (
    token.lower_.strip("-") in FREELANCER_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  )

def is_freelancer_verb(token: Token) -> bool:
  return (
    token.lower_.strip("-") in FREELANCER_VERBS and
    (token.pos_ in {"VERB"} or not token.i)
  )

def is_non_freelancer_noun(token: Token) -> bool:
  return (
    token.lower_.strip("-") in NON_FREELANCER_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  )
