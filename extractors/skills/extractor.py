import re
from spacy import Language
from spacy.matcher import DependencyMatcher, Matcher, PhraseMatcher
from spacy.tokens import Doc
from typing import Sequence
from ..patterns import expand_phrase12, expand_phrase2, to_deppatterns
from ..spacyhelpers import token_level
from ..utils import Pattern, literal, uniq
from .data import SKILLS
from .utils import Disambiguate, Resolve, Skill, label, unlabel

def create_resolve(ss: list[str]) -> Resolve:
  return lambda _: ss

class SkillExtractor:
  def __init__(self, nlp: Language) -> None:
    self.descrs: dict[str, str] = {}
    self.disambiguates: dict[str, list[Disambiguate]] = {}
    self.resolvers: dict[str, Resolve] = {}
    self.nlp = nlp
    self.matcher = Matcher(self.nlp.vocab)                      # matcher: single word, more verbose syntax than PM but less verbose than DM
    self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER") # phrases: fastest, no flexibility
    self.dmatcher = DependencyMatcher(self.nlp.vocab)           # dependency matcher: strictly 2 words
    self.init_matchers(SKILLS)

  def init_matchers(self, skills: list[Skill]) -> None:
    for skill in skills:
      key = label(skill)
      # Update descriptions
      if skill.descr is not None:
        assert skill.name not in self.descrs, f"duplicate `descr` at {skill.name!r}"
        self.descrs[skill.name] = skill.descr
      # Update disambiguate fns
      if skill.disambiguate is not None:
        assert key not in self.disambiguates, f"duplicate `disambiguate` at {skill.name!r}"
        self.disambiguates[key] = (
          skill.disambiguate if isinstance(skill.disambiguate, list) else [skill.disambiguate]
        )
      # Update resolve fns
      if skill.resolve is not None:
        assert skill.name not in self.resolvers, f"duplicate `resolve` at {skill.name!r}"
        self.resolvers[skill.name] = create_resolve(skill.resolve) if isinstance(skill.resolve, list) else skill.resolve
      # Update matchers with patterns
      for phrase in skill.phrases:
        if isinstance(phrase, str):
          if "<<" in phrase:
            # Uppercase is supported in `to_deppatterns`
            self.dmatcher.add(key, expand2_to_deppatterns(phrase))
          else:
            if re.search("[A-Z]", phrase):
              self.matcher.add(key, [literal(p) for p in expand_phrase12(phrase)])
            else:
              self.pmatcher.add(key, [self.nlp(p) for p in expand_phrase12(phrase)])
        elif isinstance(phrase, list):
          self.matcher.add(key, [phrase])

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[list[str]]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # print("Debug deps:", [{"token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc if not tok.is_punct])

    raw_matches: list[tuple[str, list[int]]] = []
    matches = self.matcher(doc) if len(self.matcher) else []
    pmatches = self.pmatcher(doc) if len(self.pmatcher) else []
    dmatches = self.dmatcher(doc) if len(self.dmatcher) else []
    for match in matches:
      # print("match:", match)
      [match_id, start, end] = match # e.g. "hardware" -> (10100372000430808166, 3, 4)
      skill = self.nlp.vocab.strings[match_id]
      raw_matches.append((skill, list(range(start, end))))
    for pmatch in pmatches:
      # print("pmatch:", pmatch)
      [match_id, start, end] = pmatch # e.g. "hardware-designer" -> (10100372000430808166, 3, 6)
      skill = self.nlp.vocab.strings[match_id]
      raw_matches.append((skill, list(range(start, end))))
    for dmatch in dmatches:
      [match_id, offsets] = dmatch # e.g. "hardware << design" -> (10100372000430808166, [4, 2])
      offsets = offsets if len(offsets) < 3 else [offsets[0], offsets[-1]]
      # We currently support << for word pairs, exclusively. Hence middle token, if present, is auxiliary.
      skill = self.nlp.vocab.strings[match_id]
      raw_matches.append((skill, offsets)) # offsets are (modifier=4) <- (anchor=2)
    # print("raw_matches:", raw_matches)

    # Resolve overriding matches
    distinct_matches: list[tuple[str, list[int]]] = []
    for skill, offsets in raw_matches:
      assumed_skill = unlabel(skill)
      is_certain = skill == assumed_skill
      other_matches: list[tuple[str, list[int]]] = []
      for sk, ofs in raw_matches:
        if ofs == offsets and unlabel(sk) != assumed_skill:
          raise Exception(f"skills {skill!r} and {sk!r} overlap at {offsets!r}")
        else:
          other_matches.append((sk, ofs))
      if not any(
        True for other_match in other_matches
        # Wider or a non-maybe alternative exists
        if set(offsets) < set(other_match[1]) or
           not is_certain and other_match[0] == assumed_skill
      ):
        distinct_matches.append((skill, offsets))
    # print("distinct_matches:", distinct_matches)

    # Disambiguate skills
    skill_matches: list[tuple[str, list[int]]] = []
    for skill, offsets in distinct_matches:
      root = doc[min(offsets, key=lambda o: token_level(doc[o]))]
      if ":maybe:" not in skill:
        if not skill.startswith("-"):
          skill_matches.append((skill, offsets))
      elif any(disambiguate(root) for disambiguate in self.disambiguates[skill]):
        skill_matches.append((unlabel(skill), offsets))
    # print("skill_matches:", skill_matches)

    # Resolve skills
    skills: list[str] = []
    for skill, offsets in skill_matches:
      # No larger match exists, continue
      if skill in self.resolvers:
        token = doc[offsets[-1]] # latest offset is (anchor)
        skills += self.resolvers[skill](token)
        # print(f"Adding topics with resolvers ({self.resolvers[topic](token)})")
      else:
        skills.append(skill)
        # print("Adding topic without resolvers")
    # print("skill_matches:", skill_matches)

    # Uniquelize skills
    return uniq(skills)

def expand2_to_deppatterns(phrase: str) -> list[Pattern]:
  return [
    p2
    for p1 in expand_phrase2(phrase)
    for p2 in to_deppatterns(p1)
  ]
