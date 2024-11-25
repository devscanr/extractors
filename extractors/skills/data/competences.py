from spacy.tokens import Span
from ...utils import get_cons_words, literal, noun, propn
from ..utils import Disambiguate, Skill, neighbour

__all__ = ["SKILLS"]

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
  Skill("IaaS", ["iaas"], "Competence"),
  Skill("BaaS", ["baas", "mbaas"], "Competence"),
  Skill("PaaS", ["paas"], "Competence"),
  Skill("SaaS", ["saas"], "Competence"),

  # MOBILE
  Skill("Cross-Platform", ["cross=platform"], "Competence"),

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
  # Skill("Accessibility", ["accessibility", "accessible"], "Competence"),
  # Skill("Performance", ["performance", "performant"], "Competence"),
  # Skill("Reliability", ["reliability", "reliable"], "Competence"),
  # Skill("Resilience", ["resilience", "resilient"], "Competence"),
  # Skill("Scalability", ["scalability", "scalable", ], "Competence"),
  # Skill("Observability", ["observability", "observable"], "Competence"),
  # Skill("Usability", ["usability", "usable"], "Competence"),

  Skill("ETL", ["etl", "elt"], "Competence"),
  Skill("Datalake", ["data=lake(s)"], "Competence"),
  Skill("DWH", ["dwh"], "Competence"),

  Skill("Computer-Vision", ["computer=vision"], "Competence"),

  # Scraping
  Skill("Deep-Learning", ["deep=learning", "dl"], "Competence"), # not sure about FPs
  Skill("Neural-Networks", ["(deep=)neural-networks", "nn"], "Competence"), # not sure about FPs
  Skill("Natural-Language-Processing", ["natural-language-processing", "nlp"], "Competence"),
  Skill("Large-Language-Models", ["large-language-model(s)", "llm"], "Competence"),
  Skill("Large-Language-Models", ["large-language-model(s)", "llm"], "Competence"),
  Skill("Multimodal-Large-Language-Models", ["multimodal-large-language-model(s)", "mllm"], "Competence"),
  # Motion-Prediction
  # Sensor-Fusion

  # UNFINISHED
  Skill("Open-Source", ["open=source", "oss"], "Competence"),

  # INDUSTRIES -- I think that maybe INDUSTRIES and SCIENCES should be separated from SKILLS
  # Skill("Advertisement", ["advertising", "advertisement"], "Competence"),
  # Academy (doc, post-doc, etc)
  # Skill("Architecture", ["architecture", "architect"], "Competence"),
  # Skill("Computer", ["computer", "computing"], "Competence"),
  # Skill("Ecology", ["ecology", "ecologist"], "Competence"),
  # Skill("Education", ["edtech", "educator", "dean", "prof(essor)", "teacher"], "Competence"), # how to differentiate from "(my) Education:"
  # Skill("Energy", ["energy"], "Competence"), # FPs
  # Environment, Environmental
  # Skill("Finance", ["finance", "fintech", "financial"], "Competence"),
  # Skill("Graphic", ["graphic", "graphical"], "Competence"),
  # Skill("Health", ["health(care)"], "Competence"),
  # Skill("Psychology", ["psychology"], "Competence"),
  # Skill("Marketing", ["marketing"], "Competence"),
  # Skill("Medicine", ["medicine", "medical"], "Competence"),
  # Skill("Music", ["music(al)", "musician"], "Competence"),
  # Skill("Sport", ["sport", "basketball"], "Competence"),
  # Skill("Startup", ["startup"], "Competence"),
  # Travel

  # SCIENCES
  # Skill("Analysis", ["analysis", "analytics", "analytical", "analyst"], "Competence"),
  # Skill("Biochemistry", ["bio=chemistry"], "Competence"),
  # Skill("Bioinformatics", ["bio=informatics", "bio=informatician"], "Competence"),
  # Skill("Biology", ["biology", "biologist"], "Competence"),
  # Skill("Economics", ["economics", "economist"], "Competence"),
  # Skill("Electronics", ["electronic(s)"], "Competence"),
  # Skill("Informatics", ["informatics"], "Competence"),
  # Skill("Mathematics", ["mathematics", "mathematical", "math", "mathematician"], "Competence"),
  # Skill("Physics", ["physics", "physical", "physicist"], "Competence"),
  # Skill("Science", ["sci", "science", "scientific", "scientist", literal("B.S"), literal("M.S")], "Competence"),
  # Skill("Statistics", ["statiscal", "statistics", "statistician"], "Competence"),
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
# edge (ambiguous)
# PCB design and Firmware development
# Astrophysics
# HRD term
