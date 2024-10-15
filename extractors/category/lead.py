import re
from spacy.language import Language
# from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["LeadParser"]

LEAD_NOUNS = {
  "lead", "leader", "tl",
}
LEAD_VERBS = {
  "leading",
}
#
# NONDEV_NOUNS = {
#   ???
# }

class LeadParser:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp

  def are_leads(self, ntexts: Iterable[str | Doc]) -> list[bool | None]:
    docs = self.nlp.pipe(ntexts)
    return [
      self.is_lead(doc) for doc in docs
    ]

  def is_lead(self, ntext: str | Doc) -> bool | None:
    if not ntext:
      return None
    doc = ntext if type(ntext) is Doc else self.nlp(ntext)
    # print([
    #   (token, token.tag_, token.pos_, token.dep_) for token in doc if not token.is_punct
    # ])
    for token in doc:
      if is_lead_noun(token, doc):
        return True
      elif is_lead_verb(token):
        return True
    return None

def is_lead_noun(token: Token, doc: Doc) -> bool:
  if (
    token.lower_.strip("-") in LEAD_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  ):
    tail = str(doc[token.i:token.i+3])
    return not re.match(r"tl[-_/;, ]{0,2}dr", tail, re.IGNORECASE)
  return False

def is_lead_verb(token: Token) -> bool:
  return (
    token.lower_.strip("-") in LEAD_VERBS and
    token.pos_ in {"VERB"}
  )
