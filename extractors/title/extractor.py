from itertools import dropwhile
import re
from spacy import Language
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc, Span, Token
from typing import Literal, Sequence
from ..categories.extractor import is_hashtagged
from ..markers import is_future, is_metaphorical, is_negated, is_past
from ..patterns import expand_phrase12
from ..spacyhelpers import token_level
from ..utils import LB, RB, Pattern, literal
from .data import TAGGED_PHRASES

class TitleExtractor:
  def __init__(self, nlp: Language) -> None:
    self.nlp = nlp
    self.matcher = Matcher(self.nlp.vocab)                      # matcher: single word, more verbose syntax than PM but less verbose than DM
    self.pmatcher = PhraseMatcher(self.nlp.vocab, attr="LOWER") # phrases: fastest, no flexibility
    self.init_matchers(TAGGED_PHRASES)

  def init_matchers(self, tagged_phrases: dict[str, list[str | Pattern]]) -> None:
    for tag, phrases in tagged_phrases.items():
      # Update matchers with patterns
      for phrase in phrases:
        if isinstance(phrase, str):
          if "<<" in phrase:
            raise Exception("not supported")
          else:
            if re.search("[A-Z]", phrase):
              self.matcher.add(tag, [literal(p) for p in expand_phrase12(phrase)])
            else:
              self.pmatcher.add(tag, [self.nlp(p) for p in expand_phrase12(phrase)])
        elif isinstance(phrase, list):
          self.matcher.add(tag, [phrase])

  def extract_many(self, text_or_docs: Sequence[str | Doc], fortag: Literal["HUMAN", "ORG"]) -> list[str]:
    docs = self.nlp.pipe(text_or_docs)
    return [self.extract(doc, fortag=fortag) for doc in docs]

  def extract(self, text_or_doc: str | Doc, fortag: Literal["HUMAN", "ORG"]) -> str:
    doc = self.nlp(text_or_doc) if isinstance(text_or_doc, str) else text_or_doc
    # print("Debug tokenization:", list(self.nlp.tokenizer.explain(text_or_doc)))
    # print("Debug tokens:")
    # pprint([{"token": tok, "pos": tok.pos_, "dep": tok.dep_, "head": tok.head} for tok in doc if not tok.is_punct])
    # print("Debug ents:", [ent.label_ for ent in doc.ents])

    raw_matches: list[tuple[str, list[int]]] = []
    matches = self.matcher(doc) if len(self.matcher) else []
    pmatches = self.pmatcher(doc) if len(self.pmatcher) else []
    for match in matches:
      # print("match:", match)
      [match_id, start, end] = match # e.g. "hardware" -> (10100372000430808166, 3, 4)
      tag = self.nlp.vocab.strings[match_id]
      raw_matches.append((tag, list(range(start, end))))
    for pmatch in pmatches:
      # print("pmatch:", pmatch)
      [match_id, start, end] = pmatch # e.g. "hardware-designer" -> (10100372000430808166, 3, 6)
      tag = self.nlp.vocab.strings[match_id]
      raw_matches.append((tag, list(range(start, end))))
    # print("raw_matches:", raw_matches)

    # Resolve overriding matches
    distinct_matches: list[tuple[str, list[int]]] = []
    for tag, offsets in raw_matches:
      other_matches: list[tuple[str, list[int]]] = []
      for tg, ofs in raw_matches:
        if ofs == offsets and tg != tag:
          raise Exception(f"anchors {tag!r} and {tg!r} overlap at {offsets!r}")
        else:
          other_matches.append((tg, ofs))
      if not any(
        True for other_match in other_matches
        # Wider alternative exists
        if set(offsets) < set(other_match[1])
      ):
        distinct_matches.append((tag, offsets))
    # print("distinct_matches:", distinct_matches)

    # Convert to sorted tag-token pairs
    tag_tokens = [
      (tag, token)
      for tag, offsets in distinct_matches
      if (token := doc[min(offsets, key=lambda o: token_level(doc[o]))])
    ]
    tag_tokens.sort(key=lambda tag_token: tag_token[1].i)
    # print("tag_tokens:", tag_tokens)

    # Filter tag-token pairs
    tag_tokens2: list[tuple[str, Token]] = []
    for tag, token in tag_tokens:
      if tag == fortag:
        if token.head.text.startswith("@"):
          tag_tokens2.append((tag, token))
        elif token.dep_ not in {"amod", "compound", "dobj", "pobj"}:
          tag_tokens2.append((tag, token))
        elif token.dep_ == "pobj" and token.head.lower_ == "as": # TODO maybe analize a verb instead
          tag_tokens2.append((tag, token))
    # print("tag_tokens2:", tag_tokens2)

    # Extract spans
    spans: list[Span] = []
    for _, token in tag_tokens2:
      span = find_noun_span(token, spans)
      if is_hashtagged(span.root):
        spans.append(span)
      elif not any(pred(span.root) for pred in [is_negated, is_past, is_future, is_metaphorical]):
        spans.append(span)
    # print("spans:", spans)

    # Drop overlapping spans (if span.root is in other span – prefer other span)
    final_spans = [
      span for span in spans
      if not any(span.root in other_span for other_span in spans if other_span != span)
    ]
    # print("final_spans:", final_spans)

    return self.format_spans(final_spans)
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
  if token.lower_ in {"year", "years", "old", "young", "new"}:
    return True
  if token.pos_ in {"NOUN", "PROPN", "ADJ"}:
    return False
  if token.pos_ == "VERB":
    return token.tag_ != "VBN" # Smth like "embedded" (VBN) -> False, otherwise -> True
  return True

def find_noun_span(token: Token, acc_spans: list[Span]) -> Span:
  # print("@ find_noun_span:", repr(str(token)))
  toks: list[Token] = []
  for tok in token.sent:
    if tok.is_punct:
      continue
    if tok == token:
      toks.append(tok) # [Developer]
    if not any(True for span in acc_spans if tok in span):
      if tok.head == token and tok.i < token.i:
        toks.append(tok) # [Senior] Developer, [Senior] PHP Developer
      elif tok.head.head == token and tok.i < token.i:
        toks.append(tok) # [Full]-Stack Developer
      elif tok.head.head.head == token and tok.i < token.i:
        toks.append(tok) # [Game] Engine Development Amateur
      elif  tok.head.head == token and tok.i > token.i and tok.head.lower_ in {"at", "of"}:
        # Not comparing with pos=ADP to intentionally drop "by" and other adps.
        toks.append(tok) # Founder of [Something]
  toks = list(dropwhile(is_hanging, toks))
  toks = list(dropwhile(is_hanging, reversed(toks)))
  toks = list(reversed(toks))
  if len(toks):
    start, end = toks[0].i, toks[-1].i + 1
    return token.doc[start:end]
  else:
    return token.doc[0:0]

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
