# import spacy
from spacy.language import Language
# from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["NondevParser"]

# nlp = spacy.load("en_core_web_lg", exclude=["ner"])
# matcher = PhraseMatcher(nlp.vocab)

NONDEV_NOUNS = {
  "artist", "dean", "founder", "manager", "mechanic", "musician", "cto", "technician", "vp",
  "physicist", # hr, recruiter
}

# --------------------------------------------------------------------------------------------------
# Currently follows the "Freelancer" scheme. Can be update to follow the "Student" scheme instead,
# where the preceding nouns have priotity over subsequent.
# --------------------------------------------------------------------------------------------------

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
    for token in doc:
      # if not token.is_space and not token.is_punct:
      # print(token, token.pos_, token.dep_, token.head.lemma_)
      if is_nondev_noun(token):
        return True
    return None

def is_nondev_noun(token: Token) -> bool:
  return (
    token.lower_ in NONDEV_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"} and # spacy default models have PROPN false positives and ADJ mistakes
    token.dep_ in {
      "ROOT",     # Manager
      "conj",     # Manager and student
      "attr",     # I am a manager
      "appos",    # Manager, student
      "compound", # Manager Nasim (Spacy mistakenly thinks the first word is PROPN)
      "nmod",     #
    }
  )
