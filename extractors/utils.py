from emoji import replace_emoji
import hashlib
from pathlib import Path
import re
import spacy
from spacy import Language
from spacy.tokens import Doc, Span, Token
from typing import Any, Callable, Generator, cast, Iterable

# RESOURCES
# - https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk

(IN, IS_PUNCT, IS_SENT_START, LOWER, OP, ORTH, POS, REGEX, TAG) = (
  "IN", "IS_PUNCT", "IS_SENT_START", "LOWER", "OP", "ORTH", "POS", "REGEX", "TAG"
)

__all__ = [
  "normalize", "uniq", "fix_grammar",
  "get_nlp", "ver1", "noun", "propn", "verb",
]

def normalize(text: str, pipechar: str = ".") -> str:
  # Correct separators for grammar
  text = text.replace("：", ": ")
  text = re.sub(r"\s+[•|]+\s+", f" {pipechar} ", text)
  text = re.sub(r"\s+/{2,}\s+", " . ", text)
  # Phone indicators
  text = re.sub(r"(📞|☎️|📱|☎)\s*:?\s*", "Phone: ", text, flags=re.UNICODE)
  # Drop "etc" in Japanese – e.g handle "Salesforceなど"
  text = text.replace("など", "")
   # Drop emojis
  text = replace_emoji(text, "!")
  # Drop sudo-emojis like ":snowflake:" which might overlap with skills
  text = re.sub(r":[-\w]+:", "!", text)
  # Workaround FPs for URLs – cases like "next.js/nuxt"
  text = re.sub(r"(\.js)/(?=\w)", r"\1 / ", text, flags=re.IGNORECASE)
  # Workarounds for C# and C++ joined with separators
  text = re.sub(r"(?<!\w)(c(?:\+\+|#))([,/])(?=\w)", sep_splitter, text, flags=re.IGNORECASE)
  # Strip the whitespace
  text = text.strip()
  # Add the trailing dot
  text = re.sub(r"(?<=\w)$", " .", text)
  # Collapse whitespace
  text = re.sub(r"\s+", " ", text)
  return text

def sep_splitter(match: re.Match[str]) -> str:
  word, sep = match.group(1), match.group(2)
  return (
    word + f"{sep} " if sep in {","} else
    word + f" {sep} "
  )

def uniq[T](arr: list[T] | Generator[str, Any, Any]) -> list[T]:
  """
  Order-preserving uniq
  """
  # Note: does not collapse "+NNN" with "NNN" so far
  d = {}
  for x in arr:
    d[x] = 1
  keys = cast(Iterable[T], d.keys()) # Looks like MyPy (or something) is improperly typing this
  return list(keys)

# --------------------------------------------------------------------------------------------------
# Invalid grammar, especially punctuation, ruins Spacy analysis. I've found that
# it's much easier to fix common errors preventively, than to fight them post-factum.
# --------------------------------------------------------------------------------------------------

LB = r"(?<!\w)"
RB = r"(?!\w)"

GRAMMAR_FIXES: list[tuple[str, str, re.RegexFlag | int]] = [
  (rf"{LB}free[-\s]+lanc([edring]*){RB}", r"freelanc\1", re.IGNORECASE),
  (rf"{LB}B\.?[sS]\.?[cC]?\.?|S[cC]?\.?[bB]\.?{RB}", r"B.S", 0), # B.S  = Bachelor of Science
  (rf"{LB}M\.?[sS]\.?[cC]?\.?|S[cC]\.?[mM]\.?{RB}", r"M.S", 0),  # M.S  = Master of Science (not handling "SM" forms for now)
  (rf"{LB}P\.?[hH]\.?[dD]?\.?{RB}", r"Ph.D", 0),                 # Ph.D = Doctor of Philosophy
  (r" @ ", r" at ", 0),
  # (r"wanna be", r"wannabe", re.IGNORECASE),
  # (r"engineer student", r"engineering student", re.IGNORECASE),
  # ...
  # TODO devops, mlops, sec-ops (insane number of varieties here)
]
GRAMMAR_FIXES = [
  (pattern, replacement, flags)
  for (pattern, replacement, flags) in GRAMMAR_FIXES
]

