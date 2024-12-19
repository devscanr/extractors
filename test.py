from extractors.skills.extractor import SkillExtractor
from extractors.utils import normalize

texts: list[str] = [
  """
  Certified Data Science graduate and a Computer Systems Engineer with strong data engineering, visualization, and analytical skills.

  """
]

# Counter-cases for "Architecture"
# licensed architect, architectural designer and web developer/programmer
# UI Architect

e = SkillExtractor()

for text in texts:
  print("ntext:", repr(normalize(text)))
  print(
    e.extract(normalize(text))
  )
  print("----------")

# TODO remove `_.used` extension if it's no longer necessary :)
