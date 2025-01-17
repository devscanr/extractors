from dataclasses import dataclass
import re
from spacy import Language
from spacy.matcher import DependencyMatcher, Matcher, PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Any, Callable, Sequence, cast
from .ppatterns import to_ppatterns
from .spacyhelpers import token_level
from .utils import hash_skillname, uniq3
from .dpatterns import DPattern, separate_dphantoms, to_dpatterns2
from .xpatterns import XPattern, literal

type OMatch = tuple[str, list[int]]          # Matched tag with corresponding offsets
type TMatch = tuple[str, list[Token], Token] # Matched tag with corresponding tokens and the determined main token
type Disambiguate = Callable[[Token], bool]

@dataclass
class Tag:
  name: str
  phrases: list[
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
          if "<" in phrase or ">" in phrase:
            assert "-" not in phrase, f"Dashes are not supported yet with dep. operations: {phrase!r}"
            assert " " not in phrase, f"Spaces are not supported yet with dep. operations: {phrase!r}"
            dpatterns = to_dpatterns2([phrase])
            for k, dpattern in enumerate(dpatterns):
              dpattern, dphantoms = separate_dphantoms(dpattern)
              if dphantoms:
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
            self.dmatcher.add(mname, [phrase])
          else:
            self.xmatcher.add(mname, [phrase])

  def find_raw_omatches(self, doc: Doc) -> list[OMatch]:
    raw_omatches: list[OMatch] = []
    xmatches = self.xmatcher(doc) if len(self.xmatcher) else []
    pmatches = self.pmatcher(doc) if len(self.pmatcher) else []
    dmatches = self.dmatcher(doc) if len(self.dmatcher) else []
    for pmatch in pmatches:
      # print("pmatch:", pmatch)
      [match_id, start, end] = pmatch
      tag = self.nlp.vocab.strings[match_id]
      raw_omatches.append((tag, list(range(start, end))))
    for xmatch in xmatches:
      # print("xmatch:", xmatch)
      [match_id, start, end] = xmatch
      tag = self.nlp.vocab.strings[match_id]
      raw_omatches.append((tag, list(range(start, end))))
    for dmatch in dmatches:
      # print("dmatch:", dmatch)
      [match_id, offsets] = dmatch
      offsets = sorted(offsets)
      pname = self.nlp.vocab.strings[match_id]
      if pname in self.phantoms:
        offsets = [o for o in offsets if o not in self.phantoms[pname]]
      mname = detach_phantom(pname) # Can still contain ":maybe"...
      raw_omatches.append((mname, offsets))
    # DMatcher often produces duplicates (graph-based pattern)
    raw_omatches = uniq3(raw_omatches)
    # print("raw_omatches:", raw_omatches)
    return raw_omatches

  def find_omatches(self, doc: Doc) -> list[OMatch]:
    raw_omatches = self.find_raw_omatches(doc)
    omatches: list[OMatch] = []
    for mname, offsets in raw_omatches:
      name = detach_maybe(mname)
      other_matches: list[tuple[str, list[int]]] = []
      for mnam, ofs in raw_omatches:
        if ofs == offsets and detach_maybe(mnam) != name:
          raise Exception(f"tags {mname!r} and {mnam!r} overlap at {offsets!r}")
        elif not (mname == mnam and offsets == ofs):
          other_matches.append((mnam, ofs))
      if not any(
        self.should_ignore((mname, offsets), other_match)
        for other_match in other_matches
      ):
        omatches.append((mname, offsets))
    # print("omatches:", omatches)
    return omatches

  def find_tmatches(self, doc: Doc) -> tuple[list[TMatch], list[TMatch]]:
    omatches = self.find_omatches(doc)
    tmatches: list[TMatch] = []
    tunmatches: list[TMatch] = []
    for mname, offsets in omatches:
      tokens = [doc[offset] for offset in offsets]
      maintoken = min(tokens, key=lambda t: token_level(t)) # not sure about this part...
      name = detach_maybe(mname)
      if name == mname:
        if name.startswith("-"):
          tunmatches.append((name, tokens, maintoken))
        else:
          tmatches.append((name, tokens, maintoken))
      else:
        if name.startswith("-"):
          raise Exception("disambiguation for negations is not supported yet")
        assert mname in self.disambiguates # TEMP
        if any(disambiguate(maintoken) for disambiguate in self.disambiguates[mname]):
          tmatches.append((name, tokens, maintoken))
    tmatches.sort(key=lambda m: m[2].i)
    tunmatches.sort(key=lambda m: m[2].i)
    # print("tmatches:", tmatches)
    # print("tunmatches:", tunmatches)
    return tmatches, tunmatches

  def should_ignore(self, match: OMatch, other_match: OMatch) -> bool:
    mname, offsets = match
    other_mname, other_offsets = other_match
    name, other_name = detach_maybe(mname), detach_maybe(other_mname)
    exclusive, other_exclusive = self.exclusives[name], self.exclusives[other_name]
    if name != mname and name == other_mname:
      # Other match of the same tag disambiguates this match
      return True
    if set(offsets) & set(other_offsets):
      if other_mname in {"-", "-" + name}:
        # Found a canceling match
        return True
      if exclusive and other_exclusive:
        # Found a wider match
        return set(offsets) < set(other_offsets)
    return False

def attach_maybe(name: str) -> str:
  return name + ":maybe:" + hash_skillname(name)

def attach_phantom(name: str, k: int) -> str:
  return name + f":ph{k}"

def detach_maybe(mname: str) -> str:
  name = re.sub(r":maybe:.+(?=$|:)", "", mname)
  return name

def detach_phantom(pname: str) -> str:
  name = re.sub(r":ph\d+(?=$|:)", "", pname)
  return name

def is_semanticparent(name: str, other_name: str) -> bool:
  # print("@ is_semanticparent", name, other_name)
  # "Science" is a superterm of "Computer-Science" (sub-pattern syntactically)
  return re.search(rf"(?<!\w){name}(?!\w)", other_name, re.IGNORECASE) is not None

# @ is_superterm SQL MS-SQLServer
