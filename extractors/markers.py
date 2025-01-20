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

def is_negated(noun: Token) -> bool:
  # print("@ is_negated", noun)
  root = noun.sent.root
  for tok in noun.sent:
    if tok.head == root and (tok.dep_ == "neg" or tok.lower_ == "non"):
      # (not) < ($root) -- "never was a developer"
      return True
    elif tok.head == noun and tok.dep_ == "neg" or tok.lower_ == "non":
      # (not) < ($noun) -- "not a developer"
      # (non) < ($noun) -- "non developer"
      return True
    elif tok.head.head == noun and tok.head.dep_ == "compound" and tok.dep_ == "neg":
      # (not) < ($) < ($noun) -- "not job seeking"
      return True
  return False

def is_past(noun: Token) -> bool:
  # print("@ is_past", noun)
  if noun.head.lower_ in {"was", "were"}:
    # (was) > $noun
    return True
  for tok in noun.sent:
    if tok.head == noun and tok.lower_ in {"ex", "former", "formerly", "previous", "previously", "retired"}:
      # (former) < ($noun)
      return True
    elif tok.lower_ == "ago":
      # (ago) < ($noun) -- "developer, some time ago"
      return True
  return False

def is_future(noun: Token) -> bool:
  # print("@ is_future", noun)
  if noun.head.lower_ in {"wannabe"}:
    # ($noun) < (wannabe)
    return True
  elif noun.head.lower_ in OPPORTUNITY_WORDS:
    # ($noun) < (opportunity)
    return True
  elif noun.head.lower_ in {"be", "become"}:
    # (be) > ($noun)
    if any(t.lower_ in WILL_WORDS for t in noun.head.lefts):
      # (will) < (be) > ($noun)
      return True
    elif noun.head.head.lower_ in PLAN_WORDS:
      # (plan) > (be) > ($noun)
      return True
  elif any(tok.lower_ in FUTURE_WORDS for tok in noun.lefts):
    # (future) < ($noun)
    return True
  elif any(tok.head == noun and tok.lower_ in FUTURE_WORDS for tok in noun.lefts):
    # (future) < ($) < ($noun) -- accounting for certain Spacy issues
    return True
  elif noun.head.lower_ in SEARCH_WORDS:
    # (search) > ($noun) -- "seeking an intership"
    return True
  elif noun.head.lower_ == "for" and noun.head.head.lower_ in SEARCH_WORDS:
    # (search) > (for) > ($noun) -- "looking for intership"
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
  # ($verb) > (be) > ($noun)
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
  # ($adj) < ($noun)
  # ($adj) < ($) < ($noun)
  "aspiring", "future", "gonnabe",
  "striving", "upcoming", "wannabe",
}

SEARCH_WORDS = expand_words([
  # ($verb) > (for) > ($noun)                 -- "looking for intership"
  # ($verb) > (for) > (opportunity) < ($noun) -- "looking for intership opportunities"
  # ($verb) > ($noun)                         -- "seeking an intership"
  # ($verb) > (opportunity) < ($noun)         -- "seeking an intership opportunity"
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
