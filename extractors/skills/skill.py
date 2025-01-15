from dataclasses import dataclass, field
from spacy.tokens import Token
from typing import Callable, Literal
from ..extractor import Disambiguate, Tag
from ..dpatterns import DPattern
from ..xpatterns import XPattern

type Group = Literal["Language", "Tech", "Topic", "Company", "Certificate"]
type Resolve = Callable[[Token], list[str]]

@dataclass
class Skill(Tag):
  group: Group = field(kw_only=True)
  exclusive: bool = field(default=True, kw_only=True)
  resolve: Resolve | list[str] | None = field(default=None, kw_only=True)

def Tech(
  name: str,
  phrases: list[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ],
  descr: str = "Tech",
  disambiguate: Disambiguate | list[Disambiguate] | None = None,
  resolve: Resolve | list[str] | None = None,
  exclusive: bool = True
) -> Skill:
  return Skill(
    name, phrases, descr,
    exclusive = exclusive,
    disambiguate = disambiguate,
    resolve = resolve,
    group = "Tech"
  )

def Topic(
  name: str,
  phrases: list[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ],
  descr: str = "Topic",
  disambiguate: Disambiguate | list[Disambiguate] | None = None,
  resolve: Resolve | list[str] | None = None,
  exclusive: bool = True
) -> Skill:
  return Skill(
    name, phrases, descr,
    exclusive = exclusive,
    disambiguate = disambiguate,
    resolve = resolve,
    group = "Topic"
  )

def Language(
  name: str,
  phrases: list[
    str |    # Custom (converted to XPattern, DPattern or expanded)
    XPattern # Matcher pattern
  ],
  descr: str = "Language",
  disambiguate: Disambiguate | list[Disambiguate] | None = None,
) -> Skill:
  return Skill(
    name, phrases, descr,
    disambiguate = disambiguate,
    group = "Language"
  )

def Company(
  name: str,
  phrases: list[
    str |    # Custom (converted to XPattern, DPattern or expanded)
    XPattern # Matcher pattern
  ],
  descr: str = "Company",
  disambiguate: Disambiguate | list[Disambiguate] | None = None
) -> Skill:
  return Skill(
    name, phrases, descr,
    disambiguate = disambiguate,
    group = "Company"
  )

def Certificate(
  name: str,
  phrases: list[
    str |    # Custom (converted to XPattern, DPattern or expanded)
    XPattern # Matcher pattern
  ],
  descr: str = "Certificate",
  disambiguate: Disambiguate | list[Disambiguate] | None = None
) -> Skill:
  return Skill(
    name, phrases, descr,
    disambiguate = disambiguate,
    group = "Certificate"
  )
