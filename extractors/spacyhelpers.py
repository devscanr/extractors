from spacy.tokens import Token

(IN, IS_PUNCT, IS_SENT_START, LOWER, OP, ORTH, POS, REGEX, TAG) = (
  "IN", "IS_PUNCT", "IS_SENT_START", "LOWER", "OP", "ORTH", "POS", "REGEX", "TAG"
)
(LEFT_ID, REL_OP, RIGHT_ID, RIGHT_ATTRS) = ("LEFT_ID", "REL_OP", "RIGHT_ID", "RIGHT_ATTRS")

def is_word(token: Token) -> bool:
  return not token.is_punct and not token.is_space

# LEFT
def left_tokens(token: Token) -> list[Token]:
  return list(token.doc[token.sent.start:token.i])

def left_lowers(token: Token) -> list[str]:
  return [
    tok.lower_ for tok in left_tokens(token)
  ]

def left_lowerwords(token: Token) -> list[str]:
  return [
    tok.lower_ for tok in left_tokens(token)
    if is_word(tok)
  ]

def left_token(token: Token) -> Token | None:
  ltokens = left_tokens(token)
  return ltokens[-1] if ltokens else None

def left_lower(token: Token) -> str | None:
  llowers = left_lowers(token)
  return llowers[-1] if llowers else None

def left_lowerword(token: Token) -> str | None:
  lwords = left_lowerwords(token)
  return lwords[-1] if lwords else None

# RIGHT
def right_tokens(token: Token) -> list[Token]:
  return list(token.doc[token.i+1:token.sent.end])

def right_lowers(token: Token) -> list[str]:
  return [
    tok.lower_ for tok in right_tokens(token)
  ]

def right_lowerwords(token: Token) -> list[str]:
  return [
    tok.lower_ for tok in right_tokens(token)
    if is_word(tok)
  ]

def right_token(token: Token) -> Token | None:
  rtoks = right_tokens(token)
  return rtoks[0] if rtoks else None

def right_lower(token: Token) -> str | None:
  rtoks = right_lowers(token)
  return rtoks[0] if rtoks else None

def right_lowerword(token: Token) -> str | None:
  rwords = right_lowerwords(token)
  return rwords[0] if rwords else None

# LEVELS
def ancestors(token: Token) -> list[Token]:
  tok = token
  toks: list[Token] = []
  while tok != tok.head:
    tok = tok.head
    toks.append(tok)
  return toks

def right_ancestors(token: Token) -> list[Token]:
  tok = token
  toks: list[Token] = []
  while tok != tok.head:
    tok = tok.head
    if tok.i > token.i:
      toks.append(tok)
    else:
      break
  return toks

def token_level(token: Token) -> int:
  level = 0
  while token != token.sent.root:
    level += 1
    token = token.head
  return level
