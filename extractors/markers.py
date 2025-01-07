from spacy.tokens import Token
from typing import cast

__all__ = [
  # "EX_MARKERS",
  # "PAST_MARKERS",
  # "FUTURE_MARKERS",
  "is_hashtagged",
  "is_negated",
  "is_past",
  "is_future",
  "is_metaphorical",
]

# EX_MARKERS = {
#   "ex"
# }

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
  # print("@ is_negated", noun)
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
  # root = token.sent.root
  # for tok in noun.sent:
  #   pprint({"token": tok.lower_, "head": tok.head})
  for tok in noun.sent:
    if tok == noun.head and tok.lower_ in {"was", "were"}:
      return True # was <- developer
    if (tok.head == noun) and tok.lower_ in {"ex", "former", "formerly", "previous", "previously", "retired"}:
      #  or tok.head == noun.head
      # print("-1-")
      # print("noun:", noun)
      # print("tok:", tok)
      # print("tok.head:", tok.head)
      # print("noun.head:", noun.head)
      return True # former -> developer, retired -> developer
    if tok.lower_ == "ago":
      return True # "time ago", "years ago", etc.
  return False

def is_future(noun: Token) -> bool:
  # print("@ is_future", noun)
  # for tok in noun.sent:
  #   pprint({"token": tok.lower_, "pos": tok.pos_, "dep": tok.dep_, "lemma": tok.lemma_, "head": tok.head})
  for tok in noun.sent:
    if tok == noun.head and tok.lower_ in {"be", "become"}:
      if any(True for t in noun.sent if t.head == tok and t.lemma_ == WILL_WORD):
        return True # will be/become <- developer
      if any(True for t in noun.sent if t == tok.head and t.lemma_ in PLAN_WORDS):
        return True # going/plan/want/wishing to be/become <- developer
    if tok == noun.head and tok.lower_ in {"wannabe"}:
      return True # developer -> wannabe
    if (tok.head == noun or tok.head.head == noun) and tok.lower_ in FUTURE_WORDS:
      return True # wannabe/future -> developer, future -> laravel -> developer
  return False

def is_metaphorical(noun: Token) -> bool:
  # print("noun.lefts:", noun.lefts)
  if {tok.lower_ for tok in noun.lefts} & {"always", "constant", "eternal", "everlasting", "forever", "lifelong", "perpetual"}:
    return True
  subtree = list(noun.subtree)
  doubles = [
    (tup[0].lower_, tup[1].lower_)
    for tup in zip(subtree, subtree[1:])
  ]
  triples = [
    (tup[0].lower_, tup[1].lower_, tup[2].lower_)
    for tup in zip(subtree, subtree[1:], subtree[2:])
  ]
  if {tup for tup in doubles} & {("life", "long"), ("of", "life")}:
    return True
  if {tup for tup in triples} & {("life", "-", "long")}:
    return True
  return False

WILL_WORD = "will"
PLAN_WORDS = {"aspire", "go", "plan", "strive", "want", "wish"}
FUTURE_WORDS = {"aspiring", "future", "gonnabe", "striving", "upcoming", "wannabe"}

# METAPHORIC_MARKERS = {
#   "always", "constant", "eternal", "everlasting",
#   "forever", "frantically", "life", "lifelong", "never",
#   "permanent", "perpetual",
# }
