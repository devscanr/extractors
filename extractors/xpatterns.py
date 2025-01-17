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

# no IS_SENT_END in Spacy, can't define `singleton`
dep_root = {DEP: "ROOT"}
tag_nn = {TAG: "NN", POS: "NOUN"}
tag_nnp = {TAG: "NNP", POS: "PROPN"} # POS is kinda of duplicate but it's required for the "attribute_ruler"
tag_jj = {TAG: "JJ", POS: "ADJ"}     # /

def ver1(word: str) -> XPattern:
  return [
    {LOWER: {REGEX: r"^" + word + r"[-\d.]{0,4}$"}}
  ]

def noun(word: str) -> XPattern:
  return [
    orth_or_lower(word) | pos_nounlike()
  ]

def propn(word: str) -> XPattern:
  return [
    orth_or_lower(word) | {POS: {IN: ["PROPN"]}}
  ]

def verb(word: str) -> XPattern:
  return [
    orth_or_lower(word) | {POS: {IN: ["VERB"]}}
  ]

def literal(phrase: str) -> XPattern:
  return [
    {ORTH: word} for word in re.split(r"(?<=\W)(?=\w)|(?<=\w)(?=\W)", phrase)
    if word.strip()
  ]
