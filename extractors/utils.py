from emoji import replace_emoji
import hashlib
from pathlib import Path
import re
import spacy
from spacy import Language
from spacy.tokens import Doc
from typing import Any, Callable, Generator, cast, Iterable

# RESOURCES
# - https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
# - https://corenlp.run/

(DEP, IN, IS_PUNCT, IS_SENT_START, LOWER, OP, ORTH, POS, REGEX, TAG) = (
  "DEP", "IN", "IS_PUNCT", "IS_SENT_START", "LOWER", "OP", "ORTH", "POS", "REGEX", "TAG"
)
(LEFT_ID, REL_OP, RIGHT_ID, RIGHT_ATTRS) = (
  "LEFT_ID", "REL_OP", "RIGHT_ID", "RIGHT_ATTRS"
)

__all__ = [
  "normalize", "uniq", "omit_parens",
  "fix_grammar",
  "get_nlp", "ver1", "noun", "propn", "verb",
  "Pattern", "LB", "RB",
  "orth", "lookslike",
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

def omit_parens(input: str) -> str:
  output = ""
  paren = 0
  for ch in input:
    if ch == "(":
      paren += 1
    elif ch == ")" and paren:
      paren -= 1
    elif not paren:
      output += ch
  return re.sub(r"\s+", " ", output)

# def get[T](seq: Sequence[T], offset: int) -> T | None:
#   try:
#     return seq[offset]
#   except Exception:
#     return None
#
# def get_prev[T](seq: Sequence[T], offset: int) -> T | None:
#   prev = get(seq, offset - 1)
#   return prev
#
# def get_next[T](seq: Sequence[T], offset: int) -> T | None:
#   next = get(seq, offset + 1)
#   return next
#
# def get_prevnext[T](seq: Sequence[T], offset: int) -> tuple[T | None, T | None]:
#   prev = get(seq, offset - 1)
#   next = get(seq, offset + 1)
#   return prev, next

# def prev_token(token: Token) -> Token | None:
#   sent = list(token.sent)
#   try:
#     return sent[token._.i - 1]
#   except Exception:
#     return None
#
# def next_token(token: Token) -> Token | None:
#   sent = list(token.sent)
#   try:
#     return sent[token._.i + 1]
#   except Exception:
#     return None

# def prev_next_tokens(token: Token) -> tuple[Token | None, Token | None]:
#   sent = list(token.sent)
#   prev, next = None, None
#   try: prev = sent[token._.i - 1]
#   except Exception: pass
#   try: next = sent[token._.i + 1]
#   except Exception: pass
#   return prev, next

# --------------------------------------------------------------------------------------------------
# Invalid grammar, especially punctuation, ruins Spacy analysis. I've found that
# it's much easier to fix common errors preventively, than to fight them post-factum.
# --------------------------------------------------------------------------------------------------

LB = r"(?<!\w)"
RB = r"(?!\w)"

GRAMMAR_FIXES: list[tuple[str, str, re.RegexFlag | int]] = [
  (rf"{LB}free[-\s]+lanc([edring]*){RB}", r"freelanc\1", re.IGNORECASE),
  (rf"{LB}B\.?S\.?C?\.?{RB}|{LB}SC?\.?B\.?{RB}", r"B.S", re.IGNORECASE), # B.S  = Bachelor of Science
  (rf"{LB}M\.?S\.?C?\.?{RB}|{LB}SC\.?M\.?{RB}", r"M.S", re.IGNORECASE),  # M.S  = Master of Science (not handling "SM" forms for now)
  (rf"{LB}P\.?H\.?D?\.?{RB}", r"Ph.D", re.IGNORECASE),                   # Ph.D = Doctor of Philosophy
  (rf"{LB}eng.{RB}", r"eng", re.IGNORECASE),
  (rf"{LB}ex\s*[-.]\s*(?=\w)", r"ex ", re.IGNORECASE),
  (r" @ ", r" at ", 0),
  (r" & ", r" and ", 0),
  (r"(?<=[\w\s])/co-founder", r" / co-founder", re.IGNORECASE),
  (r"(?<=[\w\s])/\.net", r" / .net", re.IGNORECASE),
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
  nlp = spacy.load(name, exclude=["ner"]) # "lemmatizer",
  nlp.add_pipe("index_tokens_by_sents", after="parser")

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
    if lower in {"c+", "c++", "c#", ".net", "ph.d"}:
      return True
    if lower.startswith("co-"):
      return True
    # For cases like "@foo-bar" to keep it together
    if lower.startswith(("@",)) and not lower.endswith((",", ".")):
      return True
    if lower.endswith((".js", ".py", ".net")) and (lower.count(".") == 1) and ("/" not in lower):
      return True
    return False
  nlp.tokenizer.token_match = token_match # type: ignore

  infixes = list(nlp.Defaults.infixes or [])
  infixes.append(r"(?<=[a-zA-Z)])[&+()/](?=[a-zA-Z(])")
  infix_finditer = spacy.util.compile_infix_regex(infixes)
  nlp.tokenizer.infix_finditer = infix_finditer.finditer # type: ignore

  # `add_special_case` is strictly case-sensitive :(
  # for abbr in ["Eng.", "eng.", "Ex.", "ex."]:
  #   nlp.tokenizer.add_special_case(abbr, [{ORTH: abbr}])
  # Affects sentence boundaries, unlike `token_match`

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

# TODO remove `_.used` extension if it's no longer necessary :)

def orth(phrase: str) -> dict[str, str]:
  return {ORTH: phrase} if re.search(r"[A-Z]", phrase) else {LOWER: phrase}

def lookslike(lower: str, patt: re.Pattern[str]) -> bool:
  for match in re.finditer(patt, lower):
    start, end = match.span()
    lb = (lower[start-1] if start > 0 else "", lower[start])
    rb = (lower[end-1], lower[end] if end < len(lower) else "")
    is_left_bounded = (
      not lb[0].isalpha() or
      lb[0].islower() and lb[1].isupper() or
      lb[0].isupper() and lb[1].islower()
    )
    is_right_bounded = (
      not rb[1].isalpha() or
      rb[0].islower() and rb[1].isupper() or
      rb[0].isupper() and rb[1].islower()
    )
    if is_left_bounded and is_right_bounded:
      return True
  return False
  # print(is_separated("amazon"), "-- Should be True")
  # print(is_separated("Amazon"), "-- Should be True")
  # print(is_separated("amazon-foo"), "-- Should be True")
  # print(is_separated("foo-amazon"), "-- Should be True")
  #
  # print(is_separated("amazonFoo"), "-- Should be True")
  # print(is_separated("barAmazon"), "-- Should be True")
  #
  # print(is_separated("amazon_foo"), "-- Should be True")
  # print(is_separated("bar_amazon"), "-- Should be True")
  #
  # print(is_separated("AMAZONFOO"), "-- Should be False")
  # print(is_separated("amazonfoo"), "-- Should be False")
  # print(is_separated("baramazon"), "-- Should be False")
  # print(is_separated("BARAMAZON"), "-- Should be False")
  # print(is_separated("zzz"), "-- Should be False")
