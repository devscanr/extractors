from bs4 import BeautifulSoup, NavigableString
from markdown import markdown

__all__ = ["html2text", "markdown2text"]

def html2text(html: str) -> str:
  soup = BeautifulSoup(html, features="html.parser")
  texts = []
  for element in soup.descendants:
    if isinstance(element, NavigableString):
      s = element.strip()
      if s:
        texts.append(
          f"{s}: {element.parent["href"]}"
          if element.parent and element.parent.name == "a" else
          s
        )
  return "\n\n".join(text for text in texts)

def markdown2text(md: str) -> str:
  if not md:
    return ""
  html = markdown(md, extensions=["fenced_code"])
  return html2text(html)
