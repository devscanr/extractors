from dataclasses import dataclass
from extractors.freelancer import FreelancerParser
from extractors.nondev import NondevParser
from extractors.student import StudentParser
from spacy.language import Language
from spacy.tokens import Doc
from typing import Iterable

__all__ = ["Categorized", "Categorizer"]

@dataclass
class Categorized:
  is_freelancer: bool | None
  is_nondev: bool | None
  is_student: bool | None

class Categorizer:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp
    self.freelancer_parser = FreelancerParser(self.nlp)
    self.nondev_parser = NondevParser(self.nlp)
    self.student_parser = StudentParser(self.nlp)

  def categorize(self, ntexts: Iterable[str | Doc]) -> list[Categorized]:
    docs = self.nlp.pipe(ntexts)
    return [
      Categorized(
        is_freelancer = self.freelancer_parser.is_freelancer(doc),
        is_nondev = self.nondev_parser.is_nondev(doc),
        is_student = self.student_parser.is_student(doc),
      ) for doc in docs
    ]
