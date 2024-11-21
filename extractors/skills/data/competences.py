from spacy.tokens import Span
from ...utils import get_cons_words, literal, noun, propn
from ..utils import Disambiguate, Skill, neighbour

__all__ = ["SKILLS"]

GAMEDEV_MARKERS = {
  "design", "designer",
  "art", "artist",
  "development", "dev", "developer",
  "engineering", "eng", "engineer",
  "programming", "programmer",
  "hacker", "hacking", "tester", "testing",
  "assets", "engine", "security",
  "research", "researcher" # like "game AI researcher"
}
# "creating|making|developing games" -- left side

NON_GAMEDEV_MARKERS = {"theory"}

DATA_MARKERS = {
  "ai",
  "analysis", "analytics", "analyst",
  "architecture",
  "backed",
  "science", "scientist",
  "research", "researcher",
  "engineering", "eng", "engineer",
  "security", "protection",
  "professional", "specialist", "generalist"
}

def gamedev() -> Disambiguate:
  def disambiguate(ent: Span) -> bool:
    cons_words = [token.lower_ for token in get_cons_words(ent[-1])]
    if any(True for word in cons_words if word in GAMEDEV_MARKERS):
      if not any(True for word in cons_words if word in NON_GAMEDEV_MARKERS):
        return True
    return False
  return disambiguate

def datascience() -> Disambiguate:
  def disambiguate(ent: Span) -> bool:
    cons_words = [token.lower_ for token in get_cons_words(ent[-1])]
    if any(True for word in cons_words if word in DATA_MARKERS):
      return True
    return False
  return disambiguate

