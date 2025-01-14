from ..skill import Skill

SKILLS: list[Skill] = [
  # == Companies not (yet/intentionally) extracted into their own modules ==

  # BIGTECH
  Skill("AMD", ["(@)amd", "amd=32", "amd=64"], "Company"),
  Skill("Autodesk", ["(@)autodesk"], "Company"),
  Skill("eBay", ["(@)ebay"], "Company"),
  Skill("Facebook", ["(@)facebook"], "Company"), # TODO meta?
  Skill("IBM", ["(@)ibm"], "Company"),
  Skill("Intel", ["(@)intel"], "Company"),
  Skill("Kaggle", ["(@)kaggle"], "Company"),
  Skill("Mozilla", ["(@)mozilla"], "Company"),
  Skill("Netflix", ["(@)netflix"], "Company"),
  Skill("NVidia", ["(@)nvidia"], "Company"),
  Skill("SalesForce", ["(@)salesforce"], "Company"),
  Skill("SAP", ["(@)sap"], "Company"),
  Skill("Vercel", ["(@)vercel"], "Company"),
]
