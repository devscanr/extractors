import re
from typing import Any

(DEP, HEAD, IN, IS_PUNCT, IS_SENT_START, LOWER, OP, ORTH, POS, REGEX, TAG, TEXT) = (
  "DEP", "HEAD", "IN", "IS_PUNCT", "IS_SENT_START", "LOWER", "OP", "ORTH", "POS",
  "REGEX", "TAG", "TEXT"
)

type XToken = dict[str, Any]
type XPattern = list[XToken]

def lower(word: str) -> XToken:
  return {LOWER: word}

def regex(word: str) -> XToken:
  return {TEXT: {REGEX: word}}

def orth_or_lower(word: str) -> XToken:
  return {ORTH: word} if re.search(r"[A-Z]", word) else {LOWER: word}

def pos_nounlike() -> XToken:
  return {POS: {IN: ["NOUN", "PROPN", "ADJ"]}}

def pos_propn() -> XToken:
  return {POS: {IN: ["PROPN"]}}

def pos_verb() -> XToken:
  return {POS: {IN: ["VERB"]}}

# no IS_SENT_END in Spacy, can't define `singleton`
dep_root = {DEP: "ROOT"}
tag_nn = {TAG: "NN", POS: "NOUN"}
tag_nnp = {TAG: "NNP", POS: "PROPN"} # POS is kinda of duplicate but it's required for the "attribute_ruler"
tag_jj = {TAG: "JJ", POS: "ADJ"}     # /

def ver1(word: str) -> XPattern:
  return [
    {LOWER: {REGEX: r"^" + word + r"[-\d.]{0,4}$"}}
  ]

def noun(word: str | None = None) -> XPattern:
  if not word:
    return [pos_nounlike()]
  return [
    orth_or_lower(word) | pos_nounlike()
  ]

def propn(word: str | None = None) -> XPattern:
  if not word:
    return [pos_propn()]
  return [
    orth_or_lower(word) | pos_propn()
  ]

def verb(word: str | None = None) -> XPattern:
  if not word:
    return [pos_verb()]
  return [
    orth_or_lower(word) | pos_verb()
  ]

def literal(phrase: str) -> XPattern:
  return [
    {ORTH: word} for word in re.split(r"(?<=\W)(?=\w)|(?<=\w)(?=\W)", phrase)
    if word.strip()
  ]
