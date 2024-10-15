from dataclasses import dataclass
from spacy.language import Language
from spacy.tokens import Doc
from typing import Iterable
from .freelancer import FreelancerParser
from .lead import LeadParser
from .nondev import NondevParser
from .student import StudentParser

__all__ = ["Categorized", "Categorizer"]

@dataclass
class Categorized:
  is_freelancer: bool
  is_lead: bool
  is_nondev: bool
  is_student: bool

class Categorizer:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp
    self.frparser = FreelancerParser(self.nlp)
    self.ldparser = LeadParser(self.nlp)
    self.ndparser = NondevParser(self.nlp)
    self.stparser = StudentParser(self.nlp)

  def categorize(self, ntexts: Iterable[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(ntexts)
    return [
      Categorized(
        is_freelancer = self.frparser.is_freelancer(doc) or False,
        is_lead = self.ldparser.is_lead(doc) or False,
        is_nondev = self.ndparser.is_nondev(doc) or False,
        is_student = self.stparser.is_student(doc) or False,
      ) for doc in docs
    ]
