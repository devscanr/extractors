import re
from spacy.matcher import DependencyMatcher, Matcher, PhraseMatcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span
from typing import Any, cast, Sequence
from ..patterns import expand_phrase12, expand_phrase2, to_deppatterns
from ..spacyhelpers import token_level
from ..utils import get_nlp, hash_skillname, Pattern, uniq
from .data import SKILLS
from .utils import Disambiguate, Resolve, Skill, Topic, clean

def create_resolve(ss: list[str]) -> Resolve:
  return lambda _: ss

class SkillExtractor:
  def __init__(self, name: str = "en_core_web_sm") -> None:
    self.descrs: dict[str, str] = {}
    self.disambiguates: dict[str, list[Disambiguate]] = {}
    self.resolvers: dict[str, Resolve] = {}
    self.nlp = get_nlp(name)
    self.matcher = Matcher(self.nlp.vocab)                      # matcher: single word, more verbose syntax than PM but less verbose than DM
    self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER") # phrases: fastest, no flexibility
    self.dmatcher = DependencyMatcher(self.nlp.vocab) # dependency matcher: strictly 2 words
    skills: list[Skill] = []  # Terms, unambiguate
    mskills: list[Skill] = [] # Terms, ambiguate
    tskills: list[Skill] = [] # Topics, unambiguate or ambiguate
    for skill in SKILLS:
      if isinstance(skill, Topic):
        tskills.append(skill)
      else:
        is_mskill = skill.disambiguate is not None
        if is_mskill:
          mskills.append(skill)
        else:
          skills.append(skill)
    self.init_eruler("entity_ruler1", skills)
    self.init_eruler("entity_ruler2", mskills)
    self.init_matchers(tskills)

  def init_eruler(self, name: str, skills: list[Skill]) -> None:
    ruler: EntityRuler = cast(Any, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name=name))
    for skill in skills:
      # Update self.descrs
      if skill.descr is not None:
        # if skill.name in self.descrs:
        #   print(skill.name, skill.phrases, repr(skill.descr))
        assert skill.name not in self.descrs, f"duplicate `descr` at {skill.name!r}"
        self.descrs[skill.name] = skill.descr
      # Update self.disambiguates
      if skill.disambiguate is not None:
        l = label(skill)
        assert l not in self.disambiguates, f"duplicate `disambiguate` at {skill.name!r}"
        self.disambiguates[l] = (
          skill.disambiguate if isinstance(skill.disambiguate, list) else [skill.disambiguate]
        )
      # Update self.resolvers
      if skill.resolve is not None:
        assert skill.name not in self.resolvers, f"duplicate `resolve` at {skill.name!r}"
        self.resolvers[skill.name] = create_resolve(skill.resolve) if isinstance(skill.resolve, list) else skill.resolve
      # Update the ruler with patterns
      for phrase in skill.phrases:
        if isinstance(phrase, str):
          assert not re.search("[A-Z]", phrase), f"{phrase!r} contains uppercase character(s), use pattern syntax"
          ruler.add_patterns([{
            "label": label(skill),
            "pattern": pattern
          } for pattern in expand_phrase12(phrase)])
        elif isinstance(phrase, list):
          ruler.add_patterns([{
            "label": label(skill),
            "pattern": phrase
          }])
        else:
          raise Exception("not supported")

  def init_matchers(self, skills: list[Skill]) -> None:
    for skill in skills:
      # Update self.disambiguates
      if skill.disambiguate is not None:
        l = label(skill)
        assert l not in self.disambiguates, f"duplicate `disambiguate` at {skill.name!r}"
        self.disambiguates[l] = (
          skill.disambiguate if isinstance(skill.disambiguate, list) else [skill.disambiguate]
        )
      # Update self.resolvers
      if skill.resolve is not None:
        assert skill.name not in self.resolvers, f"duplicate `resolve` at {skill.name!r}"
        self.resolvers[skill.name] = create_resolve(skill.resolve) if isinstance(skill.resolve, list) else skill.resolve
      # Update the dep.matcher with patterns
      for phrase in skill.phrases:
        if isinstance(phrase, str):
          if "<<" in phrase:
            # Uppercase is supported in `to_deppatterns`
            self.dmatcher.add(label(skill), expand2_to_deppatterns(phrase))
          else:
            # attr=LOWER is global so the approach here is forcedly different :(
            assert not re.search("[A-Z]", phrase), f"{phrase!r} contains uppercase character(s), use pattern syntax"
            self.pmatcher.add(label(skill), [self.nlp(p) for p in expand_phrase12(phrase)])
        else:
          self.matcher.add(label(skill), [phrase])

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[list[str]]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # print("Debug tokens:", list(self.nlp.tokenizer.explain(text_or_doc)))
    # print("Debug poss:", list((tok, tok.pos_) for tok in doc if not tok.is_punct))
    # print("Debug deps:")
    # pprint([{"token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc if not tok.is_punct])
    # print("Debug ents:", list(ent.label_ for ent in doc.ents))

    # Disambiguate entities
    ents: list[Span] = []
    for ent in doc.ents:
      if ":maybe:" not in ent.label_:
        ents.append(ent)
      elif any(disambiguate(ent.root) for disambiguate in self.disambiguates[ent.label_]):
        ent.label_ = clean(ent.label_)
        ents.append(ent)
    doc.ents = ents
    # print("doc.ents:", doc.ents)

    # Resolve entities to terms, collect raw topic_matches
    terms: list[str] = []
    for ent in doc.ents:
      if ent.label_ in self.resolvers:
        terms += self.resolvers[ent.label_](ent.root)
      else:
        terms.append(ent.label_)
    # Note: in future we'll probably replace EntityRuler with custom search logic,
    #       as we already heavily rely on the latter!
    ################################################################################################
    # TODO drop entity recognition to not support 2 parallel mechanics
    topic_matches: list[tuple[str, list[int]]] = []
    matches = self.matcher(doc) if len(self.matcher) else []
    pmatches = self.pmatcher(doc) if len(self.pmatcher) else []
    dmatches = self.dmatcher(doc) if len(self.dmatcher) else []
    for match in matches:
      [match_id, start, end] = match # e.g. "hardware" -> (10100372000430808166, 3, 4)
      topic = self.nlp.vocab.strings[match_id]
      topic_matches.append((topic, list(range(start, end))))
    for pmatch in pmatches:
      [match_id, start, end] = pmatch # e.g. "hardware-designer" -> (10100372000430808166, 3, 6)
      topic = self.nlp.vocab.strings[match_id]
      topic_matches.append((topic, list(range(start, end))))
    for dmatch in dmatches:
      [match_id, offsets] = dmatch # e.g. "hardware << design" -> (10100372000430808166, [4, 2])
      offsets = offsets if len(offsets) < 3 else [offsets[0], offsets[-1]]
      # We currently support << for word pairs, exclusively. Hence middle token, if present, is auxiliary.
      topic = self.nlp.vocab.strings[match_id]
      topic_matches.append((topic, offsets)) # offsets are (modifier=4) <- (anchor=2)
    # Remove topic/entity and topic/topic overrides
    # print("topic_matches before filters", topic_matches)
    topic_matches2: list[tuple[str, list[int]]] = []
    for topic, offsets in topic_matches:
      if any(True for ent in doc.ents if doc[offsets[-1]] in ent):
        continue
      elif any(
         True for other_topic, other_offsets in topic_matches
         if (set(offsets) < set(other_offsets) if offsets != other_offsets else False)
       ):
        continue
      topic_matches2.append((topic, offsets))
    # print("topic_matches after filters", topic_matches2)
    # Disambiguate topics
    topic_matches3: list[tuple[str, list[int]]] = []
    for topic, offsets in topic_matches2:
      root = doc[min(offsets, key=lambda o: token_level(doc[o]))]
      if ":maybe:" not in topic:
        if not topic.startswith("-"): # "-" matches are preserved up to here (to correctly block shorter matches)
          topic_matches3.append((topic, offsets))
      elif any(disambiguate(root) for disambiguate in self.disambiguates[topic]):
        topic_matches3.append((clean(topic), offsets))
    # Resolve topic_matches to topics
    topics: list[str] = []
    for topic, offsets in topic_matches3:
      # No larger match exists, continue
      if topic in self.resolvers:
        token = doc[offsets[-1]] # latest offset is (anchor)
        topics += self.resolvers[topic](token)
        # print(f"Adding topics with resolvers ({self.resolvers[topic](token)})")
      else:
        topics.append(topic)
        # print("Adding topic without resolvers")
    return [
      skill for skill in uniq(terms + topics)
    ]

def label(skill: Skill) -> str:
  if skill.disambiguate:
    return skill.name + ":maybe:" + hash_skillname(skill.name)
  else:
    return skill.name

def expand2_to_deppatterns(phrase: str) -> list[Pattern]:
  return [
    p2
    for p1 in expand_phrase2(phrase)
    for p2 in to_deppatterns(p1)
  ]
