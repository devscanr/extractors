from extractors.category import Categorizer, Categorized
from extractors.utils import fix_grammar, get_nlp, normalize

nlp = get_nlp("en_core_web_sm")
categorizer = Categorizer(nlp)

def categorize(texts: list[str]) -> list[Categorized]:
  return categorizer.categorize(texts)

def categorize_one(text: str) -> Categorized:
  return categorizer.categorize([text])[0]

def t(text: str) -> str:
  return fix_grammar(normalize(text))

def describe_Categorizer() -> None:
  def describe_categorize() -> None:
    def it_works() -> None:
      texts = [
        t("I'm a student and a freelancer"),
        t("I'm an engineer, a student, occasionally a musician"),
        t("I'm a student, occasionally a mathematician"),
        t("I'm a manager"),
      ]
      assert categorize(texts) == [
        Categorized(is_freelancer=True, is_nondev=None, is_student=True),
        Categorized(is_freelancer=None, is_nondev=False, is_student=False),
        Categorized(is_freelancer=None, is_nondev=False, is_student=True),
        Categorized(is_freelancer=None, is_nondev=True, is_student=False),
      ]

    def it_handles_set1() -> None:
      assert categorize_one("""
        Founder & CEO @QualiSage | Team Lead | Senior Full-Stack Developer | 10+ Years
      """) == Categorized(is_freelancer=False, is_nondev=True, is_student=False)
      assert categorize_one("""
        Junior Programmer @BohemiaInteractive | Founder @QX-Interactive
      """) == Categorized(is_freelancer=False, is_nondev=False, is_student=False)
      assert categorize_one("""
        Full-stack web developer and Zend Certified PHP Engineer. Lead dev @Web3Box and freelancer @toptal
      """) == Categorized(is_freelancer=False, is_nondev=False, is_student=False)
      assert categorize_one("""
        Game Producer & Lead Development | Network & Systems Admin
      """) == Categorized(is_freelancer=False, is_nondev=False, is_student=False)
      assert categorize_one("""
        Technical Artist. Founder of @Golden-Ram-Studio
      """) == Categorized(is_freelancer=False, is_nondev=True, is_student=False)

  def it_handles_set2() -> None:
    assert categorize_one("""
      Full stack software engineer. Freelance. Some time ago: CTO & co-founder at Nightset
    """) == Categorized(is_freelancer=True, is_nondev=False, is_student=False)
    assert categorize_one("""
      Game developer, programmer, bit of an artist; C++, Unreal
    """) == Categorized(is_freelancer=None, is_nondev=False, is_student=False)
    assert categorize_one("""
      Environmental student, Unreal Engine developer
    """) == Categorized(is_freelancer=None, is_nondev=False, is_student=True)
