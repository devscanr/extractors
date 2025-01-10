from ..utils import Topic, dis_context

SKILLS: list[Topic] = [
  # PROCESSES / INDUSTRIES
  Topic("Administration", ["administration", "administrator", "admin"]),

  Topic("Analysis", ["analysis", "analytics", "analytical", "analyst"]),
  # TODO: -"issue analysis"
  # analyses (plural, appears in vacancies)

  Topic("Architecture", ["architecture", "architect"]),

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
    "font << design", "font << designer",
    "level << design", "level << designer",
    "motion << design", "motion << designer",
    "visual << design", "visual << designer",
  ]), # Other design types are captured in topics

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
  ], resolve=[]),

  Topic("Management", [
    "people << management", "people << manager",
    "process << management", "process << manager",
    "product << management", "product << manager",
    "project << management", "project << manager",
    "release << management", "release << manager",
    "sales << management", "sales << manager",
    "team << management", "team << manager",
  ]),
  Topic("-Management", [
    # These rules are not necessary, mostly a reminder
    "content=management", "session=management",
  ]),
  # Other design types are captured in topics

  Topic("Marketing", [
    "marketing", "marketer",
    "seo", "smo", "advertising", "advertisement",
  ]),

  Topic("Operations", ["operations", "ops"]),

  Topic("Research", ["research", "reseacher"]),

  Topic("Testing", ["testing", "tested", "tester"]),
  Topic("Testing", ["test(s)"], disambiguate=dis_context(
    "acceptance", "automated", "automation", "case", "cases",
    "documentation", "execution", "execute",
    "e2e", "functional", "integration", "load",
    "management", "manual",
    "suite", "suites", "unit", "write", "writing"
  )),
  Topic("-Testing", ["battle-tested", "tested to"], resolve=[]),

  # SCIENCES / STUDIES / MATHS
  Topic("Anthropology", ["anthropology", "anthropologist"]),
  Topic("Astronomy", ["astronomy", "astronomer"]),

  Topic("Biology", ["biology", "biologist"]),
  Topic("Biochemistry", ["bio=chemistry", "bio=chemist"], resolve=["Biology", "Chemistry"]),
  Topic("Bioinformatics", ["bio=informatics", "bio=informatician"], resolve=["Biology", "Informatics"]),
  Topic("Biomedicine", ["bio=medicine", "bio=medic"], resolve=["Biology", "Medicine"]),

  Topic("Chemistry", ["chemistry", "chemist"]),

  Topic("Computer-Science", [
    "computer << science", "computer << scientist", "comp=sci",
    "CS", "mscs",
  ]),

  Topic("Data-Science", [
    "data << science",
    "data << scientist", "data=sci",
    # "DS", "msds",
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
    "correlation", "confidence interval(s)", "hypothesis",
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
  Topic("-Education", ["my-education"], resolve=[]),

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

  # BROAD ENGINEERING TOPICS
  Topic("Electrical-Engineering", ["electrical=engineering", "electrical", "electric(s)"]),

  Topic("Electronics", ["electronic(s)", "electronical"]),

  Topic("Hardware", ["hardware"]), # "HW"
  Topic("Hardware-Design", [
    "hardware << design", "hardware << designer",
  ], resolve=["Hardware", "Engineering"]),
  Topic("Hardware-Engineering", [
    "hardwareengineering", "hardwareengineer",
    "hardwaredevelopment", "hardwaredeveloper", "hardwaredev",
    "HWE",
  ], resolve=["Hardware", "Engineering"]),

  Topic("Infrastructure", ["infrastructure"]),

  Topic("Networks", ["networking", "network(s)"]),
  Topic("Internet", ["internet", "www"]),

  Topic("Robotics", ["robotic(s)", "robocon", "rpa"]),

  Topic("Software", [
    "software", "sw",
    "programming", "programmer",
    "coding", "coder",
  ]),
  Topic("Software-Achitecture", [
    "softwarearchitecture", "softwarearchitect",
  ], resolve=["Software", "Engineering"]),
  Topic("Software-Design", [
    "software << design", "software << designer",
  ], resolve=["Software", "Engineering"]),
  Topic("Software-Engineering", [
    "softwareengineering", "softwareengineer",
    "softwaredevelopment", "softwaredeveloper", "softwaredev",
    "SDE", "SWE", # sometimes SE @_@
  ], resolve=["Software", "Engineering"]),
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
