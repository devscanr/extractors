from itertools import dropwhile
import re
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span, Token
from typing import Any, Literal, cast, Sequence
from ..categories.extractor import is_hashtagged
from ..markers import is_future, is_metaphorical, is_negated, is_past
from ..patterns import expand_phrase12
from ..utils import LB, RB, get_nlp
from .data import LABELED_PHRASES

__all__ = ["TitleExtractor", "fix_more_grammar"]

class TitleExtractor:
  def __init__(self, name: str = "en_core_web_lg") -> None:
    self.nlp = get_nlp(name)
    self.init_eruler("entity_ruler", LABELED_PHRASES)

  def init_eruler(self, name: str, labeled_phrases: dict[str, list[str]]) -> None:
    ruler: EntityRuler = cast(Any, self.nlp.add_pipe("entity_ruler", config={
      "phrase_matcher_attr": "LOWER",
    }, name=name))
    for label, phrases in labeled_phrases.items():
      for phrase in phrases:
        if isinstance(phrase, str):
          assert not re.search("[A-Z]", phrase), f"{phrase!r} contains uppercase character(s), use pattern syntax"
          ruler.add_patterns([{
            "label": label,
            "pattern": pattern
          } for pattern in expand_phrase12(phrase)])
        else:
          raise Exception("not supported")

  # def init_pmatcher(..):
  #   self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
  #   self.pmatcher.add("PAST", [self.nlp(m) for m in PAST_MARKERS])
  #   self.pmatcher.add("PRESENT", [self.nlp(m) for m in PRESENT_MARKERS])
  #   self.pmatcher.add("FUTURE", [self.nlp(m) for m in FUTURE_MARKERS | INTENT_MARKERS])
  #   self.pmatcher.add("METAPHORIC", [self.nlp(m) for m in METAPHORIC_MARKERS])

  def extract_many(self, text_or_docs: Sequence[str | Doc], category: Literal["HUMAN", "ORG"]) -> list[str]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc, category=category) for doc in docs]

  def extract(self, text_or_doc: str | Doc, category: Literal["HUMAN", "ORG"]) -> str:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # print("Debug tokenization:", list(self.nlp.tokenizer.explain(text_or_doc)))
    # print("Debug tokens:")
    # pprint([{"token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc if not tok.is_punct])
    # print("Debug ents:", [ent.label_ for ent in doc.ents])
    ents = [
      ent for ent in doc.ents
      if ent.label_ == category and ent.root.pos_ in {"NOUN", "PROPN"}
      and (ent.root.dep_ != "compound" or ent.root.head.lower_.startswith("@"))
      and (ent.root.dep_ != "pobj" or ent.root.head.lower_ == "as")
      and ent.root.dep_ != "dobj"
    ]
    # print("ents:", ents)
    spans: list[Span] = []
    for ent in ents:
      span = find_noun_span(ent, ents)
      if is_hashtagged(ent.root):
        spans.append(span)
      elif not is_negated(ent.root) and not is_past(ent.root) and not is_future(ent.root) and not is_metaphorical(ent.root):
        spans.append(span)
    # Drop overlapping spans (if span.root is in other span – prefer other span)
    # print("spans:", spans)
    spans = [
      span for span in spans
      if not any(span.root in other_span for other_span in spans if other_span != span)
    ]
    # print("spans:", spans)
    return self.format_spans(spans)
    # Note: Initially I planned to keep "former" titles if nothing else is found.
    #       But some forms, e.g. "I was a web engineer" require a reformatting, like
    #       "Ex Web Engineer", which does not fit the current span-only implementation.
    #       It might be changed in future, too complex for now.
    # self.format_subtrees(selected_subtrees) or self.format_subtrees(all_subtrees)

  def format_spans(self, spans: list[Span]) -> str:
    results: list[str] = []
    for ts1 in spans:
      ts2 = list(dropwhile(is_hanging, ts1))
      ts3 = list(dropwhile(is_hanging, reversed(ts2)))
      results.append(""
        .join(get_token_text(tok) + tok.whitespace_ for tok in reversed(ts3))
        .strip()
      )
    return " | ".join(results[0:3]).strip() # the slice length should depend on how long the items are...

  # def pmatch(self, doc_or_span: Doc | Span):
  #   result = self.pmatcher(doc_or_span)
  #   matches: list[tuple[str, int, int]] = []
  #   for match_id, start, end in result:
  #     matches.append(
  #       (self.nlp.vocab.strings[match_id], start, end)
  #     )
  #   return matches

def get_token_text(token: Token) -> str:
  # Ensure that tokens are appended with correct case
  if token.pos_ in {"ADP", "CCONJ", "DET", "PART"}:
    text = str(token).lower()
  elif re.search(r"[A-Z]", token.text):
    text = str(token)
  else:
    text = str(token).title()
  return re.sub(r"^#", "", text)

def is_hanging(token: Token) -> bool:
  return (
    token.lower_ in {"-", "/", ",", ".", "current", "currently", "forever", "now"} or
    token.pos_ in {"ADP", "CCONJ", "DET", "PART", "VERB"}
  )

def find_noun_span(ent: Span, ents: list[Span]) -> Span:
  del ents # not used for now
  # print("@ find_noun_span:", repr(str(ent)))
  doc = ent[0].doc
  root = ent.root
  tokens: list[Token] = []
  for tok in ent.root.sent:
    if tok.is_punct:
      continue
    if (
      tok in ent or # [Developer]
       ( # other_ents // not tok.ent_type_ and
        tok.head == root and tok.i < root.i or # [Senior] Developer, [Senior] PHP Developer
        tok.head.head == root and tok.i < root.i or # [Full]-Stack Developer
        tok.head.head.head == root and tok.i < root.i or # [Game] Engine Development Amateur
        tok.head.head == root and tok.i > root.i and tok.head.lower_ in {"at", "of"} # Founder of [Something]
        # tok.head.head.head.head == root and tok.i > root.i and tok.head.head.head.lower_ in {"at", "of"} # Head of Dev of Some Team
        # ^ alternatively `and tok.head.pos_ == "ADP"` but I indend to drop "by" clauses
      )
    ):
      tokens.append(tok)
  tokens = list(dropwhile(is_hanging, tokens))
  tokens = list(dropwhile(is_hanging, reversed(tokens)))
  tokens = list(reversed(tokens))
  start, end = tokens[0].i, tokens[-1].i + 1
  return doc[start:end]

def is_sorted[T](arr: list[T]) -> bool:
  return sorted(arr) == arr # type: ignore

MORE_GRAMMAR_FIXES: list[tuple[str, str, re.RegexFlag | int]] = [
  (rf"{LB}Professional{RB}", r"professional", 0), # to not receive PROPN by mistake, though will break company names with this word :(
  (rf"{LB}PROFESSIONAL{RB}", r"professional", 0),
  (rf"{LB}Remote{RB}", r"remote", 0), # prevents more serious Spacy bugs
  (rf"{LB}REMOTE{RB}", r"remote", 0),
]

def fix_more_grammar(text: str) -> str:
  for pattern, replacement, flags in MORE_GRAMMAR_FIXES:
    text = re.sub(pattern, replacement, text, count=0, flags=flags)
  return text
