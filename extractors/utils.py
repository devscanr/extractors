from emoji import replace_emoji
from pathlib import Path
import re
import spacy
from spacy import Language
from spacy.tokens import Doc, Token
from typing import Any, Callable, Generator, cast, Iterable

# RESOURCES
# - https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk

(IN, IS_PUNCT, IS_SENT_START, LOWER, OP, ORTH, POS, TAG) = ("IN", "IS_PUNCT", "IS_SENT_START", "LOWER", "OP", "ORTH", "POS", "TAG")

__all__ = [
  "normalize", "uniq", "fix_grammar",
  "get_nlp",
]

def normalize(text: str) -> str:
  text = text.replace("：", ": ")
  text = re.sub(r"\s+[•|]+\s+", " . ", text)
  text = re.sub(r"\s+/{2,}\s+", " . ", text)
  text = re.sub(r"(📞|☎️|📱|☎)\s*:?\s*", "Phone: ", text, flags=re.UNICODE)
  text = replace_emoji(text, "!")
  text = text.strip()
  text = re.sub(r"(?<=\w)$", " .", text)
  text = re.sub(r"\s+", " ", text)
  return text

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
  problematic = ["Go", "Next", "Node", "REST"]
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
  prefixes.extend(["-", "="])
  prefix_regex = spacy.util.compile_prefix_regex(prefixes)
  nlp.tokenizer.prefix_search = prefix_regex.search # type: ignore

  suffixes = list(nlp.Defaults.suffixes or [])
  suffixes.extend(["-", "="])
  suffix_regex = spacy.util.compile_suffix_regex(suffixes)
  nlp.tokenizer.suffix_search = suffix_regex.search # type: ignore

  infixes = list(nlp.Defaults.infixes or [])
  infixes.append(r"(?<=[a-zA-Z_])[(](?=[a-zA-Z_])")
  infixes.append(r"(?<=[#+a-zA-Z_])[,](?=[#+a-zA-Z_])")
  infixes.append(r"(?<=[a-zA-Z])[+](?=[a-zA-Z])")
  infix_finditer = spacy.util.compile_infix_regex(infixes)
  nlp.tokenizer.infix_finditer = infix_finditer.finditer # type: ignore

  # Tokenizer exceptions
  def token_match(token: str) -> bool | None:
    KNOWN_SUFFIXES = (".js", ".py")
    tokenl = token.lower()
    if tokenl in {"c#", "ex."} or tokenl.endswith(KNOWN_SUFFIXES):
      return True
    return False
  nlp.tokenizer.token_match = token_match # type: ignore

  nlp.tokenizer.add_special_case("ex.", [{ORTH: "ex."}]) # type: ignore
  # nlp.tokenizer.add_special_case("node.js", [{ORTH: "ex."}])

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
  if not Token.has_extension("i"):
    Token.set_extension("i", default=None)
  def index_tokens_by_sents(doc: Doc) -> Doc:
    for token in doc:
      token._.i = token.i - token.sent.start
    return doc
  return index_tokens_by_sents
