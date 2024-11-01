from bs4 import BeautifulSoup, Comment, NavigableString, PageElement, Tag
from markdown import markdown
import re
from typing import cast

__all__ = ["html2text", "markdown2text"]

def html2text(html: str) -> str:
  soup = BeautifulSoup(html, features="html.parser")
  texts: list[str] = []
  for element in soup.descendants:
    if isinstance(element, Tag) and element.name == "a":
      if not element.get_text().strip() and element.has_attr("href"):
        href = str(element["href"])
        if href.startswith("mailto:"):
          texts.append(f"Email: {href}")
        elif is_whitelist_url(href):
          texts.append(f"URL: {href}")
        else:
          texts.append("/URL/")
    elif isinstance(element, NavigableString) and not isinstance(element, Comment):
      s = element.strip()
      if has_parent(element, "code"):
        if s:
          texts.append("/Code/")
      # elif has_parent(element, "a"):
      elif has_parent(element, "a"):
        parent_href = str(cast(Tag, element.parent)["href"])
        if parent_href.startswith("mailto:"):
          texts.append(f"{s.capitalize() or "Email"}: {parent_href}")
        elif parent_href and s:
          texts.append(f"{s.capitalize()}: {parent_href}")
        elif s:
          texts.append(s)
      elif s:
        texts.append(s)

  return "\n\n".join(text for text in texts)

def has_parent(element: PageElement, name: str) -> bool:
  return element.parent is not None and element.parent.name == name

def markdown2text(md: str) -> str:
  if not md:
    return ""
  html = markdown(md, extensions=["fenced_code"])
  return html2text(html)

def is_whitelist_url(href: str) -> bool:
  return re.search(WHITE_DOMAINS_REGEX, href) is not None

WHITE_DOMAINS_REGEX = r"\b" + r"|".join([
  r"about\.me",
  r"behance\.net",
  r"bio\.link",
  r"buymeacoffee\.com",
  r"codecademy\.com",
  r"codepen\.io",
  r"codersrank\.io",
  r"codewars\.com",
  r"dev\.to",
  r"discord\.com",
  r"discordapp\.com",
  r"dribbble\.com",
  r"facebook\.com",
  r"fb\.com",
  r"github\.com",
  r"github\.io",
  r"gitlab\.com",
  r"habr\.com",
  r"hashnode\.com",
  r"hashnode\.dev",
  r"herokuapp\.com",
  r"hexlet\.io",
  r"hh\.ru",
  r"instagram\.com",
  r"kaggle\.com",
  r"leetcode\.com",
  r"linkedin\.com",
  r"linktr\.ee",
  r"medium\.com",
  r"netlify\.app",
  r"patreon\.com",
  r"reddit\.com",
  r"showwcase\.com",
  r"stackoverflow\.com",
  r"stackshare\.io",
  r"t\.me",
  r"tiktok\.com",
  r"tilda\.ws",
  r"toptal\.com",
  r"twitch\.tv",
  r"twitter\.com",
  r"udemy\.com",
  r"upwork\.com",
  r"vercel\.app",
  r"vk\.com",
  r"vk\.me",
  r"wordpress\.com",
  r"wordpress\.org",
  r"youtube\.com",
  r"x\.com",
]) + r"\b"
