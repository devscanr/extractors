# from pprint import pprint
import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span
from typing import Any, Callable, cast, Sequence
from ..patterns import to_patterns2
from ..utils import get_nlp, hash_skillname, Pattern, uniq
from .data.all import MaybeSkill, SKILLS, Skill

IN, LOWER, ORTH, POS = "IN", "LOWER", "ORTH", "POS"

type Disambiguate = Callable[[Span], bool]

class SkillExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.disambiguates: dict[str, Disambiguate] = {}
    self.nlp = get_nlp(name)
    self.nlp.add_pipe("index_tokens_by_sents")
    skills: list[Skill] = []
    mskills: list[Skill] = []
    for skill in SKILLS:
      is_mskill = isinstance(skill, MaybeSkill)
      (skills, mskills)[int(is_mskill)].append(skill)
    self.add_pipe_er("entity_ruler1", skills)
    self.add_pipe_er("entity_ruler2", mskills)

  def add_pipe_er(self, name: str, skills: list[Skill]) -> None:
    ruler: EntityRuler = cast(Any, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name=name))
    for skill in skills:
      if isinstance(skill, MaybeSkill):
        self.disambiguates[label(skill)] = skill.disambiguate
      for item in skill.phrases:
        if isinstance(item, str):
          ruler.add_patterns(from_phrase(skill, item))
        elif isinstance(item, list):
          ruler.add_patterns(from_pattern(skill, item))

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[list[str]]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list((token, token.pos_, token.dep_) for token in doc if not token.is_punct))
    # print("ents:", list(ent.label_ for ent in doc.ents))
    skills = [
      skill for ent in doc.ents
      if (skill := self.ensure_skill(ent))
    ]
    return uniq(skills)

  def ensure_skill(self, ent: Span) -> str | None:
    if ":maybe:" in ent.label_:
      is_skill = self.disambiguates[ent.label_](ent)
      return re.sub(r":maybe:.+$", "", ent.label_) if is_skill else None
    return ent.label_

def from_pattern(skill: Skill, pattern: Pattern) -> Pattern:
  return [{
    "label": label(skill),
    "pattern": pattern
  }]

def from_phrase(skill: Skill, phrase: str) -> Pattern:
  return [{
    "label": label(skill),
    "pattern": pattern,
  } for pattern in to_patterns2(phrase)]

def label(skill: Skill) -> str:
  if isinstance(skill, MaybeSkill):
    return skill.name + ":maybe:" + hash_skillname(skill.name)
  else:
    return skill.name
