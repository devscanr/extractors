from spacy.tokens import Span, Token

Span.set_extension("used", default=False)
Token.set_extension("i", default=None)

# from .category import Categorizer
# from .phone import parse_phones
# from .email import parse_emails
# from .freelancer import FreelancerParser
# from .language import detect_language_iso639
# from .nondev import NondevParser
# from .student import StudentParser
# from .web import html2text, markdown2text
#
# __all__ = [
#   # Phone/Email parsers
#   "parse_phones",
#   "parse_emails",
#
#   # Human language parser
#   "detect_language_iso639",
#
#   # Categorizers
#   "Categorizer",
#   "FreelancerParser",
#   "NondevParser",
#   "StudentParser",
#
#   # Web Utils
#   "html2text",
#   "markdown2text"
# ]
