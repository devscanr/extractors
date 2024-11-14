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
  dotequal_i, equal_i, dash_i = phrase.find(".="), phrase.find("="), phrase.find("-")
  l = len(phrase)
  first_cc = min(l, l, *[i for i in [dotequal_i, equal_i, dash_i] if i != -1])
  if first_cc == dotequal_i:
    # Handling ".="s
    head, tail = phrase[0:dotequal_i], phrase[dotequal_i + 2:]
    tail_patterns = to_patterns(tail)
    return [
      head + "." + pattern for pattern in tail_patterns
    ] + [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ] + [
      head + pattern for pattern in tail_patterns
    ]
  elif first_cc == equal_i:
    # Handling "="s
    head, tail = phrase[0:equal_i], phrase[equal_i + 1:]
    tail_patterns = to_patterns(tail)
    return [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ] + [
      head + pattern for pattern in tail_patterns
    ]
  elif first_cc == dash_i:
    # Handling "-"s
    head, tail = phrase[0:dash_i], phrase[dash_i + 1:]
    tail_patterns = to_patterns(tail)
    return [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ]
  else:
    return [phrase]

# print(
#   # to_patterns2("free-lance(r)"),
#   to_patterns2("(amazon-)aws=elasticache"),
#   # to_patterns2("php"),
#   # to_patterns2("my=free=lancer"),
#   # to_patterns2("free=lancing"),
#   # to_patterns2("node.=js(er)")
# )
