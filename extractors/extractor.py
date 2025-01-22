from dataclasses import dataclass
import re
from spacy import Language
from spacy.matcher import DependencyMatcher, Matcher, PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Any, Callable, NamedTuple, Sequence, cast
from .ppatterns import to_ppatterns
from .spacyhelpers import token_level
from .utils import hash_skillname, uniq3
from .dpatterns import DPattern, separate_dphantoms, separate_xphantoms, to_dpatterns2
from .xpatterns import XPattern, literal

class OMatch(NamedTuple):
  mname: str
  offsets: list[int]

class TMatch(NamedTuple):
  name: str
  tokens: list[Token]
  maintoken: Token

type Disambiguate = Callable[[Token], bool]

@dataclass
class Tag:
  name: str
  phrases: Sequence[
    str |      # Custom (converted to XPattern, DPattern or expanded)
    XPattern | # Matcher pattern
    DPattern   # DependencyMatcher pattern
  ]
  descr: str
  exclusive: bool
  disambiguate: Disambiguate | list[Disambiguate] | None
  @property
  def ambiguous(self) -> bool:
    return bool(self.disambiguate)

class BaseExtractor:
  """
  Custom alternative for entity recognition, since the latter is incompatible
  with `DependencyMatcher` and does not provide any disambiguation mechanics.
  """

  def __init__(self, nlp: Language, tags: Sequence[Tag]):
    self.nlp = nlp
    # == Simplicity -> Flexibility ==
    # PMatcher -> XMatcher -> DMatcher
    self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER") # fastest, direct phrases
    self.xmatcher = Matcher(self.nlp.vocab)                     # pattern-based
    self.dmatcher = DependencyMatcher(self.nlp.vocab)           # pattern-based+
    self.descrs: dict[str, str] = {}
    self.exclusives: dict[str, bool] = {}
    self.disambiguates: dict[str, list[Disambiguate]] = {}
    self.phantoms: dict[str, list[int]] = {}
    self.init_matchers(tags)

  def init_matchers(self, tags: Sequence[Tag]) -> None:
    for tag in tags:
      mname = attach_maybe(tag.name) if tag.ambiguous else tag.name
      # Update descriptions
      if tag.name not in self.descrs:
        self.descrs[tag.name] = tag.descr
      # Update exclusives
      assert (
        self.exclusives[tag.name] == tag.exclusive
        if tag.name in self.exclusives
        else True
      ), f"varying `exclusive` at {tag.name!r}"
      self.exclusives[tag.name] = tag.exclusive
      # Update disambiguate fns
      if tag.disambiguate is not None:
        assert mname not in self.disambiguates, f"duplicate `disambiguate` at {tag.name!r}"
        self.disambiguates[mname] = tag.disambiguate if isinstance(tag.disambiguate, list) else [tag.disambiguate]
      # Update matchers with patterns
      for phrase in tag.phrases:
        if isinstance(phrase, str):
          if "<" in phrase or (">" in phrase and not "->" in phrase): # hack
            assert "-" not in phrase, f"Dashes are not supported yet with dep. operations: {phrase!r}"
            assert " " not in phrase, f"Spaces are not supported yet with dep. operations: {phrase!r}"
            dpatterns = to_dpatterns2([phrase])
            for dpattern in dpatterns:
              dpattern, dphantoms = separate_dphantoms(dpattern)
              if dphantoms:
                k = len(self.phantoms) + 1
                pname = attach_phantom(mname, k)
                self.phantoms[pname] = dphantoms
                self.dmatcher.add(pname, [dpattern])
              else:
                self.dmatcher.add(mname, [dpattern])
          else:
            if re.search("[A-Z]", phrase):
              self.xmatcher.add(mname, [literal(p) for p in to_ppatterns([phrase])])
            else:
              pipe = cast(Any, self.nlp.tokenizer).pipe # `tokenizer.pipe` is untyped in Spacy @_@
              self.pmatcher.add(mname, list(pipe(to_ppatterns([phrase]))))
        elif isinstance(phrase, list) and len(phrase):
          if "RIGHT_ID" in phrase[0]:
            dpattern, dphantoms = separate_dphantoms(phrase)
            # print("dpattern:", dpattern)
            if dphantoms:
              k = len(self.phantoms) + 1
              pname = attach_phantom(mname, k)
              self.phantoms[pname] = dphantoms
              self.dmatcher.add(pname, [dpattern])
            else:
              self.dmatcher.add(mname, [dpattern])
          else:
            xpattern, xphantoms = separate_xphantoms(phrase)
            # print("xpattern:", xpattern)
            if xphantoms:
              k = len(self.phantoms) + 1
              pname = attach_phantom(mname, k)
              self.phantoms[pname] = xphantoms
              self.xmatcher.add(pname, [xpattern])
            else:
              self.xmatcher.add(mname, [xpattern])

  def find_raw_omatches(self, doc: Doc) -> list[OMatch]:
    """
    Find raw omatches deriving them from xmatches, pmatches, and dmatches
    """
    raw_omatches: list[OMatch] = []
    xmatches = self.xmatcher(doc) if len(self.xmatcher) else []
    pmatches = self.pmatcher(doc) if len(self.pmatcher) else []
    dmatches = self.dmatcher(doc) if len(self.dmatcher) else []
    for pmatch in pmatches:
      [match_id, start, end] = pmatch
      mname = self.nlp.vocab.strings[match_id]
      raw_omatches.append(OMatch(mname, list(range(start, end))))
    for xmatch in xmatches:
      [match_id, start, end] = xmatch
      offsets = list(range(start, end)) # global offsets
      pname = self.nlp.vocab.strings[match_id]
      if pname in self.phantoms:
        offsets = [offs for o, offs in enumerate(offsets) if o not in self.phantoms[pname]]
      mname = detach_phantom(pname) # Can still contain ":maybe"...
      raw_omatches.append(OMatch(mname, offsets))
    for dmatch in dmatches:
      [match_id, offsets] = dmatch # global offsets
      pname = self.nlp.vocab.strings[match_id]
      if pname in self.phantoms:
        offsets = [offs for o, offs in enumerate(offsets) if o not in self.phantoms[pname]]
      mname = detach_phantom(pname) # Can still contain ":maybe"...
      raw_omatches.append(OMatch(mname, offsets))
    # DMatcher often produces duplicates (graph-based pattern)
    raw_omatches = uniq3(raw_omatches)
    # print("raw_omatches:", raw_omatches)
    return raw_omatches

  def find_omatches(self, doc: Doc) -> list[OMatch]:
    """
    Reduce omatches to min. necessary, sort offsets
    == Algorithm to merge non-collapsible overlaps ==
    'Senior Frontend Developer' can match 'Senior Frontend' and 'Senior Developer' in which case
    we want to merge them and deal with a single match. It concerns only matching tagnames, of course.
    In case any of overlapping patterns is certain (non-maybe) – their union becomes certain.
    """
    raw_omatches = self.find_raw_omatches(doc)
    omatches: list[OMatch] = []
    for omatch in raw_omatches:
      name = detach_maybe(omatch)
      other_omatches: list[OMatch] = []
      for om in raw_omatches:
        if om.offsets == omatch.offsets and detach_maybe(om) != name:
          raise ValueError(f"tags {omatch.mname!r} and {om.mname!r} overlap at {omatch.offsets!r}")
        elif omatch != om: # (mname == mnam and offsets == ofs):
          other_omatches.append(om)
      if not any(self.should_ignore(omatch, other_omatch) for other_omatch in other_omatches):
        omatches.append(omatch)
    # print("omatches:", omatches)
    # Merge overlapping and neighboring sets of offsets (for the same tagname)
    _omatches = merge_overlapping([
      (omatch.mname, set(omatch.offsets))
      for omatch in omatches
    ])
    # Restore matches & sort their offsets
    omatches = [
      OMatch(mname, sorted(offsets))
      for mname, offsets in _omatches
    ]
    # print("omatches':", omatches)
    return omatches

  def find_tmatches(self, doc: Doc) -> tuple[list[TMatch], list[TMatch]]:
    """
    Convert omatches to tokens, disambiguate, split into tmatches & tunmatches, sort the results
    """
    omatches = self.find_omatches(doc)
    tmatches: list[TMatch] = []
    tunmatches: list[TMatch] = []
    for omatch in omatches:
      tokens = [doc[offset] for offset in omatch.offsets]
      maintoken = min(tokens, key=lambda t: token_level(t)) # not sure about this part...
      name = detach_maybe(omatch)
      if name == omatch.mname:
        if omatch.mname.startswith("-"):
          tunmatches.append(TMatch(name, tokens, maintoken))
        else:
          tmatches.append(TMatch(name, tokens, maintoken))
      else:
        if name.startswith("-"):
          raise ValueError("disambiguation for negations is not supported yet")
        assert omatch.mname in self.disambiguates # TEMP
        if any(disambiguate(maintoken) for disambiguate in self.disambiguates[omatch.mname]):
          tmatches.append(TMatch(name, tokens, maintoken))
    # Sort matches and unmatches
    tmatches.sort(key=lambda tm: tm.maintoken.i)
    tunmatches.sort(key=lambda tm: tm.maintoken.i)
    # print("tmatches:", tmatches)
    # print("tunmatches:", tunmatches)
    return tmatches, tunmatches

  def should_ignore(self, match: OMatch, other_match: OMatch) -> bool:
    mname, offsets = match
    other_mname, other_offsets = other_match
    name, other_name = detach_maybe(mname), detach_maybe(other_mname)
    exclusive, other_exclusive = self.exclusives[name], self.exclusives[other_name]
    if set(offsets) & set(other_offsets):
      if other_mname in {"-", "-" + name}:
        # Ignore because of an overlapping canceling match
        return True
      if is_maybe(mname) and not is_maybe(other_mname):
        # Ignore because of an overlapping non-maybe match
        return True
      if set(offsets) < set(other_offsets):
        # Ignore an exclusive match in case of another & wider exclusive match. Unless the reverse comparison is ignored
        return exclusive and other_exclusive and not(is_maybe(other_mname) and not is_maybe(mname))
    return False

