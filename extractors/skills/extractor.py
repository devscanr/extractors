from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span
from typing import Sequence, cast
from ..patterns import to_patterns2
from ..utils import get_nlp, uniq
from .data import SKILLS

IN, LOWER, POS = "IN", "LOWER", "POS"

class SkillExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.nlp = get_nlp(name)

    ruler = cast(EntityRuler, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }))

    for skill in SKILLS:
      for item in skill.phrases:
        if isinstance(item, str):
          ruler.add_patterns([{
            "label": skill.name,
            "pattern": pattern,
          } for pattern in to_patterns2(item)])
        elif isinstance(item, tuple):
          phrase, pos = item
          poss: list[str] = []
          match pos:
            case "NOUN": poss = ["NOUN", "PROPN", "ADJ"]
            case "PROPN": poss = ["PROPN"]
            case "VERB": poss = ["VERB"]
          ruler.add_patterns([{
            "label": skill.name,
            "pattern": [{LOWER: phrase, POS: {IN: poss}}]
          }])
        elif isinstance(item, list):
          ruler.add_patterns([{
            "label": skill.name,
            "pattern": item
          }])

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[list[str]]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # for token in doc:
      # if not token.is_punct:
      # print(token, token.pos_, token.dep_)
    skills = [
      skill for ent in doc.ents
      if (skill := ensure_skill(ent))
    ]
    return uniq(skills)

def ensure_skill(ent: Span) -> str | None:
  # n = len(ent.doc)
  # if ent.label_.endswith(":maybe"):
  #   print(ent, (ent.start, ent.end))
  #   print(ent[0].pos_)
  #   print(ent[0].dep_)
  #   print()
  #   # if ent.start > 0:
  #   #   print("prev token:", ent.doc[ent.start - 1])
  #   # if ent.end + 1 < n:
  #   #   print("next token:", ent.doc[ent.end + 1])
  #   return None
  # else:
  return ent.label_
