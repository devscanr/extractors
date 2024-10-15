from ..utils import fix_grammar, get_nlp, normalize
from .category import Categorizer, Categorized

nlp = get_nlp("en_core_web_sm")
categorizer = Categorizer(nlp)

def categorize(texts: list[str]) -> list[Categorized]:
  return categorizer.categorize([
    fix_grammar(normalize(text))
    for text in texts
  ])

def categorize_one(text: str) -> Categorized:
  return categorizer.categorize([text])[0]

def describe_Categorizer() -> None:
  def describe_categorize() -> None:
    def it_works() -> None:
      texts = [
        "I'm a student and a freelancer",
        "I'm an engineer, a student, occasionally a musician",
        "I'm a student, occasionally a mathematician",
        "I'm a manager",
      ]
      assert categorize(texts) == [
        Categorized(is_freelancer=True, is_lead=False, is_nondev=False, is_student=True),
        Categorized(is_freelancer=False, is_lead=False, is_nondev=False, is_student=False),
        Categorized(is_freelancer=False, is_lead=False, is_nondev=False, is_student=True),
        Categorized(is_freelancer=False, is_lead=False, is_nondev=True, is_student=False),
      ]

    def it_handles_set1() -> None:
      assert categorize_one("""
        Founder & CEO @QualiSage | Team Lead | Senior Full-Stack Developer | 10+ Years
      """) == Categorized(is_freelancer=False, is_lead=True, is_nondev=True, is_student=False)
      assert categorize_one("""
        Junior Programmer @BohemiaInteractive | Founder @QX-Interactive
      """) == Categorized(is_freelancer=False, is_lead=False, is_nondev=False, is_student=False)
      assert categorize_one("""
        Full-stack web developer and Zend Certified PHP Engineer. Lead dev @Web3Box and freelancer @toptal
      """) == Categorized(is_freelancer=False, is_lead=True, is_nondev=False, is_student=False)
      assert categorize_one("""
        Game Producer & Lead Development | Network & Systems Admin
      """) == Categorized(is_freelancer=False, is_lead=True, is_nondev=False, is_student=False)
      assert categorize_one("""
        Technical Artist. Founder of @Golden-Ram-Studio
      """) == Categorized(is_freelancer=False, is_lead=False, is_nondev=True, is_student=False)

  def it_handles_set2() -> None:
    assert categorize_one("""
      Full stack software engineer. Freelance. Some time ago: CTO & co-founder at Nightset
    """) == Categorized(is_freelancer=True, is_lead=False, is_nondev=False, is_student=False)
    assert categorize_one("""
      Game developer, programmer, bit of an artist; C++, Unreal
    """) == Categorized(is_freelancer=False, is_lead=False, is_nondev=False, is_student=False)
    assert categorize_one("""
      Environmental student, Unreal Engine developer
    """) == Categorized(is_freelancer=False, is_lead=False, is_nondev=False, is_student=True)
    assert categorize_one("""
      Software engineer working on games, systems, and tools. Currently leading UI on Clip It @ Neura Studios.
    """) == Categorized(is_freelancer=False, is_lead=True, is_nondev=False, is_student=False)
    assert categorize_one("""
      Founder and CEO of @rangle , the leading lean/agile JavaScript consulting firm.
    """) == Categorized(is_freelancer=False, is_lead=True, is_nondev=True, is_student=False)
