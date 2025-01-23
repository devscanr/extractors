import re
from spacy.tokens import Token
from typing import cast
from extractors.ppatterns import expand_parens
from extractors.utils import prev_token, revlist, revtakeuntil

PAST_MARKERS = {
  "ex",
  "former", "formerly",
  "previous", "previously",
  "retired",
  # past, time ago
}

PRESENT_MARKERS = {
  "current", "currently",
  "now", "nowadays", "today",
  "at present", "at the moment",
  # "atm", "a.t.m."
}

FUTURE_MARKERS = {
  "aspiring", "future", "upcoming",
}

INTENT_MARKERS = set([
  intent + " " + be
  for intent in [
    "going",
    "strive", "strives", "striving",
    "plan", "plans", "planning",
    "want", "wants", "wanting",
    "wish", "wishes", "wishing",
  ]
  for be in ["to be", "to become"] # TODO smth like "to _eventually_ become"
] + ["gonna be", "wanna be", "wannabe", "gonnabe"])

def is_hashtagged(token: Token) -> bool:
  j = cast(int, token._.i)
  return j > 0 and token.sent[j - 1].lower_ == "#"

def get_ancestors(token: Token) -> list[Token]:
  tok = token
  toks: list[Token] = []
  while tok != tok.head and tok.dep_ != "dep":
    i = tok.i
    tok = tok.head
    if (
      tok.pos_ in {"AUX", "VERB"} or
      tok.pos_ in {"ADJ", "NOUN", "PROPN", "DET"} and tok.i > i
    ):
      toks.append(tok)
    else:
      break
  return toks

# is_negated
def is_negated(token: Token) -> bool:
  # print("@ is_negated", token)
  # Note: Spacy makes mistakes with 'not' head as major as it does with other things @_@
  chain = [token, *get_ancestors(token)]
  return any(_is_negated(item) for item in chain)

def _is_negated(token: Token) -> bool:
  # print("@ _is_negated:", token)
  non_chain = [*revlist(revtakeuntil(lambda tok: tok.text in {",", ";"}, token.lefts)), token]
  for tok in non_chain:
    if re.match(r"non[-.]?(?!\w)", tok.lower_):
      return True
  ## Hacks for Spacy invalid dep. parsing ##
  pt1 = prev_token(token)
  pt2 = prev_token(pt1)
  if pt1 and re.match(r"non[-.]?(?!\w)", pt1.lower_):
    return True
  if pt2 and re.match(r"non[-.]?(?!\w)", pt2.lower_) and pt1 and pt1.text in {".", "-"}:
    return True
  ## ##
  for tok in token.sent:
    if tok.head == token and tok.dep_ == "neg":
      # (not) < ($token) -- "not a developer"
      # (non) < ($token) -- "non developer"
      return True
    elif tok.head.head == token and tok.head.dep_ == "compound" and tok.dep_ == "neg":
      # (not) < ($) < ($token) -- "not job seeking"
      return True
  return False

# is_past
def is_past(token: Token) -> bool:
  # print("@ is_past", token)
  chain = [token, *get_ancestors(token)]
  return any(_is_past(item) for item in chain)

def _is_past(token: Token) -> bool:
  # print("@ _is_past", token)
  ex_chain = [*revlist(revtakeuntil(lambda tok: tok.text in {",", ";"}, token.lefts)), token]
  for tok in ex_chain:
    if re.match(r"ex[-.]?(?!\w)", tok.lower_):
      return True
  ## Hacks for Spacy invalid dep. parsing ##
  pt1 = prev_token(token)
  pt2 = prev_token(pt1)
  if pt1 and re.match(r"ex[-.]?(?!\w)", pt1.lower_):
    return True
  if pt2 and re.match(r"ex[-.]?(?!\w)", pt2.lower_) and pt1 and pt1.text in {".", "-"}:
    return True
  ## ##
  if token.head.lower_ in {"was", "were"}:
    # (was) > $token
    return True
  for tok in token.sent:
    if tok.head == token and tok.lower_ in {"ex", "former", "formerly", "previous", "previously", "retired"}:
      # (former) < ($token)
      return True
    elif tok.lower_ == "ago":
      # (ago) < ($token) -- "developer, some time ago"
      return True
  return False

# is_future
def is_future(token: Token) -> bool:
  # print("@ is_future", token)
  chain = [token, *get_ancestors(token)]
  return any(_is_future(item) for item in chain)

def _is_future(token: Token) -> bool:
  # print("@ _is_future", token)
  if token.head.lower_ in {"wannabe"} and token.dep_ != "dep":
    # ($token) < (wannabe)
    return True
  elif token.head.lower_ in OPPORTUNITY_WORDS and token.dep_ != "dep":
    # ($token) < (opportunity)
    return True
  elif token.head.lower_ in {"be", "become"} and token.dep_ != "dep":
    # (be) > ($token)
    if any(t.lower_ in WILL_WORDS for t in token.head.lefts):
      # (will) < (be) > ($token)
      return True
    elif token.head.head.lower_ in PLAN_WORDS:
      # (plan) > (be) > ($token)
      return True
  elif token.head.lower_ in SEARCH_WORDS and token.dep_ != "dep":
    # (search) > ($token) -- "seeking an intership"
    return True
  elif token.head.lower_ == "for" and token.head.head.lower_ in SEARCH_WORDS and token.dep_ != "dep":
    # (search) > (for) > ($token) -- "looking for intership"
    return True
  elif any(tok.lower_ in FUTURE_WORDS for tok in token.lefts):
    # (future) < ($token)
    return True
  elif any(tok.head == token and tok.lower_ in FUTURE_WORDS for tok in token.lefts):
    # (future) < ($) < ($token) -- accounting for certain Spacy issues
    return True
  return False

# Lemmas are confusing and inconsistent, intentionally not using them
def expand_words(words: list[str]) -> set[str]:
  return set(
    patt for word in words
    for patt in expand_parens(word)
  )

WILL_WORDS = expand_words([
  # (verb) < be > developer
  "will(s)", "'ll",
])

PLAN_WORDS = expand_words([
  # ($verb) > (be) > ($token)
  "aspire(s)", "aspiring",
  "go(es)", "going", "gon", # gonna -> gon na
  # "hop(es)", "hoping",
  "plan(s)", "planning",
  "look(s)", "looking", # e.g "looking forward"
  "strive(s)", "striving",
  "want(s)", "wanting", "wan", # wanna -> wan na
  "wish(es)", "wishing"
  "work(s)", "working",
  "willing",
])

FUTURE_WORDS = {
  # ($adj) < ($token)
  # ($adj) < ($) < ($token)
  "aspiring", "future", "gonnabe",
  "striving", "upcoming", "wannabe",
}

SEARCH_WORDS = expand_words([
  # ($verb) > (for) > ($token)                 -- "looking for intership"
  # ($verb) > (for) > (opportunity) < ($token) -- "looking for intership opportunities"
  # ($verb) > ($token)                         -- "seeking an intership"
  # ($verb) > (opportunity) < ($token)         -- "seeking an intership opportunity"
  "look(s)", "looking",
  "search(es)", "searching",
  "seek(s)", "seeking",
])

OPPORTUNITY_WORDS = expand_words([
  "offer(s)",
  "opportunity", "opportunities",
  "option(s)",
  "proposal(s)",
])
