# from pprint import pprint
import re
from spacy.tokens import Doc, Token
from ..extractor import BaseExtractor
from ..markers import is_future, is_negated
from .experience import is_OtherExperienceKind
from .experience import Experience

class ExperienceExtractor(BaseExtractor):
  # def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
  #   if not text_or_docs:
  #     return []
  #   docs = self.nlp.pipe(text_or_docs) if isinstance(text_or_docs[0], str) else text_or_docs
  #   # LATER: `n_process` for multiprocessing
  #   return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[Experience]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{
    #   "token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head}
    #   for tok in doc # if not tok.is_punct
    # ])
    tmatches, _ = self.find_tmatches(doc)
    # print("tmatches:", tmatches)

    # Filter negated and future matches
    tmatches = [
      (name, tokens, maintoken)
      for name, tokens, maintoken in tmatches
      if not any(pred(maintoken) for pred in [is_negated, is_future])
    ]
    # Extract experiences
    experiences: list[Experience] = []
    for name, tokens, _ in tmatches:
      if name in {"MOE", "YOE"}:
        exp = self.parse_ee(name, tokens)
      else:
        exp = self.parse_oe(name, tokens)
      if exp:
        experiences.append(exp)
    return experiences

  def parse_ee(self, tagname: str, tokens: list[Token]) -> Experience | None:
    sent = tokens[0].sent
    # Search for `over`
    over = any(
      tok.lower_ in {"+", "more", "over"} for tok in sent
      if tok not in tokens
      if tok.head in tokens or tok.head.head in tokens
    ) or any (
      "+" in tok.text for tok in tokens
    )
    # Search for numeric number
    numstrs = [
      tok.lower_ for tok in sent
      if tok not in tokens
      if (tok.head in tokens or tok.head.head in tokens)
      if re.fullmatch(r"\d+(\.\d+)?", tok.text)
    ]
    num = parse_numstr(numstrs[0]) if len(numstrs) == 1 else None
    if num is not None and num > 0:
      return Experience("Exact", months=num_to_months(tagname, num), over=over)
    # Search for textual number
    wnumstrs = [
      tok.lower_ for tok in sent
      if tok not in tokens
      if (tok.head in tokens or tok.head.head in tokens)
      if re.fullmatch(r"one\+?|two\+?|\+", tok.lower_)
    ]
    num = parse_wnumstr(wnumstrs[0]) if len(wnumstrs) == 1 else None
    if num is not None and num > 0:
      return Experience("Exact", months=num_to_months(tagname, num), over=over)
    return None

  def parse_oe(self, tagname: str, tokens: list[Token]) -> Experience | None:
    sent = tokens[0].sent
    # Search for `over`
    over = any(
      tok.lower_ in {"+"} for tok in sent
      if tok not in tokens
      if tok.head in tokens or tok.head.head in tokens
    ) or any (
      "+" in tok.text for tok in tokens
    )

    # TODO search "over", handle Middle+ or Middle-Senior
    if is_OtherExperienceKind(tagname):
      return Experience(tagname, over=over)
    return None

def parse_numstr(numstr: str) -> float | None:
  try:
    return float(numstr) if numstr else None
  except:
    return None

def parse_wnumstr(wnumstr: str) -> float | None:
  if wnumstr in WNUM_TO_NUM:
    return WNUM_TO_NUM[wnumstr]
  return None

def num_to_months(tagname: str, num: float) -> int:
  return round(num) if tagname == "MOE" else round(num * 12)

WNUM_TO_NUM = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4,
  "five": 5,
}
