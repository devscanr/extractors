from ..utils import normalize
from ..web import markdown2text
from .contacts import Contacts, parse_contacts

def parse(text: str) -> Contacts:
  return parse_contacts(normalize(text))

def parse_md(md: str) -> Contacts:
  return parse(markdown2text(md))

def describe_parse_emails() -> None:
  def it_parses_set1() -> None:
    assert parse("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == Contacts(
      emails = ["bishal-hadka-1600@gg.com"],
      phones = ["9707999291"],
      urls = [],
    )
    assert parse("Phone: 9046571689 https://justin-rick.com") == Contacts(
      emails = [],
      phones = ["9046571689"],
      urls = ["https://justin-rick.com"],
    )

  def it_parses_set2() -> None:
    assert parse_md("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == Contacts(
      emails = ["bishal-hadka-1600@gg.com"],
      phones = ["9707999291"],
      urls = [],
    )
    assert parse("Phone: 9046571689 https://justin-rick.com") == Contacts(
      emails = [],
      phones = ["9046571689"],
      urls = ["https://justin-rick.com"],
    )  
