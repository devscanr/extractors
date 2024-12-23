from spacy.tokens import Span

from ...utils import literal, noun
from ..utils import Disambiguate, Skill, neighbour

__all__ = ["SKILLS"]

# def dis_development() -> Disambiguate:
#   blackprec = {
#     """personal", "team"
#   }
#   def disambiguate(ent: Span) -> bool:
#     ent_idxs = {t.i for t in ent}
#     for token in ent.sent:
#       if token.i not in ent_idxs:
#         if token.lower_ in neighbours:
#           return True
#     return False
#   return disambiguate

def dis_design() -> Disambiguate:
  # blacklist = {
  #   "database", "code", "software", "hardware"
  # }
  whitelist = {
    "graphic", "game", "level", "mobile",
    "ui", "uiux", "visual", "web",
  }
  def disambiguate(ent: Span) -> bool:
    ent_idxs = {t.i for t in ent}
    for token in ent.sent:
      if token.i not in ent_idxs:
        if token.lower_ in whitelist:
          return True
    return False
  return disambiguate

def dis_management() -> Disambiguate:
  # TODO categorize all this into people management and __ what?
  whitelist = {
    # "content",
    "engineering",
    "marketing",
    "operations",
    "people", "process", "product", "project",
    # "release",
    # "sales",
    # "team",
    "warehouse",
  }
  def disambiguate(ent: Span) -> bool:
    ent_idxs = {t.i for t in ent}
    for token in ent.sent:
      if token.i not in ent_idxs:
        if token.lower_ in whitelist:
          return True
    return False
  return disambiguate

def dis_test() -> Disambiguate:
  whitelist = {
    "acceptance", "automated", "automation", "case", "cases",
    "documentation", "execution", "execute",
    "e2e", "functional", "integration", "load",
    "management", "manual",
    "suite", "suites", "unit", "write", "writing"
  }
  def disambiguate(ent: Span) -> bool:
    ent_idxs = {t.i for t in ent}
    for token in ent.sent:
      if token.i not in ent_idxs:
        if token.lower_ in whitelist:
          return True
    return False
  return disambiguate

# To consider later
# def res_science() -> Resolve:
#   related_skills = {
#     "Data", "Computer", -- this list should be auto-discovered from the skill set
#   }
#   def resolve(ent: Span) -> list[str]:
#     ent_idxs = {t.i for t in ent}
#     skills = ["Science"]
#     for token in ent.sent:
#       if token.i not in ent_idxs:
#         if token.ent_type_ in related_skills:
#           skills.append(token.ent_type_ + "-Science")
#     return skills
#   return resolve

