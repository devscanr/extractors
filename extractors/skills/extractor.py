from typing import cast

import spacy
from spacy.pipeline import EntityRuler
from spacy.util import filter_spans
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc, Token
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

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    for token in doc:
      if not token.is_punct:
        print(token, token.pos_, token.dep_)
    return list(
      uniq(ent.label_ for ent in doc.ents)
    )