def is_maybe(mname_or_omatch: str | OMatch) -> bool:
  mname = mname_or_omatch if isinstance(mname_or_omatch, str) else mname_or_omatch.mname
  return ":maybe:" in mname

def attach_maybe(name: str) -> str:
  return name + ":maybe:" + hash_skillname(name)

def detach_maybe(mname_or_omatch: str | OMatch) -> str:
  mname = mname_or_omatch if isinstance(mname_or_omatch, str) else mname_or_omatch.mname
  name = re.sub(r":maybe:.+(?=$|:)", "", mname)
  return name

# Phantoms (serve similar purpose to Regex lookaheads and lookbehinds – limit matches but aren't captured)
def attach_phantom(name: str, k: int) -> str:
  return name + f":ph{k}"

def detach_phantom(pname: str) -> str:
  name = re.sub(r":ph\d+(?=$|:)", "", pname)
  return name

type M = tuple[str, set[int]]

def merge_overlapping(matches: list[M]) -> list[M]:
  # Recursive solution, can be probably be rewritten in imperative `while (True)` style if necessary.
  """
  assert merge_overlapping([
    ("JS", {7}),
    ("Senior", {1, 2}),
    ("Senior", {1, 3}), # [senior fullstack] developer vs [senior] fullstack [developer]
    ("SQL", {1}),
    ("PHP", {4}),
    ("Senior", {1, 2, 3}),
  ]) == [("JS", {7}), ('Senior', {1, 2, 3}), ('SQL', {1}), ('PHP', {4})]
  """
  rs: list[M] = []
  for k, (mname, offsets) in enumerate(matches):
    name = detach_maybe(mname)
    for l, (other_mname, other_offsets) in enumerate(matches):
      if k != l:
        other_name = detach_maybe(other_mname)
        if name == other_name and (offsets & other_offsets or is_neighboring(offsets, other_offsets)):
          common_name = name if is_maybe(other_name) else other_name
          ms = [(common_name, offsets | other_offsets)]
          ms.extend(match for m, match in enumerate(matches) if m != k and m != l)
          return merge_overlapping(ms)
    rs.append((mname, offsets))
  if rs == matches:
    return matches
  else:
    return merge_overlapping(rs)

def is_neighboring(s1: set[int], s2: set[int]) -> bool:
  min1, min2 = min(s1), min(s2)
  max1, max2 = max(s1), max(s2)
  if abs(min1 - min2) == 1 or abs(max1 - max2) == 1:
    return True
  if abs(min1 - max2) == 1 or abs(max1 - min2) == 1:
    return True
  return False
