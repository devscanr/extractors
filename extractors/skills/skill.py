from dataclasses import dataclass
from spacy.tokens import Token
from typing import Callable
from ..extractor import Tag

type Resolve = Callable[[Token], list[str]]

@dataclass
class Skill(Tag):
  resolve: Resolve | list[str] | None = None

@dataclass
class Topic(Skill):
  descr: str = "Topic"

# Web, UI/UX and Design
