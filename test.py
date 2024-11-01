from extractors.skills.extractor import SkillExtractor
from extractors.utils import fix_grammar, normalize

se = SkillExtractor()

# print(
#   se.extract("I'm a web developer, working mostly with PHP, Go, and JS")
# )

texts = [
  # "JavaScript therapist, creative coder. Looking to excel.",
  # "Excel at your craft.",
  "working at Strapi",
  # "Analista de Dados | Python | R | SQL | ETL | Excel",
  # "oracle && excel dba",
  # "Numba",
  # "numba 1",
  # "numba wan",
  # "numba one",
]

for text in texts:
  print("Input:", repr(text))
  print(fix_grammar(normalize(text)))
  print(
    "Output:", se.extract(fix_grammar(normalize(text)))
  )
  print()
