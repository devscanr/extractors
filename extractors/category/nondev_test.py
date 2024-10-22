from ..utils import fix_grammar, get_nlp, normalize
from .nondev import NondevParser

nlp = get_nlp("en_core_web_sm")
parser = NondevParser(nlp)

def are_nondevs(texts: list[str]) -> list[bool | None]:
  return parser.are_nondevs([
    fix_grammar(normalize(text)) for text in texts
  ])

def is_nondev(text: str) -> bool | None:
  return parser.is_nondev(
    fix_grammar(normalize(text))
  )

def describe_NondevParser() -> None:
  def describe_are_nondevs() -> None:
    def it_works() -> None:
      texts = [
        "I'm a manager",
        "I'm a developer",
      ]
      assert are_nondevs(texts) == [
        True,
        False,
      ]

  def describe_is_nondev() -> None:
    def it_basically_works() -> None:
      assert is_nondev("I'm a manager")
      assert None == is_nondev("I used to be an artist like you")
      assert None == is_nondev("I'm a student")
      assert False == is_nondev("I'm a developer")
      assert is_nondev("I'm an entrepreneur")
      assert is_nondev("I'm a manager and an engineer")

    def it_handles_set1() -> None:
      assert None == is_nondev("""
        My name is Devin and I am a Senior Gameplay Designer at CD Projekt Red working on the next Witcher.
      """) # designer
      assert False == is_nondev("""
        "Striving to become a front-end developer. Formerly climbing gym founder and co-owner"
      """) # developer
      assert is_nondev("""
        Founder, CBB Analytics. Sports Data Scientist and Web Developer.
      """) # founder
      assert None == is_nondev("""
        Twas brillig, and the slithy toves
        Did gyre and gimble in the wabe
      """)

    def it_handles_set2() -> None:
      assert is_nondev("""
        ✒️ Co-founder of CollBoard.com
      """)
      assert False == is_nondev("""
        Mathematician, Mentor, Founder, Fullstack Developer, Typographer, Tech Lead, Startup Engineer"
      """)
      assert False == is_nondev("""
        Solidity developer with 10+ years experience. CTO at entro.solutions
      """)
      assert is_nondev("""
        company founder at 18yo, programmer, game developer, virtual reality enthusiast
      """)
      assert is_nondev("""
        Fullstack web design agency
      """)

    def it_handles_set3() -> None:
      assert is_nondev("""
        Lecturer at Rowan University
      """)
