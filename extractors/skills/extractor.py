import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span
from typing import Any, Callable, cast, Sequence
from ..patterns import to_patterns2
from ..utils import get_nlp, hash_skillname, Pattern, uniq
from .data import SKILLS
from .utils import Disambiguate, Resolve, Skill

IN, LOWER, ORTH, POS = "IN", "LOWER", "ORTH", "POS"

class SkillExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.descriptions: dict[str, str] = {}
    self.disambiguates: dict[str, Disambiguate] = {}
    self.resolvers: dict[str, Resolve] = {}
    self.aliases: dict[str, str] = {}
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
      if skill.disambiguate:
        l = label(skill)
        assert l not in self.disambiguates, f"{skill.name!r} issue: multiple `disambiguate` rules are not supported yet"
        self.disambiguates[l] = skill.disambiguate
      if skill.resolve:
        assert skill.name not in self.resolvers, f"{skill.name!r} issue: duplicate `resolve`"
        self.resolvers[skill.name] = skill.resolve
      if skill.alias:
        assert skill.name not in self.aliases, f"{skill.name!r} issue: duplicate `alias`"
        self.aliases[skill.name] = skill.alias
      if skill.name not in self.descriptions:
        self.descriptions[skill.name] = skill.descr
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
    # print(">>>", self.nlp.tokenizer.explain(text_or_doc))
    # for token in doc:
    #   print(token, token.pos_)
      # pprint(list((token, token.pos_, token.dep_) for token in doc if not token.is_punct))
    # print("ents:", list(ent.label_ for ent in doc.ents))

    # Disambiguate entities
    ents: list[Span] = []
    for ent in doc.ents:
      if ":maybe:" not in ent.label_ or self.disambiguates[ent.label_](ent):
        ent.label_ = clean(ent.label_)
        ents.append(ent)
    doc.ents = ents

    # Resolve entities to skills
    skills: list[str] = []
    for sent in doc.sents:
      sent_skills: list[str] = []
      for ent in sent.ents:
        if ent.label_ in self.resolvers:
          sent_skills += self.resolvers[ent.label_](ent)
        else:
          sent_skills.append(ent.label_)
      skills += [
        skill for skill in sent_skills
        if self.descriptions.get(skill, "") != "Competence" or
           not any(s.startswith(skill + "-") for s in sent_skills)
      ]
    return [
      self.aliases.get(skill, skill)
      for skill in uniq(skills)
    ]

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
