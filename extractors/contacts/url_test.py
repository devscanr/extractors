from ..utils import normalize
from .url import parse_urls

def parse(text: str) -> list[str]:
  return parse_urls(normalize(text))

def describe_parse_urls() -> None:
  def it_parses_set1() -> None:
    assert parse("""
      <a href="https://google.com">test1</a>
      [test2](https://facebook.com)
      https://gizmo.com/foo/bar?x=X#xxx
      scabbiaza.net
      ./aaa.txt
      bbb.txt
      /ccc.txt
      mailto:me@gg.net
      gg.ggx
      gg.gg
    """) == ["https://google.com", "https://facebook.com", "https://gizmo.com/foo/bar?x=X#xxx", "scabbiaza.net", "gg.gg"]
