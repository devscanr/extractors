# from pprint import pprint
import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span
from typing import Sequence, cast
from ..category.extractor import get_consequent, get_preceding
from ..patterns import to_patterns2
from ..utils import get_nlp, uniq
from .data import SKILLS, Skill

IN, LOWER, ORTH, POS = "IN", "LOWER", "ORTH", "POS"

class SkillExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.nlp = get_nlp(name)
    ruler1 = cast(EntityRuler, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name="er1"))
    ruler2 = cast(EntityRuler, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name="er2"))
    def add_patterns_to(ruler: EntityRuler, skills: list[Skill]) -> None:
      for skill in skills:
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
              "pattern": (
                [{ORTH: phrase, POS: {IN: poss}}]
                if re.search(r"[A-Z]", phrase)
                else [{LOWER: phrase, POS: {IN: poss}}]
              )
            }])
          elif isinstance(item, list):
            ruler.add_patterns([{
              "label": skill.name,
              "pattern": item
            }])
    add_patterns_to(ruler1, [skill for skill in SKILLS if not skill.name.endswith(":maybe")]) # TODO better split fn
    add_patterns_to(ruler2, [skill for skill in SKILLS if skill.name.endswith(":maybe")])     # /

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[list[str]]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list((token, token.pos_) for token in doc if not token.is_punct))
    # print("ents:", list(ent.label_ for ent in doc.ents))
    skills = [
      skill for ent in doc.ents
      if (skill := self.ensure_skill(ent))
    ]
    return uniq(skills)

  def ensure_skill(self, ent: Span) -> str | None:
    if ent.label_.endswith(":maybe"):
      has_neighbour_skill = any(
        token
        for token in get_preceding(ent[0])[-2:] + get_consequent(ent[-1])[:2]
        if not token.is_punct and token.ent_type_
      )
      return ent.label_.replace(":maybe", "") if has_neighbour_skill else None
    else:
      return ent.label_
