from spacy.tokens import Token
from typing import cast
from extractors.ppatterns import expand_parens

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

# def is_exed(token: Token) -> bool:
#   j = cast(int, token._.i)
#   if j > 0:
#     if token.sent[j - 1].lower_ in {"ex"}:
#       return True # e.g. "ex engineer"
#   if j > 1:
#     if token.sent[j - 2].lower_ in {"ex"}:
#       return True # e.g. "ex-engineer" or "ex. engineer"
#   if j > 2:
#     if token.sent[j - 3].lower_ in {"ex"}:
#       return True # e.g. "ex-web engineer"
#   return False

def is_negated(noun: Token) -> bool:
  root = noun.sent.root
  for tok in noun.sent:
    if tok.is_punct:
      continue
    if (
      tok.head == root or # "am not", "were not"
      tok.head == noun or # "not developer", "not a developer"
      tok.head.head == noun and tok.head.dep_ == "compound" # "not job seeking"
    ) and tok.dep_ == "neg":
      return True
    if tok.head == noun and tok.lower_ == "non":
      return True
    # if (tok.head.head == root or tok.head.head == noun) and tok.head.dep_ == "compound":
    #   return True
  return False

def is_past(noun: Token) -> bool:
  # print("@ is_past", noun)
  for tok in noun.sent:
    if tok == noun.head and tok.lower_ in {"was", "were"}:
      # was <- developer
      return True
    if (tok.head == noun) and tok.lower_ in {"ex", "former", "formerly", "previous", "previously", "retired"}:
      # former -> developer, retired -> developer
      return True
    if tok.lower_ == "ago":
      # "time ago", "years ago", etc.
      return True
  return False

def is_future(noun: Token) -> bool:
  # print("@ is_future", noun)
  for tok in noun.sent:
    if tok == noun.head and tok.lower_ in {"be", "become"}:
      # (tok:be) > (noun:developer)
      if any(t.head == tok and t.lower_ in WILL_WORDS for t in noun.sent):
        # (t:_verb) < (tok:be) > (noun:developer)
        return True
      if tok.head.lower_ in PLAN_WORDS:
        # (tok.head:_verb) > (tok:be) > (noun:developer)
        return True
    if tok == noun.head and tok.lower_ in {"wannabe"}:
      # (noun:developer) < (tok:wannabe)
      return True
    if (tok.head == noun or tok.head.head == noun) and tok.lower_ in FUTURE_WORDS:
      # (tok:future) < (noun:developer)
      # (tok:future) < (laravel) < (noun:developer) -- wrong Spacy parsing
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
  # (_verb) > (be) > (developer)
  "aspire(s)", "aspiring",
  "go(es)", "going", "gon", # gonna -> gon na
  "plan(s)", "planning",
  "look(s)", "looking",
  "strive(s)", "striving",
  "want(s)", "wanting", "wan", # wanna -> wan na
  "wish(es)", "wishing"
  "work(s)", "working",
  "willing",
])

FUTURE_WORDS = {
  # (_adj) < (developer), (_adj) < (_) < (developer)
  "aspiring", "future", "gonnabe",
  "striving", "upcoming", "wannabe",
}
