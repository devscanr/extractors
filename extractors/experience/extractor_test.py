# mypy: disable-error-code=no-untyped-def
import pytest
from spacy import Language
from ..utils import fix_grammar, normalize
from .data import TAGS
from .experience import Experience
from .extractor import ExperienceExtractor

class Test_ExperienceExtractor:
  @pytest.fixture(scope="class")
  def extract(self, nlp: Language):
    ex = ExperienceExtractor(nlp, TAGS)
    def extract(text: str) -> list[Experience]:
      return ex.extract(fix_grammar(normalize(text)))
    return extract

  def test_extract_smoke(self, extract) -> None:
    # Exact months
    assert extract("1 month of experience") == [Experience("Exact", months=1)]
    assert extract("1+ month of experience") == [Experience("Exact", months=1, over=True)]
    assert extract("some months of experience") == []
    # Exact years
    assert extract("1 year of experience") == [Experience("Exact", months=12)]
    assert extract("one year experience") == [Experience("Exact", months=12)]
    assert extract("1+ year of experience") == [Experience("Exact", months=12, over=True)]
    assert extract("1.5 years of experience") == [Experience("Exact", months=18)]
    assert extract("some years of experience") == []
    # Other
    assert extract("Someone") == []
    assert extract("Junior engineer") == [Experience("Junior")]
    assert extract("Middle designer") == []
    assert extract("Senior developer") == [Experience("Senior")]
    assert extract("Senior student") == []
    # Multiple
    assert extract("Junior backend, middle frontend") == [Experience("Junior"), Experience("Middle")]

  def test_extract_adhoc1(self, extract) -> None:
    # Past markers don't affect the extractor
    assert extract("Former principal developer") == [Experience("Principal")]
    assert extract("Ex middle developer") == [Experience("Middle")]
    assert extract("Retired senior developer") == [Experience("Senior")]

  def test_extract_adhoc2(self, extract) -> None:
    # Negations affect the behavior
    assert extract("Not a junior developer") == []
    assert extract("Not a senior engineer") == []

  def test_extract_adhoc3(self, extract) -> None:
    # Future markers affect the extractor
    assert extract("One day I will be a senior developer") == []
    assert extract("Middle developer wannabe") == []

  # def test_extract_adhoc4(self, extract) -> None:
  #   # Plus should not be captured by mistake
  #   assert extract("Senior Backend + Frontend developer") == [Experience("Senior", over=False)]
  #   assert extract("Backend + Frontend: 2 years of experience") == [Experience("Exact", months=24, over=False)]

  def test_extract_adhoc5(self, extract) -> None:
    # Internship
    assert extract("Intern at Microsoft") == [Experience("Intern")]
    # assert extract("Internship at Netflix") == [] # Not implemented yet, should be
    # assert extract("Looking for internship") == []

  def test_extract_bios1(self, extract) -> None:
    assert extract("me is Senior fullstack developer") == [Experience("Senior")]
    assert extract("Full Stack Developer / Founder of Senior Be Hello World") == []
    assert extract("intermediate blockchain engineer") == [Experience("Middle")]
    assert extract("""
      🍔💻| 1+ year of experience in software development
    """) == [Experience("Exact", months=12, over=True)]
    assert extract("""
      Senior iOS Developer with more than 12 year of experience.
    """) == [Experience("Senior"), Experience("Exact", months=144, over=True)]

  def test_extract_bios2(self, extract) -> None:
    assert extract("""
      I am an IT Pro with 30+ years of experience, a multi-year Microsoft MVP, 
      PowerShell author, teacher, and a member of the PowerShell Cmdlet Working Group.
    """) == [Experience("Exact", months=360, over=True)]
    assert extract("""
      my name kim i'm 15 year old i have many experience penetration testing
    """) == []
    assert extract("""
      IT CONSULTANT | REMOTE SENIOR JAVA SOFTWARE ENGINEER
    """) == [Experience("Senior")]
    assert extract("17yo dev; @dotcute & @remote-kakao") == []

  def test_extract_bios3(self, extract) -> None:
    assert extract("""
      Principal Engineer working on remote management software
    """) == [Experience("Principal")]
    assert extract("Head of Mobile, CTO, Founder, #Engineer, #Consultant, #Remote") == []
    assert extract("CTO | Senior Systems Analyst | Hybrid Remote") == [Experience("Senior")]
    assert extract("Middle+ Android Developer(Looking for Remote Role)") == [Experience("Middle", over=True)]
    assert extract("Intermediate Site Reliability Engineer, TL") == [Experience("Middle")]

  def test_extract_bios4(self, extract) -> None:
    assert extract("Junior Dev @ free lance") == [Experience("Junior")]
    assert extract("A former student at Something") == []
    assert extract("Just a noob") == []
    assert extract("Senior student of Comp Sci @ Concordia University") == []
    assert extract("A 2nd year studxnt of the Higher IT School.") == []
    assert extract("Currently looking for an ML internship") == []

  def test_extract_bios5(self, extract) -> None:
    assert extract("""
      Senior iOS Developer with more than 12 year of experience.
    """) == [Experience("Senior"), Experience("Exact", months=144, over=True)]
    assert extract("""
      I have one year experience on GitHub
    """) == [Experience("Exact", months=12)]
    assert extract("""
      Year Up works to close the #OppDivide by providing young adults w/skills, experience, & support that empowers them to reach their potential
    """) == []

  def test_extract_bios6(self, extract) -> None:
    assert extract("""
      Solidity developer with 10+ years experience. CTO at entro.solutions
    """) == [Experience("Exact", months=120, over=True)]
    assert extract("""
      company founder at 18yo, programmer, game developer, VR enthusiast
    """) == []
    assert extract("""
      Full stack software engineer. Freelance. Some time ago: CTO & co-founder at Nightset
    """) == []
    assert extract("""
      3.5 + Year Experience Swift 4 iOS Developer
    """) == [Experience("Exact", months=42, over=True)]

  def test_extract_bios7(self, extract) -> None:
    assert extract("""
      Full-stack junior software developer, system administrator and IT consultant.
    """) == [Experience("Junior")]
    assert extract("""
      My name is Devin and I am a Senior Gameplay Designer at
      CD Projekt Red working on the next Witcher.
    """) == [] # He's a "Senior Designer", we extract only DEV experience!
    assert extract("""
      rookie frontend developer
    """) == []

  def test_extract_bios8(self, extract) -> None:
    assert extract("""
      Senior Manager, Senior Program/Project Manager, Junior Developer wannabe
    """) == []
    assert extract("""
      This is Mishu Dhar Chando. Having More than 2 Year Experience at Data Science, 
      Machine Learning, Image Processing, Natural Language Processing
    """) == [Experience("Exact", months=24, over=True)]
    assert extract("""
      About I have 5-year experience in Android native app development 
      and 5-year experience in Flutter and 2-year experience in game development using Unity3D
    """) == [Experience("Exact", months=60), Experience("Exact", months=60), Experience("Exact", months=24)]
    assert extract("""
      Front-end developer with a background in history and teaching, experience as an ESL tutor, 
      and 8-year experience in BNDES. Amateur musician
    """) == [Experience("Exact", months=96)]

  def test_extract_bios9(self, extract) -> None:
    assert extract("""
      WEB3 user and 3 Year+ Experience in crypto.
    """) == [Experience("Exact", months=36, over=True)]
    assert extract("""
      Front-end & WordPress developer, UX consultant. 
      Making stuff for the web since 2005
    """) == [] # not capturing phrases like this
    assert extract("""
      I have transformed years of freelancing into a full-time career
    """) == [] # not capturing phrases like this
    assert extract("""
      Hi, I am 22 years old freelance full-stack developer from Czech Republic.
    """)  == []

  def test_extract_bios10(self, extract) -> None:
    assert extract("""
      Backend Developer 4 Year Experience
    """)  == [Experience("Exact", months=48)]
    assert extract("""
      Application Developer(Android and Flutter ) || 3+ Year Experience
    """)  == [Experience("Exact", months=36, over=True)]
