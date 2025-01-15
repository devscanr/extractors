import re
from spacy.tokens import Token
from ..extractor import Disambiguate
from ..ppatterns import to_ppatterns
from ..spacyhelpers import left_token, right_token
from ..utils import lookslike

def dis_context(*phrases: str) -> Disambiguate:
  # TODO use matchers to support multi-words combinations
  regmarkers = [
    re.compile(rf"{re.escape(marker)}", re.IGNORECASE)
    for marker in to_ppatterns(list(phrases))
  ]
  def disambiguate(token: Token) -> bool:
    ltoken = left_token(token)
    if ltoken and ltoken.lower_ == "#":
      # Hashtagged
      return True
    for tok in token.sent:
      if tok != token:
        lower = tok.lower_
        if any(lookslike(lower, regmarker) for regmarker in regmarkers):
          return True
    return False
  return disambiguate

def dis_neighbours() -> Disambiguate:
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
      if ltoken and ltoken.text in {",", ")"} and ltoken2 and re.match("[A-Z#]", ltoken2.text):
        # And the prev word is capitalized or hashtagged
        return True
      elif rtoken and rtoken.text in {",", "("} and rtoken2 and re.match("[A-Z#]", rtoken2.text):
        # And the next word is capitalized or hashtagged
        return True
      elif ltoken and rtoken and ltoken.text == "(" and rtoken.text == ")":
        # And the token is within parentheses
        return True
    return False
  return disambiguate

def dis_letter() -> Disambiguate:
  markers = {"lang", "language"}
  def disambiguate(token: Token) -> bool:
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
