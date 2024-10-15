from urlextract import URLExtract # type: ignore
from ..utils import uniq

__all__ = ["parse_urls"]

extractor = URLExtract()

def parse_urls(ntext: str) -> list[str]:
  # TODO smart deduplicate
  if not ntext:
    return []
  urls = extractor.find_urls(ntext)
  return uniq(
    url for url in urls
    if len(url) <= 255
  )
