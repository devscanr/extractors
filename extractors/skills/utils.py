from dataclasses import dataclass
from spacy.tokens import Span
from typing import Any, Callable

__all__ = ["Skill", "Disambiguate", "MaybeSkill", "contextual", "neighbour"]

@dataclass
class Skill:
  name: str
  phrases: list[
    str |                # Custom lang (produces exact matches)
    list[dict[str, Any]] # Spacy pattern
  ]
  # categories: list[str] | None = field(default_factory=lambda: [])

type Disambiguate = Callable[[Span], bool]

@dataclass
class MaybeSkill(Skill):
  disambiguate: Disambiguate

def contextual_or_neighbour(skills: list[str], distance: int) -> Disambiguate:
  fn1 = contextual(*skills)
  fn2 = neighbour(distance)
  def disambiguate(ent: Span) -> bool:
    return fn1(ent) or fn2(ent)
  return disambiguate

def contextual(*skills: str) -> Disambiguate:
  ctx_skills = set(skills)
  def disambiguate(ent: Span) -> bool:
    doc = ent[0].doc
    skill = ent[0].ent_type_
    other_skills = [ent.label_ for ent in doc.ents if ent.label_ != skill]
    return any(
      True for skill in other_skills if any(
        skill == cs or skill.startswith(cs + "-") and not ":maybe:" in skill
        for cs in ctx_skills
      )
    )
  return disambiguate

def neighbour(distance: int) -> Disambiguate:
  def disambiguate(ent: Span) -> bool:
    doc = ent[0].doc
    tis = [t.i for t in ent] # indexes of current Entity' tokens
    otis = [t.i for e in doc.ents for t in e if e != ent] # indexes of other Entities' tokens
    return any(
      True for ti in tis
      if any(abs(oti - ti) <= distance for oti in otis)
    )
  return disambiguate
