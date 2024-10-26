import re

__all__ = ["to_patterns2"]

def to_patterns2(phrase: str) -> list[str]:
  drop = lambda text: re.sub(r"\([^)]*\)", "", text)
  open = lambda text: re.sub(r"\(|\)", "", text)
  return [
    patt
    for pattern in to_patterns(phrase)
    for patt in ([drop(pattern), open(pattern)] if "(" in pattern else [pattern])
  ]

def to_patterns(phrase: str) -> list[str]:
  if not phrase:
    return []
  dotequal_i = phrase.find(".=")
  equal_i = phrase.find("=")
  if 0 <= dotequal_i and (equal_i == -1 or dotequal_i < equal_i):
    head, tail = phrase[0:dotequal_i], phrase[dotequal_i + 2:]
    tail_patterns = to_patterns(tail)
    return [
      head + "." + pattern for pattern in tail_patterns
    ] + [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ] + (
      [
        head + pattern[0] + pattern[1:]
        for pattern in tail_patterns
      ]
      if "=" in tail
      else [
        head + tail
      ]
    )
  elif 0 <= equal_i and (dotequal_i == -1 or equal_i < dotequal_i):
    head, tail = phrase[0:equal_i], phrase[equal_i + 1:]
    tail_patterns = to_patterns(tail)
    return [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ] + (
      [
        head + pattern[0] + pattern[1:]
        for pattern in tail_patterns
      ]
      if "=" in tail
      else [
        head + tail
      ]
    )
  else:
    return [phrase]

# print(
#   to_patterns2("free=lance(r)"),
#   to_patterns2("free=lancing"),
#   # to_patterns2("node.=js(er)")
# )
