from ...skills.utils import dis_context
from ..tag import Skill, Topic

SKILLS: list[Skill] = [
  # PROCESSES / INDUSTRIES / DEV SUB-INDUSTRIES
  Topic("Administration", ["administration", "administrator", "admin"]),
  Topic("Administration.Databases", [
    "databaseadministration", "databaseadministrator", "dba"
  ], resolve=["Administration", "Databases"]),
  Topic("Administration.Systems", [
    "systemadministration", "systemadministrator", "sysadmin"
  ], resolve=["Administration", "Systems"]),

  Topic("Analysis", ["analysis", "analytics", "analytical", "analyst"]),
  Topic("Analysis.Business", [
    "businessanalysis", "businessanalytics", "businessanalyst"
  ], resolve=["Analysis", "Business"]),
  Topic("Analysis.Data", [
    "dataanalysis", "dataanalytics", "dataanalyst"
  ], resolve=["Analysis", "Data"]),
  # TODO: -"issue analysis"
  # analyses (plural, appears in vacancies)
  # TODO business intelligence, BI
  # TODO nonprofit(s) ?

  Topic("Architecture", ["architecture", "architect"]),
  Topic("Architecture.Cloud", ["cloudarchitecture", "cloudarchitect"], resolve=["Architecture", "Cloud"]),
  Topic("Architecture.Data", ["dataarchitecture", "dataarchitect"], resolve=["Architecture", "Data"]),
  Topic("Architecture.Games", ["gamearchitecture", "gamearchitect"], resolve=["Architecture", "Games"]),
  Topic("Architecture.Security", ["securityarchitecture", "securityarchitect"], resolve=["Architecture", "Security"]),
  Topic("Architecture.Solutions", [
    "solution=architecture", "solution=architect"
  ], resolve=["Architecture", "Software", "Business"]),
  Topic("Architecture.Systems", [
    "systemarchitecture", "systemarchitect"
  ], resolve=["Architecture", "Systems"]),
  # UI Architect
  Topic("Architecture.Web", ["webarchitecture", "webarchitect"], resolve=["Architecture", "Web"]),

  Topic("Art", ["art", "artist"]),
  Topic("-Art", ["of arts"]), # Bachelor of Arts

  Topic("Automation", ["automation", "automated", "automatic", "automating"]),

  Topic("Business", [
    "business", "entrepreneur", "entrepreneurship", "business-development",
    "b2b", "b2c", "b2b2c",
  ]),
  Topic("Commerce", ["(e=)commerce"]),
  Topic("Startups", ["startup(s)", "startuper"]),

  Topic("Design", [
    "font<~design", "font<~designer",
    "level<~design", "level<~designer",
    "motion<~design", "motion<~designer",
    "visual<~design", "visual<~designer",
  ]),
  Topic("Design.Games", [
    "game(s)<~design", "game(s)<~designer",
  ], resolve=["Design", "Games"]),
  Topic("Design.Graphics", [
    "graphic(s)<~design", "graphic(s)<~designer",
  ], resolve=["Graphics", "Design"]),
  Topic("Design.UI/UX", [
    "ui<~design", "ui<~designer",
    "ux<~design", "ux<~designer",
    "uiux<~design", "uiux<~designer",
  ], resolve=["Design", "UI/UX"]),
  Topic("Web-Design", [
    "web<~design", "web<~designer",
  ], resolve=["Design", "Web"]),

  Topic("Engineering", [
    "engineering", "engineered", "engineer", "eng",
    "development", "developer", "dev",
    "reverse=engineering",
  ]),
  Topic("-Engineering", [
    "dev=mode", # =dev
    "human development",
    "personal development",
    "team development",
    "development team",
  ]),
  Topic("Engineering.Data", [
    "data<~design", "data<~designer",
    "dataengineering", "dataengineer",
    "datadeveloper", "datadev",
  ], resolve=["Engineering", "Data"]),
  Topic("Engineering.Databases", [
    "database<~architecture", "database<~architect",
    "database<~design", "database<~designer",
    "databaseengineering", "databaseengineer", "db=engineering",
    "database=modeling", "db=modeling",
    "db=design", "db=designer",
  ], resolve=["Engineering", "Databases"]),
  Topic("Engineering.Embedded", [
    "embeddedengineer", "embeddedprogramming", "embeddeddev",
  ], resolve=["Engineering", "Embedded"]),
  Topic("Engineering.Games", [
    "gameengineering", "gameengineer",
    "gameprogramming", "gameprogrammer",
    "gamedeveloper", "gamedev",
  ], resolve=["Engineering", "Games"]),
  Topic("Engineering.Hardware", [
    "hardware<~architecture", "hardware<~architect",
    "hardware<~design", "hardware<~designer",
    "hardwareengineering", "hardwareengineer",
    "hardwaredevelopment", "hardwaredeveloper", "hardwaredev",
    "HWE",
  ], resolve=["Engineering", "Hardware"]),
  Topic("Engineering.Machine-Learning", ["ml=engineer(ing)"], resolve=["Engineering", "Machine-Learning"]),
  Topic("Engineering.Mobile", ["mobiledev", "mobiledeveloper", "mobileengineer"], resolve=["Engineering", "Mobile"]),
  Topic("Engineering.Networks", ["network(s)dev", "network(s)developer", "network(s)engineer"], resolve=["Engineering", "Networks"]),
  Topic("Engineering.Operations", ["devop(s)"], resolve=["Engineering", "Operations"]),
  Topic("Engineering.Security.Operations", [
    "dev/sec-ops", "sec/dev-ops",
    "dev-sec-ops", "sec-dev-ops",
    "devsecop(s)", "secdevop(s)", "devop(s)sec",
  ], resolve=["Engineering", "Security", "Operations"]),
  Topic("Engineering.Software", [
    "software<~architecture", "software<~architect",
    "softwareengineering", "softwareengineer",
    "softwaredevelopment", "softwaredeveloper", "softwaredev",
    "SDE", "SWE", # sometimes SE @_@
    "software<~design", "software<~designer",
  ], resolve=["Engineering", "Software"]),
  Topic("Engineering.Systems", [
    "systemengineering", "systemengineer",
    "systemprogramming",
    "systemdeveloper", "systemdev",
  ], resolve=["Engineering", "Systems"]),
  Topic("Engineering.Web", [
    "webengineering", "webengineer",
    "webprogramming", "webprogrammer",
    "webdeveloper", "webdev",
    "webcoding", "webcoder",
  ], resolve=["Engineering", "Web"]),
  # TODO backenddev frontenddev fullstackdev

  Topic("Management", [
    "people<~management", "people<~manager",
    "process<~management", "process<~manager",
    "product<~management", "product<~manager",
    "project<~management", "project<~manager",
    "release<~management", "release<~manager",
    "sales<~management", "sales<~manager",
    "team<~management", "team<~manager",
  ]),
  Topic("-Management", [
    # These rules are not necessary, mostly a reminder
    "content=management", "session=management",
  ]),
  Topic("Management.Engineering", [
    "engineering<~management", "engineering<~manager",
  ], resolve=["Management", "Engineering"]),
  Topic("Management.Marketing", [
    "marketing<~management", "marketing<~manager",
  ], resolve=["Management", "Marketing"]),
  Topic("Management.Operations", [
    "operations<~management", "operations<~manager",
  ], resolve=["Management", "Operations"]),
  Topic("Management.Warehouses", [
    "warehouse<~management", "warehouse<~manager",
  ], resolve=["Management", "Warehouses"]),

  Topic("Marketing", [
    "marketing", "marketer",
    "seo", "smo", "advertising", "advertisement",
  ]),

  Topic("Mobile", ["mobile", "mobileapp"]),
  Topic("Mobile-Engineering", [
    "mobile<~developer", "mobile<~dev",
    "mobile<~engineer",
    "mobile<~programming", "mobile<~programmer",
    "mobile<~design", "mobile<~designer", # Mobile-Design is not UI-Design
  ], resolve=["Mobile", "Engineering"]),

  Topic("Operations", ["operations", "ops"]),
  Topic("Operations.Data", ["dataoperations", "dataop(s)"], resolve=["Operations", "Data"]),
  Topic("Operations.Machine-Learning", ["mlop(s)", "mldevop(s)", "ai=op(s)"], resolve=["Operations", "Machine-Learning"]),
  Topic("Operations.Networks", ["network(s)operations", "networkop(s)", "netop(s)"], resolve=["Operations", "Networks"]),
  Topic("Operations.Security", ["securityoperations", "secop(s)"], resolve=["Operations", "Security"]),
  Topic("Operations.Systems", ["system(s)operations", "sysop(s)"], resolve=["Operations", "Systems"]),

  Topic("Research", ["research", "reseacher"]),

  Topic("Testing", ["testing", "tested", "tester"]),
  Topic("Testing", ["test(s)"], disambiguate=dis_context(
    "acceptance", "automated", "automation", "case", "cases",
    "documentation", "execution", "execute",
    "e2e", "functional", "integration", "load",
    "management", "manual",
    "suite", "suites", "unit", "write", "writing"
  )),
  Topic("-Testing", ["battle-tested", "tested to"]),
  Topic("Games-Testing", [
    "playtest(s)",
  ], resolve=["Games", "Testing"]),
  Topic("UI/UX-Testing", [
    "uitesting", "uitester",
    "uxtesting", "uxtesting",
  ], resolve=["UI/UX", "Testing"]),

  # SCIENCES / STUDIES / MATHS
  Topic("Anthropology", ["anthropology", "anthropologist"]),
  Topic("Astronomy", ["astronomy", "astronomer"]),

  Topic("Biology", ["biology", "biologist"]),
  Topic("Biochemistry", ["bio=chemistry", "bio=chemist"], resolve=["Biology", "Chemistry"]),
  Topic("Bioinformatics", ["bio=informatics", "bio=informatician"], resolve=["Biology", "Informatics"]),
  Topic("Biomedicine", ["bio=medicine", "bio=medic"], resolve=["Biology", "Medicine"]),

  Topic("Chemistry", ["chemistry", "chemist"]),

  Topic("Computer-Science", [
    "computer(s)<~science", "computer<~scientist",
    "comp=sci", "CS",
    "ms=cs", "bs=cs", "m.s=cs", "b.s=cs",
  ]),

  Topic("Data-Science", [
    "data<~science", "data<~scientist",
    "data=sci", # "DS"
    "ms=ds", "bs=ds", "m.s=ds", "b.s=ds",
  ]),

  Topic("Cryptography", ["cryptography"]),

  Topic("Ecology", ["ecology", "ecologist"]),

  Topic("Economics", ["economics", "economist"]),

  Topic("Geography", ["geography", "geographist"]),

  Topic("Geology", ["geology", "geologist"]),

  Topic("Informatics", ["informatics", "informatician", "information=science"]),

  Topic("Linguistics", ["linguistics", "linguist"]),

  Topic("Mathematics", [
    "mathematics", "mathematical", "mathematician", "math(s)",
  ]),
  Topic("Algebra", ["algebra", "algebraist"]),
  Topic("Geometry", ["geometry", "geometer"]),
  Topic("Statistics", [
    "statistic(s)", "statistician", "statistical",
    "correlation", "confidence interval(s)", "hypothesis", "hypotheses",
    "probability", "regression", "classification", "clustering",
  ]),
  # TODO more terms: calculus, theories, etc.

  Topic("Physics", ["physics", "physical", "physicist"]),

  Topic("Psychology", ["psychology", "psychologist"]),

  Topic("Sociology", ["sociology", "sociologist"]),

  # INDUSTRIES
  Topic("Cinematography", [
    "cinematography", "cinema",
  ]),

  Topic("Education", [
    "edtech", "educator", "e=learning",
    "dean", "prof(essor)", "teacher"
  ]),
  Topic("-Education", ["my-education"]),

  Topic("Finance", [
    "banking", "bankless",
    "finance", "fintech", "financial",
    "payment(s)",
  ]),

  Topic("Energy", ["energy"]),

  Topic("Entertainment", ["entertainment"]),

  Topic("Healthcare", ["healthcare"]),
  Topic("Medicine", [
    "medicine", "medical", "medic",
    "physician",
  ]),
  Topic("Pharmacy", ["pharmacy", "pharmacist"]),

  Topic("HR", ["hr"]),
  Topic("Recruitment", ["recruitment", "recruiter", "staffing"]),

  Topic("Logistics", ["logistics", "logistician"]),
  Topic("Transport", ["transport", "transportation"]),

  Topic("Music", [
    "music", "musical", "musician",
    "drummer", "guitarist", "fleutist",
  ]),

  Topic("Photography", ["photography", "photographer"]),

  Topic("Politics", ["politics", "political"]),

  Topic("Science", [
    "science(s)", "scientist", "scientific",
    # "B.S", "M.S"
  ]),

  Topic("Security", [
    "security", "secure",
    "defensive", "offensive",
    "threat",
  ]),
  # Topic("Security", ["sec"], disambiguate=neighbour(2)),
  Topic("Security.Data", ["datasecurity", "data=sec", "data=protection"], resolve=["Security", "Data"]),
  Topic("Security.Networks", ["networksecurity", "netsecurity", "net=sec"], resolve=["Security", "Networks"]),
  Topic("Security.Web", ["websecurity", "web=sec"], resolve=["Security", "Web"]),

  Topic("Sport", [
    "sport",
    "baseball", "basketball",
    "biking", "biker",
    "snowboarding", "snowboarder",
    "soccer",
    "surfing", "surfer",
    "tennis",
  ]),
  # TODO should we drop these topics or use them to justify repository descr. text inclusion
  # along with the bio?! @_@ It's hard to list all terms and such words follow general english
  # grammar (can be lemmatized). Downside: we won't be able to show interests not listed in bio.

  Topic("Telecom", ["telecom", "telecommunication(s)"]),

  Topic("Travel", ["travel(s)"]),

  # BROAD TOPICS
  Topic("Blockchains", [
    "blockchain(s)",
    "on-chain", "off-chain",
    "litecoin",
  ]),

  Topic("Computer", ["computer(s)", "computing"]),
  # Note: to be able to name this "Computer" and still be captured by "Computer-Science"
  # we have to split dpattern rules like:
  # == probably applies only to <~ and more complex patterns ==
  # Computer-Science {LOWER: computerscience}
  # Computer-Science {LOWER: computer}<-{LOWER: science}
  # Computer-Science:1 {LOWER: computer}<-{NOUN} {CONJ} {science} omit offsets [1, 2]
  # Computer-Science:2 -- other complex rule -- omit some offsets
  # Then, perhaps in a separate step after match, drop those "omit offsets"
  # If we do this, we might not need exclusive/inclusive differentiation at all

  Topic("Data", ["data"]), # maybe a whitelist will work better here
  Topic("-Data", [
    "personal=data", "user=data",
    "my=data", "your=data", "our=data", "their=data",
    "data=graph", "data-querying", "data-storage", # vs database?
  ], resolve=[]), # oversimplified, will update later

  Topic("Databases", ["database(s)"]),

  Topic("Electrics", ["electrical", "electric(s)"]),

  Topic("Electronics", ["electronic(s)", "electronical"]),

  Topic("Games", [
    "game(s)", "gamer", "gameplay",
    "arcanoid", "minecraft", "tetris", "tictactoe",
    "single=player", "multi-player",
  ]),
  Topic("-Games", ["game=theory"]), # oversimplified, will update later

  Topic("Graphics", ["graphic(s)"]),

  Topic("Hardware", ["hardware"]), # "HW"

  Topic("Infrastructure", ["infrastructure"]),

  Topic("Machine-Learning", ["machine-learning", "ml"]),

  Topic("Networks", ["networking", "network(s)"]),

  Topic("Internet", ["internet", "www"]),

  Topic("Robotics", ["robotic(s)", "robocon", "rpa"]),

  Topic("Software", [
    "software", "sw",
    "programming", "programmer",
    "coding", "coder",
  ]),

  Topic("Web", ["web", "website", "webapp"]),
]

# Academy (doc, post-doc, etc)
# Aviation
# Entertainment
# Environment, Environmental
# Healthcare
# Media & News
# Military
# Shipping
# Trading