def fix_grammar(text: str) -> str:
  for pattern, replacement, flags in GRAMMAR_FIXES:
    text = re.sub(pattern, replacement, text, count=0, flags=flags)
  return text

nnp = {TAG: "NNP", POS: "PROPN"}
jj = {TAG: "JJ", POS: "ADJ"}

def add_dev_exceptions(nlp: Language) -> None:
  # Covers most common cases (ideally, we should retrain the model)
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  problematic = ["Go", "Lit", "Next", "Node", "React", "REST"]
  # "foo Go. bar Next"
  ruler.add([
    [{ORTH: orth, IS_SENT_START: False}]
    for orth in problematic
  ], {TAG: "NNP", POS: "PROPN"}, index=0)
  # "#go, #node, #next"
  ruler.add([
    [{ORTH: "#"}, {LOWER: orth.lower()}]
    for orth in problematic
  ], {TAG: "NNP", POS: "PROPN"}, index=1)
  # "; go,"
  ruler.add([
    [{IS_PUNCT: True}, {LOWER: orth.lower()}, {IS_PUNCT: True}]
    for orth in problematic
  ], {TAG: "NNP", POS: "PROPN"}, index=1)
  # e.g. "_/go"
  ruler.add([
    [{ORTH: "/"}, {LOWER: orth.lower()}]
    for orth in problematic
  ], {TAG: "NNP", POS: "PROPN"}, index=1)
  # e.g. "go/_"
  ruler.add([
    [{LOWER: orth.lower()}, {ORTH: "/"}]
    for orth in problematic
  ], {TAG: "NNP", POS: "PROPN"}, index=0)

def add_nnp_exceptions(nlp: Language, items: list[str]) -> None:
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 2:
      raise ValueError("NNP items with >= 2 spaces are not supported yet")
    elif spacecount == 1:
      w1, w2 = item.split(" ")
      pattern = [
        {LOWER: w1.lower()}, {LOWER: "-", OP: "?"}, {LOWER: w2.lower()},
      ]
      ruler.add([pattern], nnp, index=0)
      ruler.add([pattern], nnp, index=1)
    else:
      pattern = [
        {LOWER: item.lower()}
      ]
      ruler.add([pattern], nnp)

def add_jj_exceptions(nlp: Language, items: list[str]) -> None:
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 1:
      raise ValueError("JJ items with >= 1 spaces are not supported")
    else:
      pattern = [
        {LOWER: item.lower()}, {TAG: {IN: ["NN", "CD"]}}
      ]
      ruler.add([pattern], jj)

def add_jj_exceptions2(nlp: Language, items: list[str]) -> None:
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 1:
      raise ValueError("VBG items with >= 1 spaces are not supported")
    else:
      pattern = [
        {TAG: {IN: ["VBG"]}}, {LOWER: item.lower()},
      ]
      ruler.add([pattern], jj, index=1)

