from ..dpatterns import DPattern, LEFT_ID, REL_OP, RIGHT_ATTRS, RIGHT_ID
from ..extractor import Tag
from .tag import ExpTag
from ..ppatterns import expand_parens, to_ppatterns
from ..xpatterns import lower, orth_or_lower, pos_nounlike, regex

ROLES = [p for ph in [
  "administrator", "admin",
  "architect",
  "analyst",
  "coder",
  "dataop(s)",
  "developer", "dev",
  "devop(s)",
  "engineer", "eng",
  "mlop(s)",
  "netop(s)",
  "op(s)",
  "programmer",
  "qa",
  "scientist",
  "secop(s)",
  "tester",
] for p in expand_parens(ph)]

SUDOROLES = to_ppatterns([
  # Languages
  "c", "c.",
  "c#",
  "javascript", "js",
  "php",
  "python",
  "ruby",
  "typescript", "ts",
  # Fields
  "backend", "blockchain(s)",
  "frontend", "fullstack", "game(s)",
  "mobile(s)", "network(s)",
  "security", "system(s)",
  "web",
])

def term_of_exp_patterns() -> list[Tag]:
  # Example: years* > of > experience
  return [
    ExpTag(name, [[
      {RIGHT_ID: "term", RIGHT_ATTRS: regex(termreg)},
      {RIGHT_ID: "of", RIGHT_ATTRS: lower("of"), LEFT_ID: "term", REL_OP: ">"},
      {RIGHT_ID: exp, RIGHT_ATTRS: lower(exp), LEFT_ID: "of", REL_OP: ">"},
    ]])
    for name, termreg in [("YOE", r"(?i)^years?\+?$"), ("MOE", r"(?i)^months?\+?$")]
    for exp in ["experience", "expertise"]
  ]

def term_exp_patterns() -> list[Tag]:
  # Example: years < experience*
  return [
    ExpTag(name, [[
      {RIGHT_ID: "term", RIGHT_ATTRS: regex(reg)},
      {RIGHT_ID: exp, RIGHT_ATTRS: lower(exp), LEFT_ID: "term", REL_OP: "<"},
    ]])
    for name, reg in [("YOE", r"(?i)^years?\+?$"), ("MOE", r"(?i)^months?\+?$")]
    for exp in ["experience", "expertise"]
  ]

def init_role_patterns(phrases: list[str]) -> list[str | DPattern]:
  patterns: list[str | DPattern] = []
  for anchor in ROLES:
    for phrase in phrases:
      for modifier in expand_parens(phrase):
        patterns.append(f"{modifier}<{anchor}")
        patterns.append([{
          RIGHT_ID: modifier,
          RIGHT_ATTRS: orth_or_lower(modifier),
        }, {
          LEFT_ID: modifier,
          REL_OP: "<",
          RIGHT_ID: "$noun",
          RIGHT_ATTRS: pos_nounlike(),
        }, {
          LEFT_ID: "$noun",
          REL_OP: "<",
          RIGHT_ID: anchor,
          RIGHT_ATTRS: orth_or_lower(anchor),
        }])
  return patterns

def init_sudorole_patterns(phrases: list[str]) -> list[str | DPattern]:
  return [
    f"{modifier}-{anchor}"
    for anchor in SUDOROLES
    for phrase in phrases
    for modifier in expand_parens(phrase)
  ]

def init_all_patterns(modifiers: list[str]) -> list[str | DPattern]:
  return [
    *modifiers,
    *init_role_patterns(modifiers),
    *init_sudorole_patterns(modifiers),
  ]

def init_double_patterns(modifiers: list[str]) -> list[str | DPattern]:
  return [
    *init_role_patterns(modifiers),
    *init_sudorole_patterns(modifiers),
  ]

TAGS: list[Tag] = [
  # EXACT
  *term_of_exp_patterns(),
  *term_exp_patterns(),

  # OTHER
  ExpTag("Intern", init_all_patterns(["intern", "internship", "trainee"])),
  ExpTag("Junior", init_double_patterns(["junior(+)"])), # TODO accept if "Junior" is ROOT
  ExpTag("Middle", init_double_patterns(["middle(+)", "intermediate(+)"])), # TODO accept if "Middle" is ROOT
  ExpTag("Senior", init_double_patterns(["senior(+)"])),
  ExpTag("Principal", init_double_patterns(["principal(+)"])),
]
