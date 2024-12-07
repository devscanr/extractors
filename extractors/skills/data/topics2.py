from spacy.tokens import Span
from ...utils import literal, noun, propn
from ..utils import Disambiguate, Skill, clean, neighbour

__all__ = ["SKILLS"]

def dis_processor() -> Disambiguate:
  def disambiguate(ent: Span) -> bool:
    for e in ent.sent.ents:
      if e == ent: continue
      label = clean(e.label_)
      if label in {"AMD", "Intel", "ARM", "ARC", "x86", "x32", "x64"}:
        # Note: we can try to avoid repetitive declarations at `disambiguate`s by tagging skills, e.g.
        # AMD gets #CPU, Intel gets #CPU and here we can just refer to any skill with "CPU" tag...
        return True
    return False
  return disambiguate

SKILLS: list[Skill] = [
  # SOFTWARE ENGINEERING
  Skill("Agile", ["agile", "kanban", "scrum"], "Topic"),
  Skill("TDD", ["tdd"], "Topic"),
  Skill("BDD", ["ddd"], "Topic"),
  Skill("DDD", ["ddd"], "Topic"),
  Skill("FP", ["functional=programming", "fp", "фп"], "Topic"),
  Skill("OOP", [
    "object=oriented( programming)", "oop", literal("SOLID"), literal("S.O.L.I.D"), "ооп"
  ], "Topic"),
  # YAGNI, DRY, KISS, MVC
  # (software) design patterns

  Skill("API", ["api"], "Topic"),
  Skill("ORM", ["orm"], "Topic"),
  Skill("REST", ["rest=api", propn("rest"), noun("REST")], "Topic"),
  Skill("REST", ["rest"], disambiguate=neighbour(2)),
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
  Skill("-SPA", ["med spa", "medical spa"], "Topic", resolve=[]),
  Skill("OpenAPI", ["openapi"], "Topic"),
  Skill("IP", ["ip"], "Topic"),
  Skill("TCP", ["tcp"], "Topic"),
  Skill("HTTP", ["http"], "Topic"),
  Skill("HTTPS", ["https"], "Topic"),
  Skill("WebGL", ["webgl"], "Topic"),
  Skill("WebSocket", ["websocket", "ws"], "Topic"),
  Skill("Web-Components", ["web=component(s)"], "Topic"),

  # BLOCKCHAIN
  Skill("dApps", ["decentralized-application(s)", "dapp(s)"], "Topic"),
  Skill("DeFi", ["decentralized-finance", "de=fi"], "Topic"),
  Skill("Crypto", ["crypto"], "Topic"),
  Skill("P2P", ["peer=2=peer", "peer=to=peer", "p2p"], "Topic"),

  # LOW-CODE
  Skill("IaaS", ["iaas"], "Topic"),
  Skill("BaaS", ["baas", "mbaas"], "Topic"),
  Skill("PaaS", ["paas"], "Topic"),
  Skill("SaaS", ["saas"], "Topic"),

  # EMBEDDED
  Skill("PCB", ["pcb"], "Topic"),

  # OPERATIONS
  Skill("CI/CD", ["continuous=integration", "continuous=delivery", "continuous=deployment", "ci/cd", "ci"], "Topic"),
  Skill("Gitops", ["gitops"], "Topic"),
  Skill("Monorepo", ["monorepo(s)", "monorepository", "monorepositories"], "Topic"),
  Skill("Containerization", ["containerization", "containerized"], "Topic"),
  Skill("Virtual-Machine", ["virtual=machine(s)", "vm(s)"], "Topic"),

  # ???
  Skill("Integration", ["integration"], "Topic"),
  Skill("Integration-Testing", ["integration=testing", "integration=test(s)"], "Topic"),

  # SECURITY
  Skill("Access-Control", ["rbac", "abac", "acl"], "Topic"),
  Skill("VA/PT", [
    "penetration=testing", "penetration=test(s)", "penetration=tester",
    "pen=testing", "pen=test", "pen=tester",
    "vapt",
    "vulnerability=assessment",
    "vulnerability=scanning", "vulnerability=scan(ner)",
    "vulnerability=testing", "vulnerability=test(s)", "vulnerability=tester",
  ], "Topic"),

  # QA
  Skill("E2E-Testing", ["end=to=end=testing", "e2e=testing", "e2e=test(s)"], "Topic"), # TODO capture split words
  Skill("Functional-Testing", ["functional=testing", "functional=test(s)"], "Topic"),
  Skill("Regression-Testing", ["regression=testing", "regression=test(s)"], "Topic"),
  Skill("Unit-Testing", ["unit=testing", "unit=test(s)"], "Topic"),

  # AUTOMATION
  Skill("Load-Testing", ["load=testing", "load=test(s)"], "Topic"),

  # ...
  Skill("Large-Language-Models", ["large-language-model(s)", "llm(s)"], "Topic"),
  Skill("Multimodal-Large-Language-Models", ["multimodal-large-language-model(s)", "mllm(s)"], "Topic"),
  # Motion-Prediction
  # Sensor-Fusion

  # UNFINISHED
  Skill("Open-Source", ["open=source", "oss"], "Topic"),

  # INDUSTRIES -- I think that maybe INDUSTRIES and SCIENCES should be separated from SKILLS
  # Skill("Advertisement", ["advertising", "advertisement"], "Topic"),
  # Academy (doc, post-doc, etc)
  # Skill("Ecology", ["ecology", "ecologist"], "Topic"),
  # Skill("Energy", ["energy"], "Topic"), # FPs
  # Environment, Environmental
  # Skill("Health", ["health(care)"], "Topic"),
  # Skill("Psychology", ["psychology"], "Topic"),
  # Skill("Medicine", ["medicine", "medical"], "Topic"),
  # Skill("Music", ["music(al)", "musician"], "Topic"),
  # Skill("Sport", ["sport", "basketball"], "Topic"),
  # Travel

  # ANALYSIS
  Skill("AB-Testing", ["a/b test(ing)"], "Topic"),
  Skill("Hypothesis", ["hypothesis", "hypotheses"], "Topic"),

  # SCIENCES
  # Skill("Biochemistry", ["bio=chemistry"], "Topic"),
  # Skill("Bioinformatics", ["bio=informatics", "bio=informatician"], "Topic"),
  # Skill("Biology", ["biology", "biologist"], "Topic"),
  # Skill("Electronics", ["electronic(s)"], "Topic"),
  # Skill("Informatics", ["informatics"], "Topic"),
  Skill("Mathematics", ["mathematics", "mathematical", "math", "mathematician"], "Topic"),
  Skill("Physics", ["physics", "physical", "physicist"], "Topic"),

  # UNSORTED
  Skill("CPU", ["cpu", "central-processing-unit"], ""),
  Skill("CPU", ["processor(s)"], disambiguate=dis_processor()),
  Skill("GPU", ["gpu"], ""),
  Skill("CLI", ["cli"], ""),
  Skill("GUI", ["gui"], ""),

  Skill("Voxel", ["voxel"], ""),
  Skill("Pixel", ["pixel"], ""),
  Skill("Sprite", ["sprite"], ""),
  Skill("Texture", ["texture"], ""),
  # Skill("2D", ["2d"], ""), -- too widespread
  # Skill("3D", ["3d"], ""), -- too widespread
  # Skill("Ray-Tracing", ["ray=tracing"], ""),
  # Skill("Compiler", ["compiler"], ""),
  # Skill("Singleplayer", ["single=player"], ""),
  # Skill("Multiplayer", ["multi=player"], ""),
  # Skill("Entity-Component-System", ["entity-component-system", "ecs"], ""), -- conflicts with AWS-ECS
  Skill("Cron", ["cron", "crond", "cronjob"], ""),
  Skill("SSL", ["ssl"], ""),
  Skill("SSH", ["ssh"], ""),
  Skill("FTP", ["ftp"], ""),
  Skill("SFTP", ["sftp"], ""),
  Skill("RTOS", ["rtos"], ""),
  Skill("GPOS", ["gpos"], ""),
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
# 'Rohit Kabra (Masters in information System)
# data extraction/modeling, visualization (Tableau, Power BI)
# edge (ambiguous)
# Astrophysics
# HRD term
# Real-Time x 2
# Serverless x 2
# Logging
# Monitoring
# OCR models
# Familiarity with ConvNeXt and similar models