def get_nlp(name: str | Path = "en_core_web_sm") -> Language:
  nlp = spacy.load(name, exclude=["lemmatizer", "ner"])
  # nlp.add_pipe("index_tokens_by_sents", after="parser")
  # ^ can't add here as we sometimes merge ENT tokens

  prefixes = list(nlp.Defaults.prefixes or [])
  prefixes.append(r"[-=/(](?=[a-zA-Z(])")
  prefix_regex = spacy.util.compile_prefix_regex(prefixes)
  nlp.tokenizer.prefix_search = prefix_regex.search # type: ignore

  suffixes = list(nlp.Defaults.suffixes or [])
  suffixes.append(r"(?<=[a-zA-Z)])[-=/.)]")
  suffixes = [
    # Slice "#" when "#" if not preceded by r"[cC]" (except when it's like r"\w[cC]")
    suffix if suffix != "#" else r"(?<!\W[cC])#"
    # Note: r"^[cC]#" cases are covered separately, by token_match
    for suffix in suffixes
  ]
  suffix_regex = spacy.util.compile_suffix_regex(suffixes)
  nlp.tokenizer.suffix_search = suffix_regex.search # type: ignore

  # Tokenizer exceptions (sometimes are applied after prefix/suffix, sometimes before – wtf)
  def token_match(token: str) -> bool | None:
    lower = token.lower()
    if lower in {"c+", "c++", "c#", ".net", "ex.", "ph.d"}:
      return True
    # For cases like "@foo-bar" to keep it together
    if lower.startswith(("@",)):
      return True
    if lower.endswith((".js", ".py", ".net")) and (lower.count(".") == 1) and ("/" not in lower):
      return True
    return False
  nlp.tokenizer.token_match = token_match # type: ignore

  infixes = list(nlp.Defaults.infixes or [])
  infixes.append(r"(?<=[a-zA-Z)])[&+()](?=[a-zA-Z(])") # /
  infix_finditer = spacy.util.compile_infix_regex(infixes)
  nlp.tokenizer.infix_finditer = infix_finditer.finditer # type: ignore

  # Make the following PROPER NOUNs
  add_dev_exceptions(nlp)
  add_nnp_exceptions(nlp, [
    "deep learning", "machine learning",
  ])
  add_jj_exceptions(nlp, [
    # Make the following ADJECTIVEs if before NOUNs
    "graduate", "graduated",
    "undergraduate", "undergraduated",
    "learning", "aspiring",
  ])
  add_jj_exceptions2(nlp, [
    # Make the following ADJECTIVEs if after VERBs
    "leading",
  ])
  return nlp

@Language.factory("index_tokens_by_sents")
def component(nlp: Language, name: str) -> Callable[[Doc], Doc]:
  del nlp, name
  def index_tokens_by_sents(doc: Doc) -> Doc:
    for token in doc:
      token._.i = token.i - token.sent.start
    return doc
  return index_tokens_by_sents

def hash_skillname(text: str) -> str:
  return hashlib.md5(text.encode()).hexdigest()[:12]

type Pattern = list[dict[str, Any]]

def ver1(word: str) -> Pattern:
  return [
    {LOWER: {REGEX: r"^" + word + r"[-\d.]{0,4}$"}}
  ]

def literal(word: str) -> Pattern:
  # TODO support spaces and other punct
  return [
    {ORTH: word}
  ]

def noun(word: str) -> Pattern:
  poss = ["NOUN", "PROPN", "ADJ"]
  if re.search(r"[A-Z]", word):
    return [
      {ORTH: word, POS: {IN: poss}}
    ]
  else:
    return [
      {LOWER: word, POS: {IN: poss}}
    ]

def propn(word: str) -> Pattern:
  poss = ["PROPN"]
  if re.search(r"[A-Z]", word):
    return [
      {ORTH: word, POS: {IN: poss}}
    ]
  else:
    return [
      {LOWER: word, POS: {IN: poss}}
    ]

def verb(word: str) -> Pattern:
  poss = ["VERB"]
  if re.search(r"[A-Z]", word):
    return [
      {ORTH: word, POS: {IN: poss}}
    ]
  else:
    return [
      {LOWER: word, POS: {IN: poss}}
    ]

def get_prec_tokens(token: Token) -> list[Token]:
  return list(token.doc[token.sent.start : token.i])

def get_prec_words(token: Token) -> list[Token]:
  return [token for token in token.doc[token.sent.start : token.i] if is_word(token)]

def get_cons_tokens(token: Token) -> list[Token]:
  return list(token.doc[token.i+1 : token.sent.end])

def get_cons_words(token: Token) -> list[Token]:
  return [token for token in token.doc[token.i+1 : token.sent.end] if is_word(token)]

def get_heads(_token: Token) -> list[Token]:
  token = _token
  tokens: list[Token] = []
  while token != token.head:
    token = token.head
    tokens.append(token)
  return tokens

def get_cons_heads(_token: Token) -> list[Token]:
  token = _token
  tokens: list[Token] = []
  while token != token.head:
    token = token.head
    if token.i > _token.i:
      tokens.append(token)
  return tokens

def is_word(token: Token) -> bool:
  return not token.is_punct and not token.is_space

def get_root(sent: Span) -> Token | None:
  for token in sent:
    if token.dep_ == "ROOT":
      return token
  return None
