from emoji import replace_emoji
import hashlib
from pathlib import Path
import re
import spacy
from spacy import Language
from spacy.tokens import Doc
from typing import Any, Callable, cast, Iterable
from .xpatterns import DEP, HEAD, IN, IS_PUNCT, IS_SENT_START, LOWER, OP, ORTH, TAG, tag_jj, tag_nn, tag_nnp

# RESOURCES
# - https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
# - https://corenlp.run/

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
  # Strip decorations
  text = re.sub(r"(^[-~=\s]+)|([-~=#@\s]+$)", "", text)
  # Collapse whitespace
  text = re.sub(r"\s+", " ", text)
  # Ensure the trailing dot if necessary
  last_word = text.split(" ")[-1]
  if not last_word.endswith((".", "?", "!")) and not "." in last_word:
    text += "."
  # print(repr(text))
  return text

def sep_splitter(match: re.Match[str]) -> str:
  word, sep = match.group(1), match.group(2)
  return (
    word + f"{sep} " if sep in {","} else
    word + f" {sep} "
  )

# TODO rename to `uniq2` and add set-based `uniq1`. No `uniq` version to not forget the related quirks.
def uniq[T](itr: Iterable[T]) -> list[T]:
  """
  Order-preserving uniq. Does not support nested lists and other non-hashable item types.
  """
  arr = list(itr)
  d = {}
  for x in arr:
    d[x] = 1
  keys = cast(Iterable[T], d.keys()) # Looks like MyPy (or something) is improperly typing this
  return list(keys)

def uniq3[T](itr: Iterable[T]) -> list[T]:
  """
  Slower than the above. Supports nested lists and other non-hashable item types.
  """
  arr = list(itr)
  return [x for i, x in enumerate(arr) if arr.index(x) == i]

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
  (rf"{LB}eng\.{RB}", r"eng", re.IGNORECASE),
  (rf"{LB}ex\s*[-.]\s*(?=\w)", r"ex ", re.IGNORECASE),
  (rf"{LB}non\s*-\s*(?=\w)", r"non ", re.IGNORECASE),
  (r" @ ", r" at ", 0),
  (r" & ", r" and ", 0),
  (r"(?<=[\w\s])/co-founder", r" / co-founder", re.IGNORECASE),
  (r"(?<=[\w\s])/\.net", r" / .net", re.IGNORECASE),
]

def fix_grammar(text: str) -> str:
  for pattern, replacement, flags in GRAMMAR_FIXES:
    text = re.sub(pattern, replacement, text, count=0, flags=flags)
  return text

def add_dev_exceptions(nlp: Language) -> None:
  # Covers most common cases (ideally, we should retrain the model)
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  problematic = ["Go", "Lit", "Next", "Node", "React", "REST"]
  # "foo Go. bar Next"
  ruler.add([
    [{ORTH: orth, IS_SENT_START: False}]
    for orth in problematic
  ], tag_nnp, index=0)
  # "#go, #node, #next"
  ruler.add([
    [{ORTH: "#"}, {LOWER: orth.lower()}]
    for orth in problematic
  ], tag_nnp, index=1)
  # "; go,"
  ruler.add([
    [{IS_PUNCT: True}, {LOWER: orth.lower()}, {IS_PUNCT: True}]
    for orth in problematic
  ], tag_nnp, index=1)
  # e.g. "_/go"
  ruler.add([
    [{ORTH: "/"}, {LOWER: orth.lower()}]
    for orth in problematic
  ], tag_nnp, index=1)
  # e.g. "go/_"
  ruler.add([
    [{LOWER: orth.lower()}, {ORTH: "/"}]
    for orth in problematic
  ], tag_nnp, index=0)

def add_nnp_exceptions(nlp: Language, items: list[str]) -> None:
  # NN: Noun, singular or mass
  # NNP: Proper noun, singular Phrase
  # NNS: Noun, plural
  # NNPS: Proper noun, plural
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 2:
      raise ValueError("NNP items with >= 2 spaces are not supported yet")
    elif spacecount == 1:
      for caseditem in [item.lower(), item.upper(), item.title()]:
        w1, w2 = caseditem.split(" ")
        if caseditem.islower():
          patts = [[
            {LOWER: w1.lower()}, {ORTH: "-", OP: "?"}, {LOWER: w2.lower()},
          ]]
          ruler.add(patts, tag_nn | {HEAD: 1, DEP: "compound"}, index=0)
          ruler.add(patts, tag_nn, index=1)
        else:
          patts = [[
            {ORTH: w1.lower()}, {ORTH: "-", OP: "?"}, {ORTH: w2.lower()},
          ]]
          ruler.add(patts, tag_nnp | {HEAD: 1, DEP: "compound"}, index=0)
          ruler.add(patts, tag_nnp, index=1)
    else:
      for caseditem in [item.lower(), item.upper(), item.title()]:
        if caseditem.islower():
          ruler.add([[{LOWER: item.lower()}]], tag_nn)
        else:
          ruler.add([[{LOWER: item.lower()}]], tag_nnp)

def add_jj_exceptions(nlp: Language, items: list[str]) -> None:
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 1:
      raise ValueError("JJ items with >= 1 spaces are not supported")
    else:
      ruler.add([[
        {LOWER: item.lower()}, {TAG: {IN: ["NN", "CD"]}}
      ]], tag_jj)

def add_jj_exceptions2(nlp: Language, items: list[str]) -> None:
  ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  for item in items:
    spacecount = item.count(" ")
    if spacecount >= 1:
      raise ValueError("VBG items with >= 1 spaces are not supported")
    else:
      ruler.add([[
        {TAG: {IN: ["VBG"]}}, {LOWER: item.lower()},
      ]], tag_jj, index=1)

def add_new_exceptions(nlp: Language) -> None:
  pass
  # ruler = cast(Any, nlp.get_pipe("attribute_ruler"))
  # ruler.add([[
  #   {LOWER: "computer"}, {ORTH: "/"}, {LOWER: "data"},
  #   {LOWER: "science"},
  # ]], {HEAD: 3, DEP: "nmod"}, index=0)
  # ruler.add([[
  #   {LOWER: "data"}, {ORTH: "/"}, {LOWER: "computer"},
  #   {LOWER: "science"},
  # ]], {HEAD: 3, DEP: "nmod"}, index=0)

def get_nlp(name: str | Path = "en_core_web_sm") -> Language:
  nlp = spacy.load(name, exclude=["ner"]) # "lemmatizer",

  # Custom components
  nlp.add_pipe("index_tokens_by_sents", after="parser")

  # Prefixes
  prefixes = list(nlp.Defaults.prefixes or [])
  prefixes.append(r"[-=/(](?=[a-zA-Z(])")
  prefix_regex = spacy.util.compile_prefix_regex(prefixes)
  nlp.tokenizer.prefix_search = prefix_regex.search # type: ignore

  # Suffixes
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

  # Infixes
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
    "computer science", # fixing POS, TAG, DEP, HEAD
    "deep learning",
    "data science",
    "machine learning",
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
  add_new_exceptions(nlp)
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

# TODO remove `_.used` extension if it's no longer necessary :)

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

def includes[T](itr: Iterable[T], subitr: Iterable[T]) -> bool:
  arr, subarr = list(itr), list(subitr)
  la, ls = len(arr), len(list(subarr))
  if not la or not ls:
    return False
  for i in range(0, la):
    try:
      for j in range(0, ls):
        if arr[i + j] != subarr[j]:
          raise ValueError()
      return True
    except (IndexError, ValueError):
      pass
  return False
