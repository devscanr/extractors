from ...xpatterns import ver1
from ..skill import Skill

SKILLS: list[Skill] = [
  Skill("Adobe", ["(@)adobe"], "Company"),

  # Low-Code
  Skill("Adobe-Commerce", ["adobe=commerce", "magento-enterprise", ver1("magento")], ""),
  Skill("Adobe-CC", ["adobe=cc", "adobe=creative=cloud"], ""),
  Skill("Adobe-Illustrator", ["adobe=illustrator"], ""), # TODO disambig. Illustrator
  Skill("Adobe-Photoshop", ["adobe=photoshop", "photoshop"], ""),
]
