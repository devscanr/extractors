import re
from typing import Sequence
from .utils import IN, LEFT_ID, POS, Pattern, REL_OP, RIGHT_ATTRS, RIGHT_ID, orth

__all__ = [
  "expand_phrase1", "expand_phrase2", "expand_phrase12", "to_deppatterns",
]

# expand_phrase1
def expand_phrase1(phrase: str) -> list[str]:
  if not phrase:
    return []
  dotequal_i, equal_i, dash_i = phrase.find(".="), phrase.find("="), phrase.find("-")
  l = len(phrase)
  first_cc = min(l, l, *[i for i in [dotequal_i, equal_i, dash_i] if i != -1])
  if first_cc == dotequal_i:
    # TODO support also "/=" ?
    # Handling ".="s
    head, tail = phrase[0:dotequal_i], phrase[dotequal_i + 2:]
    tail_patterns = expand_phrase1(tail)
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
    tail_patterns = expand_phrase1(tail)
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
    tail_patterns = expand_phrase1(tail)
    return [
      head + "-" + pattern for pattern in tail_patterns
    ] + [
      head + " " + pattern for pattern in tail_patterns
    ]
  else:
    return [phrase]

def expand_phrases1(phrases: Sequence[str]) -> list[str]:
  return [
    patt
    for phrase in phrases
    for patt in expand_phrase1(phrase)
  ]

# expand_phrase2
def expand_phrase2(phrase: str) -> list[str]:
  drop = lambda text: re.sub(r"\([^)]*\)", "", text)
  open = lambda text: re.sub(r"\(|\)", "", text)
  return [
    patt for patt in ([drop(phrase), open(phrase)]
    if "(" in phrase else [phrase])
  ]

def expand_phrases2(phrases: Sequence[str]) -> list[str]:
  return [
    patt
    for phrase in phrases
    for patt in expand_phrase2(phrase)
  ]

# expand_phrase(s)12
def expand_phrase12(phrase: str) -> list[str]:
  return [
    patt2
    for patt1 in expand_phrase1(phrase)
    for patt2 in expand_phrase2(patt1)
  ]

def expand_phrases12(phrases: Sequence[str]) -> list[str]:
  return [
    patt
    for phrase in phrases
    for patt in expand_phrase12(phrase)
  ]

# to_deppatterns
def to_deppatterns(phrase: str) -> list[Pattern]:
  # (modifier) << (anchor) e.g
  # (computer) << (science)
  parts = [part.strip() for part in phrase.split("<<")]
  match len(parts):
    case 1:
      anchor = parts[0]
      return [
        [{
          # (term)
          RIGHT_ID: "anchor",
          RIGHT_ATTRS: orth(anchor)
        }]
      ]
    case 2:
      (modifier, anchor) = parts
      # print("modifier:", modifier)
      # print("anchor:", anchor)
      return [
        [{
          # (modifier_anchor)
          RIGHT_ID: "modifier",
          RIGHT_ATTRS: orth(modifier + anchor)
        }],
        [{
          # (modifier)
          RIGHT_ID: "modifier",
          RIGHT_ATTRS: orth(modifier)
        }, {
          # (modifier) << (anchor)
          LEFT_ID: "modifier",
          REL_OP: "<<",
          RIGHT_ID: "anchor",
          RIGHT_ATTRS: orth(anchor) # & {DEP: {IN: ["ROOT", "pobj", "dobj"]}}
        }],
        # [{ -- I think it's mostly covered by the next graph pattern
        #   # (modifier)
        #   RIGHT_ID: "modifier",
        #   RIGHT_ATTRS: orth(modifier)
        # }, {
        #   # (modifier) . (anchor)
        #   LEFT_ID: "modifier",
        #   REL_OP: ".",
        #   RIGHT_ID: "anchor",
        #   RIGHT_ATTRS: orth(anchor)
        # }],
        [{
          # (modifier)
          RIGHT_ID: "modifier",
          RIGHT_ATTRS: orth(modifier) # game(s)
        }, {
          # (modifier) < (other_anchor)
          LEFT_ID: "modifier",
          REL_OP: "<<",
          RIGHT_ID: "other_anchor", # dev
          RIGHT_ATTRS: {POS: {IN: ["NOUN", "PROPN", "PRON"]}},
        }, {
          # (other_anchor) [appos]> (anchor)
          LEFT_ID: "other_anchor",
          REL_OP: ">>",
          RIGHT_ID: "anchor", # design
          RIGHT_ATTRS: orth(anchor)
        }]
      ]
    case _:
      raise Exception("only '(modifier) << (anchor)' format is currently supported")
