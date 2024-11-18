from dataclasses import dataclass, field
from spacy.tokens import Span, Token
from typing import Callable
from ..utils import Pattern, get_cons_tokens, get_prec_tokens

__all__ = ["Skill", "Disambiguate", "contextual", "neighbour"]

type Disambiguate = Callable[[Span], bool]

@dataclass
class Skill:
  name: str
  phrases: list[
    str |   # Custom pattern (exact matches)
    Pattern # Spacy pattern
  ]
  descr: str
  stack: list[str] = field(default_factory=lambda: [])
  # categories: list[str] = field(default_factory=lambda: [])
  disambiguate: Disambiguate | None = None

# @dataclass
# class MaybeSkill(Skill):

def contextual_or_neighbour(skills: list[str], distance: int) -> Disambiguate:
  fn1 = contextual(*skills)
  fn2 = neighbour(distance)
  def disambiguate(ent: Span) -> bool:
    return fn1(ent) or fn2(ent)
  return disambiguate

def contextual(*skills: str) -> Disambiguate:
  ctx_skills = set(skills)
  def disambiguate(ent: Span) -> bool:
    # TODO consider only words within the same paragraph
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
  # TODO next word as "Developer", "Dev", "Engineer" (maybe all DEV & STUDENT roles)
  # should also disambiguate the skill
  def disambiguate(ent: Span) -> bool:
    doc = ent[0].doc
    tis = [
      t.i for t in ent
    ] # indexes of current Entity' tokens
    otis = [
      t.i for e in doc.ents for t in e
      if e != ent and (":maybe:" not in e.label_)
    ] # indexes of other (non-maybe) Entity tokens
    return any(
      True for ti in tis
      if any(abs(oti - ti) <= distance for oti in otis)
    )
  return disambiguate

def singleletter() -> Disambiguate:
  def disambiguate(ent: Span) -> bool:
    # doc = ent[0].doc
    prec_tokens = get_prec_tokens(ent[0])
    cons_tokens = get_cons_tokens(ent[-1])
    # Avoid highly ambiguos cases, at the cost of some FNs:
    if gets(prec_tokens, -1) == "-":
      return False # foo-c, bar-v
    if gets(cons_tokens, 0) == "-" and gets(cons_tokens, 1) not in {"lang", "language"}:
      return False # c-foo, v-bar
    return True
  return disambiguate

def gets(tokens: list[Token], index: int) -> str:
  return tokens[index].lower_ if -len(tokens) <= index < len(tokens) else ""
