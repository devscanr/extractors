from spacy.language import Language
# from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["NondevParser"]

NONDEV_NOUNS = {
  "cofounder", "ceo", "cto", "dean", "entrepreneur",
  "founder", "manager", "professor", "recruiter", "svp", "vp",
}

DEV_NOUNS = {
  "admin", "analyst", "architect", "dev", "developer", "devops",
  "eng", "engineer", "hacker", "investigator", "mathematician", "mlops", "programmer",
  "researcher", "secops", "scientist",
}

class NondevParser:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp

  def are_nondevs(self, ntexts: Iterable[str | Doc]) -> list[bool | None]:
    docs = self.nlp.pipe(ntexts)
    return [
      self.is_nondev(doc) for doc in docs
    ]

  def is_nondev(self, ntext: str | Doc) -> bool | None:
    doc = ntext if type(ntext) is Doc else self.nlp(ntext)
    # print([
    #   (token, token.pos_, token.dep_) for token in doc if not token.is_punct
    # ])
    for token in doc:
      if is_nondev_noun(token):
        return True
      elif is_dev_noun(token):
        return False
    return None

def is_nondev_noun(token: Token) -> bool:
  return (
    token.lower_.strip("-") in NONDEV_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  )

def is_dev_noun(token: Token) -> bool:
  return (
    token.lower_.strip("-") in DEV_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  )
