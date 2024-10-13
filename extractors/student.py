from extractors.match import words_to_regex
import re
from spacy.language import Language
# from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Token
from typing import Iterable

__all__ = ["StudentParser"]

STUDENT_NOUNS = {
  "freshman",  # first-course
  "graduate",  # has a degree but often used as a shortening for "graduate student" which is someone who continues to learn
  "sophomore", # second-course
  "student",   # junior student (3rd), senior student (4th year), no universal term for 5th year
  "teenager",
  "undergraduate",
}
STUDENT_VERBS = {
  # Do not add "learn" or "study" words naively – lots of false positives
  "learning",
  "studying",
}
WEAK_NON_STUDENT_NOUNS = {
  # Mean a Non-Student only if sentence contains no STUDENT_NOUNS (these words can precede it)
  "B.S", "M.S", "Ph.D", "bachelor"
}
STRONG_NON_STUDENT_NOUNS = {
  # Non-included cases:
  #   intern -- does not mean a non-student
  #   pilot -- non-digital
  # Conflicts:
  #   MS - Mississippi State
  #   BC - British Columbia Province
  "admin", "analyst", "architect", "artist", "cto", "dean", "designer", "dev", "devops", "developer", "doctor",
  "engineer", "engineering", "eng", "entrepreneur",
  "founder", "generalist", "guru", "lawyer", "lead", "leader", "magician", "manager",
  "mathematician", "mechanic",
  "mlops", "musician", "ninja", "physicist", "producer", "professor", "programmer", "researcher",
  "recruiter", "scientist", "specialist", "vp",
  # hr
}
ASPIRING_SYNONIMS = {"aspiring", "future", "wannabe"}
ASPIRING_REGEX = words_to_regex(ASPIRING_SYNONIMS)
PERPETUAL_SYNONIMS = {"constant", "eternal", "everlasting", "life=long", "permanent", "perpetual"}
PERPETUAL_REGEX = words_to_regex(PERPETUAL_SYNONIMS)

class StudentParser:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp

  def are_students(self, ntexts: Iterable[str | Doc]) -> list[bool | None]:
    docs = self.nlp.pipe(ntexts)
    return [
      self.is_student(doc) for doc in docs
    ]

  def is_student(self, ntext: str | Doc) -> bool | None:
    doc = ntext if type(ntext) is Doc else self.nlp(ntext)
    for token in doc:
      # if not token.is_space and not token.is_punct:
      #   print(token, token.pos_, token.dep_)
      # Assuming whatever role is found first, is more important and deciding
      if is_student_noun(token):
        subtree = get_subtree_text(token)
        if re.search(PERPETUAL_REGEX, subtree) is None:
          return True
      elif is_student_verb(token):
        return True
      elif is_strong_non_student_noun(token):
        subtree = get_subtree_text(token)
        if re.search(ASPIRING_REGEX, subtree) is None:
          return False # not canceled by ASPIRING
      elif is_weak_non_student_noun(token):
        subtree = get_subtree_text(token)
        is_aspiring = re.search(ASPIRING_REGEX, subtree) is not None
        is_student_ = any(t for t in token.sent if is_student_noun(t))
        if not is_aspiring and not is_student_:
          return False # not canceled by ASPIRING or following STUDENT_NOUN
    return None

def is_student_noun(token: Token) -> bool:
  return (
    token.lower_.strip("-") in STUDENT_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  )

def is_strong_non_student_noun(token: Token) -> bool:
  return (
    token.lower_ in STRONG_NON_STUDENT_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  )

def is_weak_non_student_noun(token: Token) -> bool:
  return (
    token.lower_ in WEAK_NON_STUDENT_NOUNS and
    token.pos_ in {"NOUN", "PROPN", "ADJ"}
  )

def is_student_verb(token: Token) -> bool:
  if token.lower_ not in STUDENT_VERBS:
    return False
  # Special case if it's the first word (a relatively often case)
  if not token.i:
    return True
  # ...
  if token.pos_ == "VERB":
    # if token.dep_ == "ROOT":
    #   # yes, unless preceded by certain adverbs
    lefts = (
      left.lower_
      for left in list(token.lefts) + list(get_root(token).lefts)
    )
    return not any(left in {"always", "frantically", "never"} for left in lefts)
    # elif token.dep_ == "xcomp":
    #   # no, unless parented by "started"
    #   return token.head.lower_ == "started" if token.head else False
    # return True
  return False

def get_root(token: Token) -> Token:
  while token.dep_ != "ROOT":
    token = token.head
  return token

def get_subtree_text(token: Token) -> str:
  return "".join(t.lower_ + t.whitespace_ for t in token.subtree)

# E.g.
# "Lawyer. Lecturer. Researcher. Student." -> only the last noun gets properly marked as "NOUN"

# UNIVERSITIES. Currently thinking we can't generalize to students – could be teachers or scientists.
# assert is_student("Itmo")
# assert is_student("Dstu")
# assert is_student("Itmo university")
# assert is_student("Financial University under the government of Russia")
# assert is_student("Yandex.Fintech | ITMO SWE '25")

# GRADUATE
# assert not is_student("CMC MSU bachelor's degree, FCS HSE master student, ex-Data Scientist at Tinkoff bank.")

# TYPOS
# assert is_student("A 2nd year studxnt of the Higher IT School.")

# INTERNSHIP
# assert is_student("Currently looking for an ML internship. I love interesting and non-typical projects.")

# STUDY
# assert is_student("I'm studying data analytics and here are my first projects")
# assert is_student("Hello. I'am Vadim Tikhonov. I study code, data analysis and data science.")
# assert is_student("I am new to ML & DL")