SKILLS: list[Skill] = [
  Skill("Accessibility", ["accessibility", "accessible"], "Topic"),

  Skill("Administration", ["administration", "administrator", "admin"], "Topic"),

  Skill("AI", ["ai", "artificial-intelligence"], "Topic"),

  Skill("Analysis", ["analysis", "analytics", "analytical", "analyst"], "Topic"),
  # TODO: -"issue analysis"
  # analyses (plural, appears in vacancies)

  Skill("Animation", ["animation", "animated", "animating", "animator"], "Topic"),

  Skill("AR/VR", [
    "augmented=reality", "mixed=reality", "virtual=reality",
    "vr/ar", "vr/mr", "ar/vr", "mr/vr", "vr",
  ], "Topic"),

  Skill("Architecture", ["architecture", "architect"], "Topic"),

  Skill("Art", ["art", "artist"], "Topic"),
  Skill("-Art", ["of arts"]), # Bachelor of Arts

  Skill("Automation", ["automation", "automated", "automatic", "automating"], "Topic"),

  Skill("Backend", ["back=end", "backender", noun("BE")], "Topic"), # not detected as PROPN, needs to be retrained

  Skill("BigData", ["big=data"], "Topic"),

  Skill("Biochemistry", ["bio=chemistry", "bio=chemist"], resolve=["Biology", "Chemistry"]),
  Skill("Bioinformatics", ["bio=informatics", "bio=informatician"], resolve=["Biology", "Informatics"]),

  Skill("Biology", ["biology", "biologist"], "Topic"),

  Skill("Blockchains", [
    "blockchain(s)",
    "on-chain", "off-chain",
    "litecoin",
  ], "Topic"),

  Skill("Business", [
    "business", "entrepreneur", "entrepreneurship", "business-development",
    "b2b", "b2c", "b2b2c",
  ], "Topic"),
  Skill("Business-Analysis", [
    "businessanalysis", "businessanalytics", "businessanalyst"
  ], resolve=["Business", "Analysis"]),
  # TODO business intelligence, BI
  # TODO nonprofit(s) ?

  Skill("Chemistry", ["chemistry", "chemist"], "Topic"),

  Skill("Computer", ["computer", "computing"], "Topic"),
  Skill("Computer-Science", [
    "computerscience", "computerscientist", "comp=sci",
    literal("CS"), "mscs",
  ], resolve=["Computer", "Science"]),
  Skill("Computer-Vision", ["computer=vision"], "Topic", resolve=["Computer", "Vision"]),

  Skill("Commerce", ["commerce", "e=commerce"], "Topic"),

  Skill("Cloud", ["cloud"], "Topic"),
  Skill("Cloud-Architecture", ["cloudarchitecture", "cloudarchitect"], resolve=["Cloud", "Architecture"]),

  Skill("Cross-Platform", ["cross=platform"], "Topic"),

  Skill("Data", ["data"], "Topic"), # maybe a whitelist will work better here
  Skill("-Data", [
    "personal=data", "user=data",
    "my=data", "your=data", "our=data", "their=data",
    "data=graph", "data-querying", "data-storage", # vs database?
  ], resolve=[]), # oversimplified, will update later
  Skill("Data-Analysis", ["dataanalysis", "dataanalytics", "dataanalyst"], resolve=["Data", "Analysis"]),
  Skill("Data-Operations", ["dataoperations", "dataops"], resolve=["Data", "Operations"]),
  Skill("Data-Engineering", [
    "dataengineering", "dataengineer", "datadeveloper", "datadev"
  ], resolve=["Data", "Engineering"]),
  Skill("Data-Security", ["datasecurity", "data=sec", "data=protection"], resolve=["Data", "Security"]),
  Skill("Data-Science", [
    "datascience", "datascientist", "data=sci", literal("DS")
  ], resolve=["Data", "Science"]),
  Skill("Data-Visualization", ["data=viz",], resolve=["Data", "Visualizations"]),

  Skill("Databases", ["database(s)"], "Topic"),
  Skill("Database-Administration", [
    "databaseadministration", "databaseadministrator", "dba"
  ], resolve=["Databases", "Administration"]),
  Skill("Database-Design", [
    "databasedesign", "databasedesigner", "dbdesign", "dbdesigner",
    "databasemodeling", "dbmodeling",
  ], resolve=["Databases", "Modeling"]), #

  Skill("Decentralized", ["decentralized"], "Topic"),

  Skill("Deep-Learning", ["deep=learning", "deep=reinforcement=learning", "dl"], "Topic"), # not sure about FPs for "dl"
  # Signal Processing

  Skill("Desktop", ["desktop"], "Topic"),

  Skill("Distributed", ["distributed"], "Topic"),

  Skill("Design", [
    noun("design"), # too many FPs, need to narrow somehow. A frequent verb.
    "designer",
    "motiondesign", "motiondesigner",
    "visualdesign", "visualdesigner"
  ], "Topic"),

  Skill("Economics", ["economics", "economist"], "Topic"),

  Skill("Education", [
    "edtech", "educator", "e=learning",
    "dean", "prof(essor)", "teacher"
  ], "Topic"), # how to differentiate from "(my) Education:"
  Skill("-Education", ["my-education"], resolve=[]),

  Skill("Electrics", ["electrics", "electrical"], "Topic"),

  Skill("Electronics", ["electronic(s)", "electronical"], "Topic"),

  Skill("Embedded", ["embedded"], "Topic"),
  Skill("Embedded-Engineering", [
    "embeddedengineer", "embeddedprogramming", "embeddeddev",
    # Rare:
    # embeddedengineering, embeddedprogrammer, embeddeddeveloper
  ], resolve=["Embedded", "Engineering"]),

  Skill("Engineering", [
    "engineering", "engineered", "engineer", "eng",
    "coding", "coder",
    "development", "developed", "developer", "dev",
    "programming", "programmer",
  ], "Topic"),
  Skill("-Engineering", [
    "dev=mode", # =dev
    "human development",
    "personal development",
    "team development",
    "development team",
  ], resolve=[]),
  Skill("Engineering-Operations", [
    "devops",
    # Rare:
    # devoperations
  ], resolve=["Engineering", "Operations"]),
  Skill("Engineering-Security-Operations", [
    "dev/sec-ops", "sec/dev-ops",
    "dev-sec-ops", "sec-dev-ops",
    "devsecops", "secdevops", "devopssec",
  ], resolve=["Engineering", "Security", "Operations"]),

  Skill("Finance", [
    "banking", "bankless",
    "finance", "fintech", "financial",
    "payment(s)",
  ], "Topic"),

  Skill("Firmware", ["firmware"], "Topic"),

  Skill("Frontend", ["front=end", "frontender", noun("FE")], "Topic"), # not detected as PROPN, needs to be retrained

  Skill("Fullstack", ["full=stack(er)"], resolve=["Backend", "Frontend"]),

  Skill("Games", [
    "game(s)", "gamer", "gameplay",
    "arcanoid", "minecraft", "tetris", "tictactoe",
  ], "Topic"),
  Skill("-Games", ["game=theory"], resolve=[]), # oversimplified, will update later
  Skill("Game-Design", ["gamedesign", "gamedesigner"], resolve=["Games", "Design"]),
  Skill("Game-Engineering", [
    "gameengineering", "gameengineer",
    "gameprogramming", "gameprogrammer"
    "gamedeveloper", "gamedev"
  ], resolve=["Games", "Engineering"]),
  Skill("Game-Testing", [
    "playtest(s)",
  ], resolve=["Games", "Testing"]),

  Skill("Graphics", ["graphic(s)"], "Topic"),
  Skill("Graphics-Design", ["graphic(s)design", "graphic(s)designer"], resolve=["Graphics", "Design"]),

  Skill("Hardware", ["hardware"], "Topic"),
  Skill("Hardware-Design", ["hardwaredesign", "hardwaredesigner"], resolve=["Hardware", "Design"]),
  Skill("Hardware-Engineering", [
    "hardwareengineering", "hardwareengineer",
    "hardwaredeveloper", "hardwaredev"
  ], resolve=["Hardware", "Engineering"]),

  Skill("Infrastructure", ["infrastructure"], "Topic"),

  Skill("IoT", ["iot", "internet-of-things"], "Topic"),

  Skill("Informatics", ["informatics", "information=science"], "Topic"),

  Skill("Leadership", ["leadership", "leader", "lead", "leading role"], "Topic"),

  Skill("Linguistics", ["linguistics", "linguist"], "Topic"),

  Skill("Low-Code", ["low=code", "no=code"], "Topic"),

  Skill("Machine-Learning", ["machine-learning", "ml"], "Topic"),
  Skill("Machine-Learning-Engineering", ["mlengineer"], resolve=["Machine-Learning", "Engineering"]),
  Skill("Machine-Learning-Operations", ["mlops", "mldevops", "ai=ops"], resolve=["Machine-Learning", "Operations"]),

  Skill("Management", ["management", "manager"], "Topic", disambiguate=dis_management()),

  Skill("Marketing", [
    "marketing", "marketer",
    "seo", "smo",
  ], "Topic"),

  Skill("Mathematics", ["mathematics", "mathematical", "math", "mathematician"], "Topic"),

  Skill("Medicine", [
    "medicine", "medical", "medic",
    "physician",
  ], "Topic"),

  Skill("Mobile", ["mobile", "mobileapp"], "Topic"),
  Skill("Mobile-Design", ["mobiledesign", "mobiledesigner"], resolve=["Mobile", "Design"]),
  Skill("Mobile-Engineering", [
    "mobileengineer",
    "mobileprogramming", "mobileprogrammer",
    "mobiledeveloper", "mobiledev",
    # Rare:
    # mobileengineering
  ], resolve=["Mobile", "Engineering"]),

  Skill("Modeling", ["datamodeling"], "Topic"),

  Skill("Music", [
    "music", "musical", "musician",
    "drummer", "guitarist", "fleutist",
  ], "Topic"),

  Skill("Networks", ["networking", "network(s)"], "Topic"),
  Skill("Network-Operations", [
    "networkoperations", "networkops", "netops",
  ], resolve=["Networks", "Operations"]),
  Skill("Network-Security", ["networksecurity", "netsecurity", "net=sec"], resolve=["Networks", "Security"]),

  Skill("Natural-Language-Processing", ["natural=language=processing", "nlp"], "Topic"),

  Skill("Neural-Networks", ["(deep=)neural-networks", "nn", "dnn"], "Topic"), # not sure about FPs

  Skill("Operations", [
    "operations", "ops",
  ], "Topic"),

  Skill("Politics", ["politics", "political"], "Topic"),

  Skill("Performance", [
    "performance", "performant",
    # "bandwidth", -- also specific to NETWORKS
  ], "Topic"),

  Skill("Photography", ["photography", "photographer"], "Topic"),

  Skill("Product", ["product"], "Topic"),

  Skill("Project", ["project"], "Topic"),

  Skill("QA", ["quality-assurance", "qa"], "Topic"),
  Skill("AQA", ["aqa"], resolve=["Automation", "QA"]),

  Skill("Physics", ["physics", "physical", "physicist"], "Topic"),

  Skill("Recruitment", ["recruitment", "recruiter", "staffing"], "Topic"),

  Skill("Reliability", ["reliability", "reliable"], "Topic"),

  Skill("Research", ["research", "reseacher"], "Topic"),

  Skill("Robotics", ["robotic(s)", "robocon", "rpa"], "Topic"),

  Skill("Scalability", ["scalability", "scalable"], "Topic"),

  Skill("Science", [
    "science(s)", "scientist", "scientific",
    literal("B.S"), literal("M.S")
  ], "Topic"),

  Skill("Scraping", ["scraping", "webscraping"], "Topic"),

  Skill("SDET", ["sdet"], resolve=["Software", "Engineering", "Testing"]),
  Skill("SDLC", ["sdlc"], resolve=["Software", "Engineering", "Testing", "Deployment"]),

  Skill("Security", [
    "security", "secure",
    "defensive", "offensive", "threat", # _ tools, _ techniques, etc.
    "exploit(s)", "malware", "malicious",
    "vulnerability", "vulnerabilities",
  ], "Topic"),
  Skill("Security", ["sec"], disambiguate=neighbour(2)),
  Skill("Security-Operations", [
    "securityoperations", "secops"
    # Rare:
    # secoperations
  ], resolve=["Security", "Operations"]),
  Skill("Security-Cyber", [
    "cyber=security", "cyber=sec", "cyber=defence"
  ], resolve=["Security"]),
  Skill("Security-Information", [
    "information=security", "info=security", "info=sec"
  ], resolve=["Security"]),
  # offensive security, audit

  Skill("Software", ["software", "sw"], "Topic"),
  Skill("Software-Design", ["softwaredesign", "softwaredesigner"], resolve=["Software", "Design"]),
  Skill("Software-Engineering", [
    "softwareengineering", "softwareengineer",
    "softwaredeveloper", "softwaredev",
    # Rare:
    # softwareprogramming,  softwareprogrammer
    literal("SDE"), literal("SWE"), # sometimes SE @_@
  ], resolve=["Software", "Engineering"]),

  Skill("Solution-Architecture", [
    "solution=architecture", "solution=architect"
  ], resolve=["Business", "Architecture"]),

  Skill("Sport", [
    "sport",
    "baseball", "basketball",
    "biking", "biker",
    "snowboarding", "snowboarder",
    "soccer",
    "surfing", "surfer",
    "tennis",
  ], "Topic"),
  # TODO should we drop these topics or use them to justify repository descr. text inclusion
  # along with the bio?! @_@ It's hard to list all terms and such words follow general english
  # grammar (can be lemmatized). Downside: we won't be able to show interests not listed in bio.

  Skill("SRE", [literal("SRE")], resolve=["Reliability", "Engineering"]),

  Skill("Startups", ["startup(s)"], "Topic"),

  Skill("Statistics", [
    "statistic(s)", "statistician", "statistical",
    "correlation", "confidence interval(s)", "hypothesis",
    "probability", "regression", "classification", "clustering",
  ], "Topic"),

  Skill("Systems", ["system(s)"], "Topic"), # TODO many FPs e.g. "information systems"
  Skill("System-Administration", [
    "systemadministration", "systemadministrator", "sysadmin"
  ], resolve=["Systems", "Administration"]),
  Skill("System-Architecture", [
    "systemarchitecture", "systemarchitect"
  ], resolve=["Systems", "Architecture"]),
  Skill("System-Engineering", [
    "systemengineering", "systemengineer",
    "systemprogramming",
    "systemdeveloper", "systemdev",
    # Rare:
    # systemprogrammer
  ], resolve=["Systems", "Engineering"]),
  Skill("System-Operations", [
    "sysops",
    # Rare:
    # systemoperations, systemops
  ], resolve=["Systems", "Operations"]),

  Skill("Telecom", ["telecom", "telecommunication(s)"], "Topic"),

  Skill("Testing", ["testing", "tested", "tester"], "Topic"),
  Skill("Testing", ["test(s)"], disambiguate=dis_test()),
  Skill("-Testing", ["battle-tested", "tested to"], resolve=[]),

  Skill("UI/UX", [
    "ui=ux", "ui/ux", "uix", "ui", "ux", "user=interface", "human=interface", "user=experience"
  ], "Topic"),
  Skill("UI-Design", ["uidesign", "uidesigner", "uxdesign", "uxdesigner"], resolve=["UI/UX", "Design"]),

  Skill("Usability", ["usability", "usable"], "Topic"),

  Skill("Videography", ["videography", "videographer", "video(s)"], "Topic"),
  # Medical Imaging, Audio

  Skill("Visualizations", ["visualization", "visualizer"], "Topic"),

  Skill("Web", ["web", "website", "webapp"], "Topic"),
  Skill("Web3", ["web3"], "Topic"),
  Skill("Web-Design", ["webdesign", "webdesigner"], resolve=["Web", "Design"]),
  Skill("Web-Engineering", [
    "webengineering", "webengineer",
    "webprogramming", "webprogrammer",
    "webdeveloper", "webdev",
    "webcoding", "webcoder",
  ], resolve=["Web", "Engineering"]),
  Skill("Web-Security", ["websecurity", "web=sec"], resolve=["Web", "Security"]),
]

# TODO phpdeveloper, dataarchitect, webarchitect, phpcoder, dbadmin, rubydev

# TODO split into inside (dev) and outside topics

# malware-analysis = security-research

# Skill("Resilience", ["resilience", "resilient"], "Topic"),
# Skill("Observability", ["observability", "observable"], "Topic"),
# Highly Available, High Availability, high performance, high traffic,
# Clustering, Sharding, load balancing
# Replication, Partitioning | Enterprise, large-scale
# Skill("Resiliency", ["resiliency", "resilient"], "Topic"),
#
# Skill("E-Commerce", ["e=commerce"], "Topic"),
# Skill("Cluster", ["cluster"], "Topic"),
# + Logistics
# 3D modeling

# Idea: recognize designers, managers, maybe architects as roles
# Ignore "Design" and "Management" topic as too broad
# Not sure about "Architecture" topic yet
