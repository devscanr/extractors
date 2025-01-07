from dataclasses import dataclass
import re
from spacy.tokens import Token
from typing import Callable
from ..patterns import expand_phrases12
from ..spacyhelpers import left_token, right_token
from ..utils import Pattern, lookslike

__all__ = [
  "Skill", "Term", "Topic",
  "Disambiguate",
]

type Disambiguate = Callable[[Token], bool]
type Resolve = Callable[[Token], list[str]]

@dataclass
class Skill:
  name: str
  phrases: list[
    str |   # Custom pattern (exact matches)
    Pattern # Spacy pattern
  ]
  descr: str | None = None
  disambiguate: Disambiguate | list[Disambiguate] | None = None
  resolve: Resolve | list[str] | None = None

@dataclass
class Term(Skill):
  pass

@dataclass
class Topic(Skill):
  descr: None = None

def dis_context(*phrases: str) -> Disambiguate:
  regmarkers = [
    re.compile(rf"{re.escape(marker)}", re.IGNORECASE)
    for marker in expand_phrases12(phrases)
  ]
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    if ltoken and ltoken.lower_ == "#":
      # Hashtagged
      return True
    for tok in token.sent:
      if tok != token:
        lower = tok.lower_
        if any(True for regmarker in regmarkers if lookslike(lower, regmarker)):
          return True
    return False
  return disambiguate

def dis_sequence() -> Disambiguate:
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    rtoken = right_token(token)
    ltoken2 = left_token(ltoken) if ltoken else None
    rtoken2 = right_token(rtoken) if rtoken else None
    if ltoken and ltoken.lower_ == "#":
      # Hashtagged
      return True
    elif re.match("[A-Z]", token.text):
      # Capitalized
      if ltoken and ltoken.text == "," and ltoken2 and re.match("[A-Z#]", ltoken2.text):
        # And the prev word is capitalized or hashtagged
        return True
      elif rtoken and rtoken.text == "," and rtoken2 and re.match("[A-Z#]", rtoken2.text):
        # And the next word is capitalized or hashtagged
        return True
    return False
  return disambiguate

def dis_letter() -> Disambiguate:
  markers = {"lang", "language"}
  def disambiguate(token: Token) -> bool:
    print("@ disambiguate letter", token)
    ltoken = left_token(token)
    if ltoken and ltoken.lower_ == "#":
      return True
    rtoken = right_token(token)
    # Avoid highly ambiguos cases, at the cost of some FNs:
    if ltoken and ltoken.lower_ in {"-", "@"}:
      return False # foo-c, bar-v
    elif rtoken and rtoken.lower_ == "-":
      rtoken2 = right_token(rtoken)
      if rtoken2 and rtoken2.lower_ not in markers:
        return False # c-foo, v-bar
    return True
  return disambiguate

# def oneof(*dis_fns) -> Disambiguate:
#   def disambiguate(token: Token) -> bool:
#     return any(dis_fn(token) for dis_fn in dis_fns)
#   return disambiguate

def clean(label: str) -> str:
  return re.sub(r":maybe:.+$", "", label)
