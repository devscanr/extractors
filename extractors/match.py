# import re
# from typing import Pattern
#
# SEPS = ["", "-", " "]
#
# def to_variants(phrase: str) -> list[str]:
#   if "=" in phrase:
#     [head, tail] = phrase.split("=", maxsplit = 1)
#     tail_variants = to_variants(tail)
#     return [
#       head + x + variant for variant in tail_variants
#       for x in SEPS
#     ]
#   else:
#     return [phrase]
#
# def words_to_regex(words: list[str] | set[str]) -> Pattern[str]:
#   return re.compile(r"(?<!\w)(?:" + r"|".join(
#     variant
#     for word in words
#     for variant in to_variants(word)) + r")(?!\w)"
#   )

# def to_patterns(phrase: str) -> list[list[dict[str, Any]]]:
#   if "=" in phrase:
#     [head, tail] = phrase.split("=", maxsplit = 1)
#     tail_patterns = to_patterns(tail)
#     return [
#       [{"LOWER": head}, {"LOWER": "-", "OP": "?"}] + pattern for pattern in tail_patterns
#     ] + ([
#       [{"LOWER": pattern[0]["LOWER"] + head}] + pattern[1:]
#       for pattern in tail_patterns
#     ] if "=" in tail else [[{"LOWER": head + tail}]])
#   else:
#     return [
#       [{"LOWER": phrase}]
#     ]

# import spacy
# from spacy.matcher import Matcher
#
# def to_patterns(phrase: str) -> list[object]:
#   if "=" in phrase:
#     return [
#       [{"LOWER": phrase}],
#       [{"LOWER": "life"}, {"IS_PUNCT": True}, {"LOWER": "long"}],
#       [{"LOWER": "life"}, {"IS_SPACE": True}, {"LOWER": "long"}],
#     ]
#   else:
#     return [
#       {"LOWER": phrase}
#     ]
#
# nlp = spacy.load("en_core_web_lg")
# matcher = Matcher(nlp.vocab)
#
# # doc = nlp("Go to school, learn Go, JS, HTML languages") # , Chrome (Google Chrome)
# doc = nlp("life-long lifelong life    long sophomore student") # , Chrome (Google Chrome)
# for tok in doc:
#   print(tok, tok.pos_)
# #
# matcher.add("lifelong", [
#   [{"LOWER": "lifelong"}],
#   [{"LOWER": "life"}, {"IS_SPACE": True}, {"LOWER": "long"}],
#   [{"LOWER": "life"}, {"IS_PUNCT": True}, {"LOWER": "long"}],
# ])
#
# # matcher.add("Go", [
# #   [{"LOWER": "go", "POS": "PROPN"}]
# # ])
# # matcher.add("PHP", [
# #   [{"LOWER": {"REGEX": r"PHP\d?"}}]
# # ])
# # matcher.add("Google Chrome", [
# #   [{"LOWER": "google", "OP": "?"}, {"LOWER": "chrome"}]
# # ])
# matches = matcher(doc)
# for match_id, start, end in matches:
#     string_id = nlp.vocab.strings[match_id]  # Get string representation
#     span = doc[start:end]  # The matched span
#     print(match_id, string_id, start, end, span.text) # string_id,
