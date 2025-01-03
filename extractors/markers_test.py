from . import markers
from .utils import fix_grammar, get_nlp, normalize

nlp = get_nlp()

def is_hashtagged(text: str, i: int) -> bool:
  ntext = fix_grammar(normalize(text))
  return markers.is_hashtagged(nlp(ntext)[i])

def is_negated(text: str, i: int) -> bool:
  ntext = fix_grammar(normalize(text))
  return markers.is_negated(nlp(ntext)[i])

def is_past(text: str, i: int) -> bool:
  ntext = fix_grammar(normalize(text))
  return markers.is_past(nlp(ntext)[i])

def is_future(text: str, i: int) -> bool:
  ntext = fix_grammar(normalize(text))
  return markers.is_future(nlp(ntext)[i])

def describe_is_hashtagged() -> None:
  def it_works() -> None:
    assert not is_hashtagged("Developer", 0)
    assert not is_hashtagged("A developer", 1)
    assert not is_hashtagged("I am a developer", 3)
    assert is_hashtagged("#developer", 1)
    assert is_hashtagged("#web-developer", 1)

def describe_is_negated() -> None:
  def it_handles_no_indicators() -> None:
    assert not is_negated("Developer", 0)
    assert not is_negated("A developer", 1)
    assert not is_negated("I am a developer", 3)

  def it_handles_not_indicators() -> None:
    assert is_negated("not developer", 1)
    assert is_negated("not a developer", 2)
    assert is_negated("I am not a developer", 4)

  def it_handles_non_indicators() -> None:
    assert is_negated("non developer", 1)
    assert is_negated("non-developer", 2)

def describe_is_past() -> None:
  def it_handles_no_indicators() -> None:
    assert not is_past("Non-developer", 2)
    assert not is_past("Developer", 0)
    assert not is_past("A developer", 1)
    assert not is_past("I am a developer", 3)
    assert not is_past("I will be a developer", 4)

  def it_handles_ex_indicators() -> None:
    assert is_past("ex developer", 1)
    assert is_past("ex. developer", 1)
    assert is_past("ex-developer", 1)
    assert is_past("ex-web developer", 2)

  def it_handles_past_indicators() -> None:
    assert is_past("Former developer", 1)
    assert is_past("A former developer", 2)
    assert is_past("Retired developers", 1)
    assert is_past("A retired developer", 2)
    assert is_past("Previously a developer at Facebook", 2)

  def it_handles_was_indicator() -> None:
    assert is_past("Previously I was a developer at Facebook", 4)
    assert is_past("I was developer", 2)
    assert is_past("I was a developer", 3)
    assert is_past("We were developers", 2)

  def it_handles_complex_cases1() -> None:
    text = "I was a developer now I am a manager"
    assert is_past(text, 3)     # developer
    assert not is_past(text, 8) # manager

  def it_handles_complex_cases2() -> None:
    text = "Today I'm developer yet I was manager"
    assert not is_past(text, 3) # developer
    assert is_past(text, 7)     # manager

  def it_handles_complex_cases3() -> None:
    text = "Former developer, currently a manager"
    assert is_past(text, 1)     # developer
    assert not is_past(text, 5) # manager

def describe_is_future() -> None:
  def it_handles_no_indicators() -> None:
    assert not is_future("Non-developer", 2)
    assert not is_future("Developer", 0)
    assert not is_future("A developer", 1)
    assert not is_future("I am a developer", 3)
    assert not is_future("I was a developer", 3)

  def it_handles_future_indicators() -> None:
    assert is_future("Future developer", 1)
    assert is_future("A future developer", 2)
    assert is_future("Aspiring developer", 1)
    assert is_future("An aspiring developer", 2)
    assert is_future("Upcoming developer", 1)
    assert is_future("An upcoming developer", 2)

  def it_handles_future_shortcuts() -> None:
    assert is_future("Wannabe developer", 1)
    assert is_future("Gonnabe developer", 1)
    assert is_future("Developer wannabe", 0)

  def it_handles_will_indicators() -> None:
    assert is_future("I will be developer", 3)
    assert is_future("I will be a developer", 4)
    assert is_future("I will become developer", 3)
    assert is_future("I will become a developer", 4)
    assert is_future("I'll be developer", 3)
    assert is_future("I'll be a developer", 4)

  def it_handles_plan_indicators() -> None:
    assert is_future("Want to be a developer", 4)
    assert is_future("I plan to become developer", 4)
    assert is_future("I wish to be a developer", 5)
    assert is_future("Planning to be the developer", 4)
    assert is_future("Carl wants to be a developer", 5)
    assert is_future("Planning to become a developer", 4)
    assert is_future("Striving to become a developer", 4)
    assert is_future("I strive to be a developer", 5)
    assert is_future("Going to become developer", 3)
    assert is_future("Going to become a developer", 4)
    assert is_future("Gonna be developer", 3) # Tokenization yields [Gon, na]
    assert is_future("Gonna become a developer", 4) # Tokenization yields [Gon, na]
