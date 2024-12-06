from extractors.skills.extractor import SkillExtractor
from extractors.utils import normalize

# + 2 DevOps
# + 3 Mobile
# + 1 (Product) Analyst
# + 3 QA
# + 4 ML
# + 4 Security

texts: list[str] = [
  """
  """
]

e = SkillExtractor()

for text in texts:
  print("text:", repr(text))
  print(
    e.extract(normalize(text))
  )
  print("----------")

# TODO remove `_.used` extension if it's no longer necessary :)
