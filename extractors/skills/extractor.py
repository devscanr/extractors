# from pprint import pprint
import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span
from typing import Any, Callable, cast, Sequence
from ..patterns import to_patterns2
from ..utils import get_nlp, hash_skillname, Pattern, uniq
from .data import SKILLS
from .utils import Skill

IN, LOWER, ORTH, POS = "IN", "LOWER", "ORTH", "POS"

type Disambiguate = Callable[[Span], bool]

class SkillExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.stacks: dict[str, list[str]] = {}
    self.disambiguates: dict[str, Disambiguate] = {}
    self.nlp = get_nlp(name)
    self.nlp.add_pipe("index_tokens_by_sents")
    skills: list[Skill] = []
    mskills: list[Skill] = []
    for skill in SKILLS:
      is_mskill = skill.disambiguate is not None
      (skills, mskills)[int(is_mskill)].append(skill)
    self.add_pipe_er("entity_ruler1", skills)
    self.add_pipe_er("entity_ruler2", mskills)

  def add_pipe_er(self, name: str, skills: list[Skill]) -> None:
    ruler: EntityRuler = cast(Any, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name=name))
    for skill in skills:
      if skill.stack:
        assert skill.name not in self.disambiguates, f"{skill.name!r} issue: multiple `stack` rules are not supported yet"
        self.stacks[skill.name] = skill.stack
      if skill.disambiguate:
        l = label(skill)
        assert l not in self.disambiguates, f"{skill.name!r} issue: multiple `disambiguate` rules are not supported yet"
        self.disambiguates[l] = skill.disambiguate
      for item in skill.phrases:
        if isinstance(item, str):
          assert not re.search("[A-Z]", item), f"{item!r} contains uppercase character(s), use pattern syntax"
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
      skill
      for ent in doc.ents
      for skill in self.get_skill(ent)
    ]
    return uniq(skills)

  def get_skill(self, ent: Span) -> list[str]:
    if ":maybe:" in ent.label_:
      if self.disambiguates[ent.label_](ent):
        l = clean(ent.label_)
        if l in self.stacks:
          return self.stacks[l]
        else:
          return [l]
      else:
        return []
    if ent.label_ in self.stacks:
      return self.stacks[ent.label_]
    else:
      return [ent.label_]

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
  if skill.disambiguate:
    return skill.name + ":maybe:" + hash_skillname(skill.name)
  else:
    return skill.name

def clean(label: str) -> str:
  return re.sub(r":maybe:.+$", "", label)
