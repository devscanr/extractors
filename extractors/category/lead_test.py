from ..utils import fix_grammar, get_nlp, normalize
from .lead import LeadParser

nlp = get_nlp("en_core_web_sm")
parser = LeadParser(nlp)

def are_leads(texts: list[str]) -> list[bool | None]:
  return parser.are_leads([
    fix_grammar(normalize(text)) for text in texts
  ])

def is_lead(text: str) -> bool | None:
  return parser.is_lead(
    fix_grammar(normalize(text))
  )

def describe_LeadParser() -> None:
  def describe_are_leads() -> None:
    def it_works() -> None:
      texts = [
        "I'm a team lead",
        "I'm a developer",
      ]
      assert are_leads(texts) == [
        True,
        None,
      ]

  def describe_is_freelancer() -> None:
    def it_handles_set1() -> None:
      assert is_lead("Gopher. Former TL of Go CDK and author of Wire.")
      assert is_lead("TL, JavaScript Developer")
      assert is_lead("CTO, TL")
      assert None == is_lead("TL;DR : DJ turned software engineer")
      assert None == is_lead("Founder and SVP Creative at Frac.tl")
      assert is_lead("Senior Site Reliability Engineer, TL")

    def it_handles_set2() -> None:
      assert is_lead("Engineering Leader")
      assert is_lead("AI Thought Leader | Cognitive Architecture | Heuristic Imperatives")
      assert is_lead("Tech leader")
      assert is_lead("Open Source Enthusiast, Project Leader @OWASP Chapter Leader @OWASP")
      assert is_lead("Mobile Platform Technical Leader - iOS Engineer")
      assert is_lead("Team Leader Manager")
      assert is_lead("People first leader and indie hacker.") # FP?, ok for simplicity
      assert is_lead("Leader of Ukrainian Rust Community")    # FP, ok for simplicity

    def it_handles_set3() -> None:
      assert is_lead("AWESOME Developer/Lead")
      assert is_lead("Software Dev & Tech Lead")
      assert is_lead("Horizon 2020 Project LEAD - Low-Emission Adaptive last mile logistics")
      assert is_lead("Lead Cloud Engineer @ Namecheap")
      assert is_lead("Technical Content Lead")
      assert is_lead("IT Sec guy, @zaproxy co-lead, @OWASP WSTG co-lead, @OWASP VWAD co-lead, Hac≺3r, supporter of oxford commas, #INTJ.")
      assert None == is_lead("Raising the bar for leadership in tech.")

    def it_handles_set4() -> None:
      assert is_lead("The leading platform for local cloud development") # FP
      assert is_lead("Leading anti-cheat @ someplace.")
      assert is_lead("Software Engineer at @microsoft leading the Copilot UX team")
      assert is_lead("Designer Developer from Northern Ireland, leading design and development teams in San Francisco.")
      assert None == is_lead("Tech stuff at Leadingly LLC")
      assert is_lead("All roads leading to humanoids")  # FP
      assert is_lead("Captain leading from the front!") # FP
      assert is_lead("Into kubernetes, typescript, golang, microservices, and leading teams.") # FP?
      assert is_lead("Leading talent to expertise") # FP
      assert None == is_lead("mechanical engineer with leading skills")
      assert None == is_lead("Building leading data science tools and state-of-the-art ML models")
      assert is_lead("Creating market-leading software products") # FP
      assert is_lead("Leading a life long learning expedition") # FP
