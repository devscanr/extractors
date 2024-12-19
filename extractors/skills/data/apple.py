# from ...utils import propn
from ..utils import Skill #, contextual, contextual_or_neighbour, neighbour

__all__ = ["SKILLS"]

SKILLS: list[Skill] = [
  Skill("Apple", ["(@)apple"], "Company"),

  # DESIGN
  # Skill("Sketch", ["sketch"], ""), many FPs, need to disambig.

  # MOBILE
  Skill("Objective-C", ["objective=c", "objective=c++", "objective=cpp"], ""),
  Skill("Swift", ["swift"], ""),
  Skill("AppKit", ["appkit"], "Framework"),
  Skill("SwiftUI", ["swiftui"], "Framework"),
  Skill("UIKit", ["uikit"], "Framework"),

  # OS
  Skill("iOS", ["ios"], ""),
  Skill("iPadOS", ["ipados"], ""),
  Skill("tvOS", ["tvos"], ""),
  Skill("watchOS", ["watchos"], ""),

  # DEVICES
  Skill("iMac", ["imac"], ""),
  Skill("iPad", ["ipad"], ""),
  Skill("iPhone", ["iphone"], ""),
  Skill("iWatch", ["iwatch"], ""),
]
