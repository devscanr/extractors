from pprint import pprint

from spacy import Language
from spacy.tokens import Doc, Token
from typing import Callable, Sequence
from ..extractor import BaseExtractor
from ..utils import uniq
from .skill import Skill

type Resolve = Callable[[Token], list[str]]

def create_resolve(ss: list[str]) -> Resolve:
  return lambda _: ss

class SkillExtractor(BaseExtractor):
  def __init__(self, nlp: Language, skills: Sequence[Skill]):
    super().__init__(nlp, skills)
    self.resolvers: dict[str, Resolve] = {}
    self.init_matchers2(skills)

  def init_matchers2(self, skills: Sequence[Skill]) -> None:
    for skill in skills:
      # Update resolve fns
      if skill.resolve is not None:
        assert skill.name not in self.resolvers, f"duplicate `resolve` at {skill.name!r}"
        self.resolvers[skill.name] = create_resolve(skill.resolve) if isinstance(skill.resolve, list) else skill.resolve

  def extract_many(self, text_or_docs: Sequence[str | Doc]) -> list[list[str]]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc) for doc in docs]

  def extract(self, text_or_doc: str | Doc) -> list[str]:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # pprint(list(self.nlp.tokenizer.explain(text_or_doc)))
    # pprint([{
    #   "token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc
    # ]) # if not tok.is_punct
    tmatches, _ = self.find_tmatches(doc)
    tmatches = self.filter_main(tmatches)
    # Resolve skills
    skills: list[str] = []
    for skill, [token] in tmatches:
      if skill in self.resolvers:
        skills += self.resolvers[skill](token)
      else:
        skills.append(skill)
    # Uniquelize skills
    return uniq(skills)
