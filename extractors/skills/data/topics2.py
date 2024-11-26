from ...utils import literal, noun, propn
from ..utils import Skill, neighbour

__all__ = ["SKILLS"]

SKILLS: list[Skill] = [
  # SOFTWARE ENGINEERING
  Skill("Agile", ["agile", "kanban", "scrum"], "Topic"),
  Skill("TDD", ["tdd"], "Topic"),
  Skill("BDD", ["ddd"], "Topic"),
  Skill("DDD", ["ddd"], "Topic"),
  Skill("FP", ["functional=programming", "fp", "фп"], "Topic"),
  Skill("OOP", ["object=oriented( programming)", "oop", literal("SOLID"), "ооп"], "Topic"),
  # YAGNI, DRY, KISS, MVC

  Skill("API", ["api"], "Topic"),
  Skill("ORM", ["orm"], "Topic"),
  Skill("REST", ["rest=api", propn("rest"), noun("REST")], "Topic"),
  Skill("REST", ["rest"], "Topic", disambiguate=neighbour(2)),
  Skill("RPC", ["rpc=api", "rpc"], "Topic"),
  Skill("SOAP", ["soap"], "Topic"),
  Skill("SSG", ["ssg"], "Topic"),
  Skill("SSR", ["ssr"], "Topic"),

  # FRONTEND
  # BEM, БЭМ
  Skill("DOM", ["dom"], "Topic"),
  Skill("Browser", ["browser"], "Topic"),
  Skill("DevTools", ["dev=tools"], "Topic"),
  Skill("MPA", ["mpa"], "Topic"),
  Skill("SPA", ["spa"], "Topic"),
  Skill("OpenAPI", ["openapi"], "Topic"),
  Skill("IP", ["ip"], "Topic"),
  Skill("TCP", ["tcp"], "Topic"),
  Skill("HTTP", ["http"], "Topic"),
  Skill("HTTPS", ["https"], "Topic"),
  Skill("WebGL", ["webgl"], "Topic"),
  Skill("WebSocket", ["websocket", "ws"], "Topic"),

  Skill("dApps", ["decentralized-application(s)", "dapp(s)"], "Topic"),
  Skill("DeFi", ["decentralized-finance", "de=fi"], "Topic"),

  Skill("Crypto", ["crypto"], "Topic"),
  Skill("P2P", ["peer=2=peer", "peer=to=peer", "p2p"], "Topic"),

  # LOW-CODE
  Skill("IaaS", ["iaas"], "Topic"),
  Skill("BaaS", ["baas", "mbaas"], "Topic"),
  Skill("PaaS", ["paas"], "Topic"),
  Skill("SaaS", ["saas"], "Topic"),

  # PL/QL UMBRELLAS
  Skill("Assembly", ["assembly"], "Topic"),
  Skill("GraphQL", ["graphql"], "Topic"),
  Skill("SQL", ["sql"], "Topic"),
  Skill("NoSQL", ["nosql"], "Topic"),

  # SECURITY
  Skill("Malware", ["malware"], "Topic"),

  Skill("Large-Language-Models", ["large-language-model(s)", "llm"], "Topic"),
  Skill("Large-Language-Models", ["large-language-model(s)", "llm"], "Topic"),
  Skill("Multimodal-Large-Language-Models", ["multimodal-large-language-model(s)", "mllm"], "Topic"),
  # Motion-Prediction
  # Sensor-Fusion

  # UNFINISHED
  Skill("Open-Source", ["open=source", "oss"], "Topic"),

  # INDUSTRIES -- I think that maybe INDUSTRIES and SCIENCES should be separated from SKILLS
  # Skill("Advertisement", ["advertising", "advertisement"], "Topic"),
  # Academy (doc, post-doc, etc)
  # Skill("Ecology", ["ecology", "ecologist"], "Topic"),
  # Skill("Education", ["edtech", "educator", "dean", "prof(essor)", "teacher"], "Topic"), # how to differentiate from "(my) Education:"
  # Skill("Energy", ["energy"], "Topic"), # FPs
  # Environment, Environmental
  # Skill("Finance", ["finance", "fintech", "financial"], "Topic"),
  # Skill("Graphic", ["graphic", "graphical"], "Topic"),
  # Skill("Health", ["health(care)"], "Topic"),
  # Skill("Psychology", ["psychology"], "Topic"),
  # Skill("Marketing", ["marketing"], "Topic"),
  # Skill("Medicine", ["medicine", "medical"], "Topic"),
  # Skill("Music", ["music(al)", "musician"], "Topic"),
  # Skill("Sport", ["sport", "basketball"], "Topic"),
  # Skill("Startup", ["startup"], "Topic"),
  # Travel

  # SCIENCES
  # Skill("Analysis", ["analysis", "analytics", "analytical", "analyst"], "Topic"),
  # Skill("Biochemistry", ["bio=chemistry"], "Topic"),
  # Skill("Bioinformatics", ["bio=informatics", "bio=informatician"], "Topic"),
  # Skill("Biology", ["biology", "biologist"], "Topic"),
  # Skill("Economics", ["economics", "economist"], "Topic"),
  # Skill("Electronics", ["electronic(s)"], "Topic"),
  # Skill("Informatics", ["informatics"], "Topic"),
  # Skill("Mathematics", ["mathematics", "mathematical", "math", "mathematician"], "Topic"),
  # Skill("Physics", ["physics", "physical", "physicist"], "Topic"),
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
