import re
from spacy.tokens import Doc, Token
from ..extractor import BaseExtractor, TMatch
from .experience import is_OtherExperienceKind
from .experience import Experience
from ..spacyhelpers import token_level
from ..utils import uniq3

class ExperienceExtractor(BaseExtractor):
  # def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[Categorized]:
  #   if not text_or_docs:
  #     return []
  #   docs = self.nlp.pipe(text_or_docs) if isinstance(text_or_docs[0], str) else text_or_docs
  #   # LATER: `n_process` for multiprocessing
  #   return [self.extract(doc) for doc in docs]

  def find_tmatches(self, doc: Doc) -> tuple[list[TMatch], list[TMatch]]:
    tmatches, tunmatches = super().find_tmatches(doc)
    # This is currently the only precedent where we have intersecting patterns with the same name
    # of the same length. Example: "senior block engineer" matches on [0,1] and [1,2]
    # I'm not currently sure about a universal behavior in such cases. Here we merge matches into
    # a single match – sounds as a resonable thing to do generally. E.g. for skills we could match:
    # "foo bar baz" as "foo bar" (FooBarBaz) and "bar bazzz" (FooBarBaz)...
    # Would we generally want to continue with the full match instead of two partial matches? Probably yes.
    # I'm not so sure about ALL disjoint matches though.
    # OMG, do we need to perform the same crap for unmatches?! @_@
    # ---
    # Merge overlapping spans
    _tmatches = merge_overlapping([
      (match[0], set(t.i for t in match[1]))
      for match in tmatches
    ])
    # Restore sorted tokens
    tmatches2 = [(
      _tmatch[0],                                 # name
      ts := [doc[o] for o in sorted(_tmatch[1])], # tokens
      min(ts, key=lambda t: token_level(t))       # maintoken
    ) for _tmatch in _tmatches]
    # Restore the overall order
    tmatches2.sort(key=lambda m: m[2].i)
    return tmatches2, tunmatches

  def extract(self, text_or_doc: str | Doc) -> list[Experience]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{
    #   "token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head}
    #   for tok in doc # if not tok.is_punct
    # ])

    tmatches, _ = self.find_tmatches(doc)
    tmatches = uniq3(tmatches)
    # print("tmatches:", tmatches)

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

  def parse_oe(self, tagname: str, _tokens: list[Token]) -> Experience | None:
    # TODO search "over", handle Middle+ or Middle-Senior
    if is_OtherExperienceKind(tagname):
      return Experience(tagname)
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

type M = tuple[str, set[int]]

def merge_overlapping(matches: list[M]) -> list[M]:
  """
  assert merge_overlapping([
    ("PHP", {1, 2}),
    ("PHP", {1, 3}),
    ("SQL", {1}),
    ("PHP", {4, 5}),
    ("PHP", {1, 2, 3}),
  ]) == [('PHP', {1, 2, 3}), ('SQL', {1}), ('PHP', {4, 5})]
  """
  rs: list[M] = []
  for k, (name, offsets) in enumerate(matches):
    for l, (other_name, other_offsets) in enumerate(matches):
      if k != l:
        if name == other_name and offsets & other_offsets:
          ms = [(name, offsets | other_offsets)]
          ms.extend(match for m, match in enumerate(matches) if m != k and m != l)
          return merge_overlapping(ms)
    rs.append((name, offsets))
  if rs == matches:
    return matches
  else:
    return merge_overlapping(rs)
