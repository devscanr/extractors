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
  Skill("MVC", [
    "mvc", "model-view-controller",
  ], "Topic"),
  # YAGNI, DRY, KISS
  # (software) design patterns

  Skill("Algorithms", ["algorithm(s)"], "Topic"),
  Skill("Data-Structures", ["data=structure(s)", "data=type(s)", "data=class(es)"], "Topic"),
  Skill("Devices", ["device(s)"], "Topic"),
  Skill("Markup", ["markup"], "Topic"),

  Skill("API", ["api"], "Topic"),
  Skill("ORM", ["orm"], "Topic"),
  Skill("REST", ["rest=api", "restful", propn("rest"), noun("REST")], "Topic"),
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
  Skill("Smart-Contracts", ["smart=contract(s)"], "Topic"),

  # LOW-CODE
  Skill("IaaS", ["iaas"], "Topic"),
  Skill("BaaS", ["baas", "mbaas"], "Topic"),
  Skill("PaaS", ["paas"], "Topic"),
  Skill("SaaS", ["saas"], "Topic"),

  Skill("CMS", ["cms", "content=management=system"], "Topic"),
  Skill("CRM", ["crm", "customer=relationship=management"], "Topic"),

  # ?
  # Skill("ERP", ["erp"], "Topic"),

  # EMBEDDED
  Skill("PCB", ["pcb"], "Topic"),

  # DATA
  Skill("Data-Mining", ["data=mining", "data=extraction"], "Topic", resolve=["Data", "Mining"]),
  Skill("Data-Warehouse", ["data=warehouse", "dwh"], "Topic", resolve=["Data", "Warehouse"]),
  Skill("ETL", ["etl(s)", "elt"], "Topic"),
  Skill("Warehouse", ["warehouse"], "Topic"),

  # DATABASES
  Skill("Datalake", ["data=lake(s)"], "Topic"),

  # OPERATIONS
  Skill("CI/CD", [
    "continuous=integration", "continuous=delivery", "continuous=deployment",
    "ci/cd", "ci",
  ], "Topic"),
  Skill("Deployment", ["deployment", "deploy"], "Topic"),
  Skill("Gitops", ["gitops"], "Topic"),
  Skill("Monorepo", ["monorepo(s)", "monorepository", "monorepositories"], "Topic"),
  Skill("Containerization", ["containerization", "containerized"], "Topic"), # TODO container with disambig.
  Skill("Orchestration", ["orchestration"], "Topic"),
  Skill("Provisioning", ["provisioning"], "Topic"),
  Skill("Virtualization", ["virtualization", "virtual=machine(s)", "vm(s)"], "Topic"),
  # certificates: AWS Certified Solutions Architect Professional, AWS Certified DevOps Engineer Professional
  Skill("Integration", ["integration"], "Topic"),

  # NETWORKS
  Skill("Firewall", ["firewall(s)"], "Topic"), # also SECURITY
  Skill("VLAN", ["vlan"], "Virtual LAN: a way to logically separate a group of computers into a network"),
  Skill("VPN", ["vpn(s)"], "Topic"), # also SECURITY
  Skill("Wireless", ["wireless"], "Topic"),

  # SECURITY
  Skill("Access-Control", ["rbac", "abac", "acl"], "Topic"),
  # Identity and Access management
  Skill("VA/PT", [
    "penetration=testing", "penetration=test(s)", "penetration=tester",
    "pen=testing", "pen=test", "pen=tester",
    "vapt",
    "vulnerability=assessment",
    "vulnerability=scanning", "vulnerability=scan(ner)",
    "vulnerability=testing", "vulnerability=test(s)", "vulnerability=tester",
  ], "Topic"),
  # Familiarity with industry standards like MITRE ATT&CK and D3FEND,
  # the NIST Cybersecurity Framework, STIX/TAXII, and OpenIOC
  Skill("ISO-27001", ["iso-27001"], "Security Compliance"),
  Skill("GDPR", ["gdpr"], "Security Compliance"),
  Skill("NIST", ["nist"], "Security Compliance"),

  # GAMES
  Skill("Pixel", ["pixel(s)"], ""),
  Skill("-Pixel", ["google=pixel"]),
  # Polygon -- disambig.
  Skill("Shaders", ["shader(s)"], ""),
  Skill("Sprite", ["sprite(s)"], ""),
  Skill("Texture", ["texture(s)"], ""),
  Skill("Voxel", ["voxel(s)"], ""),

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
  # Travel

  # ANALYSIS
  Skill("AB-Testing", ["a/b-test(s)", "a/b-testing", "ab-test(s)", "ab-testing"], "Topic"),
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

  Skill("HighLoad", ["high=load"], "Topic"),
  Skill("IAC", ["iac", "infrastructure=as=code"], resolve=["Infrastructure", "Engineering"]),

  # VCS
  Skill("VCS", ["branching", "versioning", "version control", "vcs"], ""),

  # ??
  # blue green deployments


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
# • Extensive hands-on experience with BGP, OSPF, and EIGRP routing protocols in large-scale, enterprise environments.
# • In-depth knowledge of Layer 2 and Layer 3 network technologies, including VLANs, spanning-tree, and routing.
# • Proven expertise in SD-WAN architecture and deployment.
# • Proficiency with networking products and solutions from Cisco, Meraki, Fortinet, Palo Alto, and other leading vendors.
# • In-depth knowledge of VoIP protocols (e.g., SIP, RTP, H.323) and their application in diverse environments.
# • Strong experience in unified communications platforms (e.g., Cisco, Avaya, Asterisk, Microsoft Teams).
# • Advanced understanding of VoIP hardware and software, including PBX systems, softphones, and gateways.
# ISTQB Performance testing experience
# • Knowledge of DoD STIGs, STIG vulnerabilities, and remediation strategies
# President at Intellect Neurosciences, Inc. | Business Officer and Co-Founder at Various Life Science Companies | Former Chief Executive Officer at Immune Pharma
# Data Scientist actively looking for a position within the pharma/healthcare industry.
# I am currently a Ph.D. candidate in a Geosciences program, seismology in particular.
# I have a mixed background in Biology and Computer Science. I also work in an animal hospital and love being around my dogs and cats.
# I am a newbie Data Analyst who likes to explore data concerning cognitive neuroscience, psychology, gaming, anime and book publishing.
# News, publishing, and media industry experience.
# I am an oceanographer and climate scientist who investigates the interactions between the ocean, the atmosphere, and the rest of the Earth System.
# Astronomy PhD student and data scientist.
# Ph.D. Candidate in Systems Engineering with focus in Optimization of Distributed Spacecraft Missions.
# Electrical Engineer interested in the intersection of software and hardware to build better healthcare technologies including diagnostics, robotics, and devices
# Sensor Fusion and Navigation Engineer at Kearfott, previous experiences at @American-Robotics, @fdcl-gwu
# Design verification engineer working with ORAN/LTE/5g radio hardware
# HPC (high performance computing)
# Electrician by trade, Electrical & Computer Engineering Student, Programmer, Maker, Photographer by Hobby.
# Seasoned IT Storage Architect specializing in SAN and NAS infrastructure design , migration and deployment strategies
# Pro tinkerer- Odroid, Pi, Pine- ARM Boards. Virtualization, LXC
# I'm an ASU graduate with a degree in Graphic Information Technology.
# WordPress, PHP, Stellar Lumens, XDC, XRPL, Python and Solidity. Rodi Software.
# Software Developer, I like to use GNU Emacs and NixOS.

# LATEST ADDON:
# + 3 DevOps
# + 4 Mobile
# + 1 (Product) Analyst
# + 4 QA
# + 6 ML
# + 5 Security
# + 1 Low-Code
# + 3 Blockchain & Web3
# + 3 Games
# + 3 Networks
# + 1 Frontend
# + 1 Backend
# + 1 Fullstack

# HIREABLE
# "#OpenToWork"