SKILLS: list[Skill] = [
  # SOFTWARE ENGINEERING
  Skill("Agile", ["agile", "kanban", "scrum"], "Competence"),
  Skill("TDD", ["tdd"], "Competence"),
  Skill("BDD", ["ddd"], "Competence"),
  Skill("DDD", ["ddd"], "Competence"),
  Skill("FP", ["functional progamming", "fp", "фп"], "Competence"),
  Skill("OOP", ["object=oriented( programming)", "oop", literal("SOLID"), "ооп"], "Competence"),
  # YAGNI, DRY, KISS, MVC

  Skill("Backend", ["back=end(er)", noun("BE")], "Competence"),   # not detected as PROPN, needs to be retrained
  Skill("API", ["api"], "Competence"),
  Skill("ORM", ["orm"], "Competence"),
  Skill("REST", ["rest=api", propn("rest"), noun("REST")], "Competence"),
  Skill("REST", ["rest"], "Competence", disambiguate=neighbour(2)),
  Skill("RPC", ["rpc=api", "rpc"], "Competence"),
  Skill("SOAP", ["soap"], "Competence"),
  Skill("gRPC", ["grpc"], "Competence"),
  Skill("SSG", ["ssg"], "Competence"),
  Skill("SSR", ["ssr"], "Competence"),
  Skill("tRPC", ["trpc"], "Competence"),

  # FRONTEND
  Skill("Frontend", ["front=end(er)", noun("FE")], "Competence"), # not detected as PROPN, needs to be retrained
  # BEM, БЭМ
  Skill("DOM", ["dom"], "Competence"),
  Skill("UI/UX", ["ui", "ux", "user-interface", "user-experience"], "Competence"),
  Skill("Browser", ["browser"], "Competence"),
  Skill("DevTools", ["dev=tools"], "Competence"),
  Skill("MPA", ["mpa"], "Competence"),
  Skill("SPA", ["spa"], "Competence"),
  Skill("OpenAPI", ["openapi"], "Competence"),
  Skill("IP", ["ip"], "Competence"),
  Skill("TCP", ["tcp"], "Competence"),
  Skill("HTTP", ["http"], "Competence"),
  Skill("HTTPS", ["https"], "Competence"),
  Skill("WebGL", ["webgl"], "Competence"),
  Skill("WebSocket", ["websocket", "ws"], "Competence"),

  Skill("Web", ["web", "website(s)", "webdev"], "Competence"),
  Skill("Fullstack", ["full=stack(er)"], "Competence"),

  Skill("Blockchain", ["blockchain"], "Competence"),
  Skill("dApps", ["decentralized-application(s)", "dapp(s)"], "Competence"),
  Skill("DeFi", ["decentralized-finance", "de=fi"], "Competence"),
  Skill("Web3", ["web3"], "Competence"),
  Skill("Crypto", ["crypto"], "Competence"),
  Skill("P2P", ["peer=2=peer", "peer=to=peer", "p2p"], "Competence"),

  # LOW-CODE
  Skill("Low-Code", ["low=code", "no=code"], "Competence"),
  Skill("CMS", ["content-management-system", "cms"], "Competence"),
  Skill("CRM", ["crm"], "Competence"),
  Skill("IaaS", ["iaas"], "Competence"), # INFRASTRUCTURE
  Skill("PaaS", ["paas"], "Competence"), # INFRASTRUCTURE
  Skill("SaaS", ["saas"], "Competence"),

  # MOBILE
  Skill("Mobile", ["mobile", "mobiledev"], "Competence"),
  Skill("Cross-Platform", ["cross=platform"], "Competence"),

  # GAMEDEV
  Skill("Game", ["gamedev"], "Competence"),
  Skill("Game", ["game(s)"], "Competence", disambiguate=gamedev()),

  # DATABASE
  Skill("Database", ["database(s)"], "Competence"),

  # PL/QL UMBRELLAS
  Skill("Assembly", ["assembly"], "Competence"),
  Skill("GraphQL", ["graphql"], "Competence"),
  Skill("SQL", ["sql"], "Competence"),
  Skill("NoSQL", ["nosql"], "Competence"),

  # INFRASTRUCTURE
  Skill("Infrastructure", ["infrastructure"], "Competence"),
  Skill("CI/CD", ["continuous-integration", "ci/cd", "ci"], "Competence"),
  Skill("Cloud", ["cloud"], "Competence"),
  Skill("Orchestration", ["orchestration"], "Competence"),

  # QA & AUTOMATION
  Skill("QA", ["quality-assurance", "qa"], "Competence", stack=["Automation", "Testing"]),
  Skill("E2E-Testing", ["e2e-testing", "e2e=test(s)", "e2e"], "Competence"),
  Skill("Unit-Testing", ["unit-testing", "unit=test(s)"], "Competence"),
  Skill("Integration-Testing", ["integration-testing", "integration=test(s)"], "Competence"),
  Skill("Functional-Testing", ["functional-testing", "functional=test(s)"], "Competence"),
  Skill("Load-Testing", ["load=testing", "load=test(s)"], "Competence"),
  Skill("Testing", ["testing"], "Competence"),
  Skill("Accessibility", ["accessibility", "accessible"], "Competence"),
  Skill("Performance", ["performance", "performant"], "Competence"),
  Skill("Reliability", ["reliability", "reliable"], "Competence"),
  # Skill("Resilience", ["resilience", "resilient"], "Competence"),
  # Skill("Scalability", ["scalability", "scalable", ], "Competence"),
  # Skill("Observability", ["observability", "observable"], "Competence"),
  # Skill("Usability", ["usability", "usable"], "Competence"),

  Skill("ETL", ["etl", "elt"], "Competence"),
  Skill("DWH", ["dwh"], "Competence"),

  # SECURITY
  Skill("Security", ["security"], "Competence"), # "secure"?
  Skill("App-Security", ["app=sec(urity)"], "Competence"),
  Skill("Cyber-Security", ["cyber=sec(urity)", "cyber=defence"], "Competence"),
  Skill("Data-Protection", ["data-protection"], "Competence"),
  Skill("Data-Security", ["data=sec(urity)"], "Competence"),
  Skill("Information-Security", ["information-sec(urity)", "info=sec(urity)"], "Competence"),
  Skill("Network-Security", ["network-security"], "Competence"),
  Skill("Penetration-Testing", ["penetration-testing", "penetration-test(s)", "penetration-tester"], "Competence"),
  Skill("Vulnerability-Testing", ["vulnerability-testing", "vulnerability-test(s)"], "Competence"),

  Skill("Network", ["network"], "Competence"), # TODO networking

  Skill("Robotics", ["robotics"], "Competence"),
  Skill("Computer-Vision", ["computer-vision"], "Competence"),

  Skill("Decentralized", ["decentralized"], "Competence"),
  Skill("Distributed", ["distributed"], "Competence"),
  Skill("HighLoad", ["high=load"], "Competence"),
  # Highly Available, High Availability, high performance, high traffic,
  # Clustering, Sharding, load balancing
  # Replication, Partitioning | Enterprise, large-scale
  # Big Data  Data-heavy, logic-heavy

  Skill("Computer-Science", ["comp=sci(ence)", "computer=sci(ence)", "comp(uter)=scientist", literal("CS")], "Competence", stack=["Computer", "Science"]),
  Skill("Data-Science", ["data=sci(ence)", "data=scientist", literal("DS")], "Competence", stack=["Data", "Science"]),

  Skill("AI", ["artificial-intelligence", "ai"], "Competence"),
  Skill("Big-Data", ["big=data"], "Competence"),
  Skill("Data", ["data"], "Competence", disambiguate=datascience()),
  Skill("Data-Extraction", ["data=extraction"], "Competence"),
  Skill("Data-Mining", ["data=mining"], "Competence"),
  Skill("Data-Visualization", ["data-visualization", "data=viz"], "Competence"), # FN for "Data Analysis and Visualization", needs a disambig. item
  # Scraping
  Skill("Machine-Learning", ["machine-learning", "ml"], "Competence"),
  Skill("Deep-Learning", ["deep=learning", "dl"], "Competence"), # not sure about FPs
  Skill("Neural-Networks", ["(deep=)neural-networks", "nn"], "Competence"), # not sure about FPs
  Skill("Natural-Language-Processing", ["natural-language-processing", "nlp"], "Competence"),
  Skill("Large-Language-Models", ["large-language-model(s)", "llm"], "Competence"),
  Skill("Large-Language-Models", ["large-language-model(s)", "llm"], "Competence"),
  Skill("Multimodal-Large-Language-Models", ["multimodal-large-language-model(s)", "mllm"], "Competence"),
  # Motion-Prediction
  # Sensor-Fusion

  Skill("Software", ["software"], "Competence"),
  Skill("SDLC", ["sdlc"], "Competence", stack=["Software", "Engineering"]),
  Skill("Hardware", ["hardware"], "Competence"),
  Skill("Malware", ["malware"], "Competence"),
  Skill("Firmware", ["firmware"], "Competence"),

  # STACK ROLES
  Skill("Programmer", ["programming", "coding", "programmer", "coder"], "Competence", stack=["Software", "Engineering"]),
  Skill("SDE", [literal("SDE")], "Competence", stack=["Software", "Engineering"]),
  Skill("SWE", [literal("SWE")], "Competence", stack=["Software", "Engineering"]),
  Skill("SRE", [literal("SRE")], "Competence", stack=["Reliability", "Engineering"]),
  Skill("DataOps", ["data=ops"], "Competence", stack=["ETL", "Automation", "Operations"]),
  Skill("DevOps", ["dev=ops"], "Competence", stack=["Infrastructure", "Automation", "Operations"]),
  Skill("DevSecOps", ["dev=sec=ops", "sec=dev=ops"], "Competence", stack=["Infrastructure", "Security", "Automation", "Operations"]),
  Skill("ITOps", ["itops"], "Competence", stack=["Infrastructure", "Operations"]),
  Skill("MlOps", ["ml=ops"], "Competence", stack=["Machine-Learning", "Automation", "Operations"]),
  Skill("SecOps", ["sec=ops"], "Competence", stack=["Security", "Automation", "Operations"]),

  # UNFINISHED
  Skill("Embedded", ["embedded"], "Competence"),
  Skill("System", ["system(s)"], "Competence"), # TODO many FPs, should be disambiguated like Data
  Skill("IoT", ["iot"], "Competence"),
  Skill("Open-Source", ["open=source", "oss"], "Competence"),

  # PRACTICES
  Skill("Administration", ["administration", "admin(istrator)"], "Competence"),
  Skill("Automation", ["automation", "automated"], "Competence"),
  Skill("Design", ["design"], "Competence"), # FPs in company names, not sure how to avoid
  Skill("Engineering", ["engineering", "engineer", "development", "developer"], "Competence"),
  Skill("Hacking", ["hacking", "hacker"], "Competence"),
  Skill("Leadership", ["leadership", "leader", "lead"], "Competence"),
  Skill("Management", ["management", "manager"], "Competence"),
  Skill("Operations", ["operations", "ops"], "Competence"),
  Skill("Recruitment", ["staffing", "recruitment", "recruiter"], "Competence"),
  Skill("Research", ["research", "researcher"], "Competence"),
  Skill("Visualization", ["visualization", "visualizer"], "Competence"),

  # INDUSTRIES -- I think that maybe INDUSTRIES and SCIENCES should be separated from SKILLS
  Skill("Advertisement", ["advertising", "advertisement"], "Competence"),
  # Academy (doc, post-doc, etc)
  Skill("Architecture", ["architecture", "architect"], "Competence"),
  Skill("Business", ["business", "entrepreneurship", "entrepreneur"], "Competence"),
  Skill("Computer", ["computer", "computing"], "Competence"),
  Skill("Ecology", ["ecology", "ecologist"], "Competence"),
  Skill("Education", ["edtech", "educator", "dean", "prof(essor)", "teacher"], "Competence"), # how to differentiate from "(my) Education:"
  Skill("Energy", ["energy"], "Competence"), # FPs
  # Environment, Environmental
  Skill("Finance", ["finance", "fintech", "financial"], "Competence"),
  Skill("Graphic", ["graphic", "graphical"], "Competence"),
  Skill("Health", ["health(care)"], "Competence"),
  Skill("Psychology", ["psychology"], "Competence"),
  Skill("Marketing", ["marketing"], "Competence"),
  Skill("Medicine", ["medicine", "medical"], "Competence"),
  Skill("Music", ["music(al)", "musician"], "Competence"),
  Skill("Sport", ["sport", "basketball"], "Competence"),
  Skill("Startup", ["startup"], "Competence"),
  # Travel

  # SCIENCES
  Skill("Analysis", ["analysis", "analytics", "analytical", "analyst"], "Competence"),
  Skill("Biochemistry", ["bio=chemistry"], "Competence"),
  Skill("Bioinformatics", ["bio=informatics", "bio=informatician"], "Competence"),
  Skill("Biology", ["biology", "biologist"], "Competence"),
  Skill("Economics", ["economics", "economist"], "Competence"),
  Skill("Electronics", ["electronic(s)"], "Competence"),
  Skill("Informatics", ["informatics"], "Competence"),
  Skill("Mathematics", ["mathematics", "mathematical", "math", "mathematician"], "Competence"),
  Skill("Physics", ["physics", "physical", "physicist"], "Competence"),
  Skill("Science", ["sci", "science", "scientific", "scientist", literal("B.S"), literal("M.S")], "Competence"),
  Skill("Statistics", ["statiscal", "statistics", "statistician"], "Competence"),
]

# Non-skills (words that look like skills but are not, might be useful to help with them in UI)
# SOTA: state of the art
# Self-Driving car
# neuroscience, neuroscientist +1
# transportation industry
# digital illustration
# cognitive science, cog-sci
# "5 yrs teaching FinTech and Market Operations. 30 yrs PMO Digital Transformations of Wall St. Investment Banks
# Talend
# Crucible
# Involved with VNFs, Cloud, etc
# I automate the web and moble-web; making bots and working in the cloud. Lately, I have been hired to make some anti-bots.
# Trade Settlements Analyst
# A tech-savvy story teller who loves to tell stories, not verbally, but through data.
# BI, business intelligence
# I am a LINUX/UNIX Administratory
# Biomedical Engineer
# Interest in Bioinformatics/Biostatistics
# has worked as a Director, Cinematographer, Sound Mixer, Videographer, Editor, and Producer for 10 years.
# analytical
# sales
# Site Reliability
# implementation of COTS software
# CPA turned developer
# Information Science != Informatics (1st is broader)
# "Python, STATA, SQL, R, SPSS, NVivo.", -- STATA? SPSS? NVivo?
# Information Technology
# data extraction/modeling, visualization (Tableau, Power BI)
