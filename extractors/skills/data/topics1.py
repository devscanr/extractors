from ...utils import literal, noun
from ..utils import Skill, neighbour

__all__ = ["SKILLS"]

SKILLS: list[Skill] = [
  Skill("Accessibility", ["accessibility", "accessible"], "Topic"),

  Skill("Administration", ["administration", "administrator", "admin"], "Topic"),

  Skill("AI", ["ai", "artificial-intelligence"], "Topic"),

  Skill("Algorithm", ["algorithm(s)", "algorithmic"], "Topic"),

  Skill("Analysis", ["analysis", "analytics", "analyst"], "Topic"),

  Skill("Animation", ["animation", "animated", "animating", "animator"], "Topic"),

  Skill("Architecture", ["architecture", "architect"], "Topic"),

  Skill("Automation", ["automation", "automated", "automatic", "automating"], "Topic"),

  Skill("Backend", ["back=end", "backender", noun("BE")], "Topic"), # not detected as PROPN, needs to be retrained

  Skill("BigData", ["big=data"], "Topic"),

  Skill("Blockchain", ["blockchain"], "Competence"),

  Skill("Business", ["business", "entrepreneur", "entrepreneurship"], "Topic"),
  Skill("Business-Analysis", ["businessanalysis", "businessanalytics", "businessanalyst"], "Topic", resolve=["Business", "Analysis"]),
  # TODO business intelligence, BI

  Skill("CI/CD", ["continuous=integration", "continuous=delivery", "ci/cd", "ci"], "Competence"),

  Skill("Computer", ["computer", "computing"], "Topic"),
  Skill("Computer-Science", [
    "computerscience", "computerscientist", "comp=sci", literal("CS")
  ], "Topic", resolve=["Computer", "Science"]),
  Skill("Computer-Vision", ["computer=vision"], "Topic"),

  Skill("Cloud", ["cloud"], "Topic"),
  Skill("Cloud-Architecture", ["cloudarchitecture", "cloudarchitect"], "Topic", resolve=["Cloud", "Architecture"]),

  Skill("Cross-Platform", ["cross=platform"], "Competence"),

  Skill("CMS", ["cms", "content=management=system"], "Topic"),

  Skill("CRM", ["crm", "customer=relationship=management"], "Topic"),

  Skill("Data", ["data"], "Topic"),
  Skill("-Data", [
    "personal=data", "user=data",
    "my=data", "your=data", "our=data", "their=data",
    "data=graph",
  ], "Topic", resolve=[]), # oversimplified, will update later
  Skill("Data-Analysis", ["dataanalysis", "dataanalytics", "dataanalyst"], "Topic", resolve=["Data", "Analysis"]),
  Skill("Data-Mining", ["data=mining", "data=extraction"], "Topic"),
  Skill("Data-Operations", ["dataoperations", "dataops"], "Topic", resolve=["Data", "Operations"]),

  Skill("Database", ["database(s)"], "Topic"),
  Skill("Database-Administration", [
    "databaseadministration", "databaseadministrator", "dba"
  ], "Topic", resolve=["Database", "Administration"]),
  Skill("Database-Design", ["databasedesign", "dbdesign", "databasedesigner", "dbdesigner"], "Topic", resolve=["Database", "Design"]),

  Skill("Datalake", ["data=lake(s)"], "Topic"),
  Skill("Data-Engineering", [
    "dataengineering", "dataengineer","datadeveloper", "datadev"
  ], "Topic", resolve=["Data", "Engineering"]),
  Skill("Data-Security", ["datasecurity", "data=sec", "data=protection"], "Topic", resolve=["Data", "Security"]),
  Skill("Data-Science", ["datascience", "datascientist", "data=sci", literal("DS")], "Topic", resolve=["Data", "Science"]),
  Skill("Data-Warehouse", ["data=warehouse", "dwh"], "Topic"),

  Skill("Decentralized", ["decentralized"], "Topic"),

  Skill("Deep-Learning", ["deep=learning", "dl"], "Topic"), # not sure about FPs

  Skill("Distributed", ["distributed"], "Topic"),

  Skill("Design", [
    "design", "designer",
    "graphicdesign", "graphicdesigner",
    "motiondesign", "motiondesigner",
    "visualdesign", "visualdesigner"
  ], "Topic"),

  Skill("E2E-Testing", ["end=to=end=testing", "e2e=testing", "e2e=test(s)"], "Topic"), # TODO capture split words

  Skill("Embedded", ["embedded"], "Topic"),
  Skill("Embedded-Engineering", [
    "embeddedengineering", "embeddedengineer",
    "embeddedprogramming", "embeddedprogrammer",
    "embeddeddeveloper", "embeddeddev",
  ], "Topic", resolve=["Embedded", "Engineering"]),

  Skill("Engineering", [
    "engineering", "engineered", "engineer", "eng",
    "coding", "coder",
    "development", "developed", "developer", "dev",
    "programming", "programmer",
  ], "Topic"),
  Skill("-Engineering", [
    "dev=mode", # =dev
  ], "Topic", resolve=[]),
  Skill("Engineering-Operations", ["devoperations", "devops"], "Topic", resolve=["Engineering", "Operations"]),
  Skill("Engineering-Security-Operations", [
    "dev/sec-ops", "sec/dev-ops",
    "dev-sec-ops", "sec-dev-ops",
    "devsecops", "secdevops",
  ], "Topic", resolve=["Engineering", "Security", "Operations"]),

  Skill("ETL", ["etl", "elt"], "Topic"),

  Skill("System-Engineering", [
    "systemengineering", "systemengineer",
    "systemprogramming", "systemprogrammer",
    "systemdeveloper", "systemdev",
  ], "Topic", resolve=["System", "Engineering"]),

  Skill("Firmware", ["firmware"], "Topic"),

  Skill("Frontend", ["front=end", "frontender", noun("FE")], "Topic"), # not detected as PROPN, needs to be retrained

  Skill("Fullstack", ["full=stack(er)"], "Topic", resolve=["Backend", "Frontend"]),

  Skill("Functional-Testing", ["functional=testing", "functional=test(s)"], "Topic"),

  Skill("Game", ["game"], "Topic"),
  Skill("-Game", ["game=theory"], "Topic", resolve=[]), # oversimplified, will update later
  Skill("Game-Design", ["gamedesign", "gamedesigner"], "Topic", resolve=["Game", "Design"]),
  Skill("Game-Engineering", [
    "gameengineering", "gameengineer",
    "gameprogramming", "gameprogrammer"
    "gamedeveloper", "gamedev"
  ], "Topic", resolve=["Game", "Engineering"]),

  Skill("Hardware", ["hardware"], "Topic"),
  Skill("Hardware-Design", ["hardwaredesign", "hardwaredesigner"], "Topic", resolve=["Hardware", "Design"]),
  Skill("Hardware-Engineering", [
    "hardwareengineering", "hardwareengineer",
    "hardwaredeveloper", "hardwaredev"
  ], "Topic", resolve=["Hardware", "Engineering"]),

  Skill("HighLoad", ["high=load"], "Topic"),

  Skill("Infrastructure", ["infrastructure"], "Topic"),

  Skill("Integration", ["integration"], "Topic"),
  Skill("Integration-Testing", ["integration=testing", "integration=test(s)"], "Topic"),

  Skill("IoT", ["iot", "internet-of-things"], "Topic"),

  Skill("Leadership", ["leadership", "leader", "lead"], "Topic"),

  Skill("Load-Testing", ["load=testing", "load=test(s)"], "Topic"),

  Skill("Low-Code", ["low=code", "no=code"], "Topic"),

  Skill("Machine-Learning", ["machine-learning", "ml"], "Topic"),
  Skill("ML-Engineering", [
    "mobileengineering", "mobileengineer",
    "mobileprogramming", "mobileprogrammer",
    "mobiledeveloper", "mobiledev",
  ], "Topic", resolve=["ML", "Engineering"]),
  Skill("ML-Operations", ["mloperations", "mlops", "ai=ops"], "Topic", resolve=["ML", "Operations"]),

  Skill("Management", ["management", "manager"], "Topic"),

  Skill("Mobile", ["mobile", "mobileapp"], "Topic"),
  Skill("Mobile-Design", ["mobiledesign", "mobiledesigner"], "Topic", resolve=["Mobile", "Design"]),
  Skill("Mobile-Engineering", [
    "mobileengineering", "mobileengineer",
    "mobileprogramming", "mobileprogrammer",
    "mobiledeveloper", "mobiledev",
  ], "Topic", resolve=["Mobile", "Engineering"]),

  Skill("Network", ["networking", "network"], "Topic"),
  Skill("Network-Security", ["networksecurity", "netsecurity", "net=sec"], "Topic", resolve=["Network", "Security"]),

  Skill("Natural-Language-Processing", ["natural=language=processing", "nlp"], "Topic"),

  Skill("Neural-Networks", ["(deep=)neural-networks", "nn", "dnn"], "Competence"), # not sure about FPs

  Skill("Operations", ["operations", "ops"], "Topic"),

  Skill("Orchestration", ["orchestration"], "Topic"),

  Skill("VA/PT", [
    "penetration=testing", "penetration=test(s)", "penetration=tester",
    "pen=testing", "pen=test", "pen=tester",
    "vapt",
    "vulnerability=assessment",
    "vulnerability=scanning", "vulnerability=scan(ner)",
    "vulnerability=testing", "vulnerability=test(s)", "vulnerability=tester",
  ], "Topic"),

  Skill("Performance", ["performance", "performant"], "Topic"),

  Skill("Product", ["product"], "Topic"),

  Skill("Project", ["project"], "Topic"),

  Skill("QA", ["quality-assurance", "qa"], "Topic"),
  Skill("AQA", ["aqa"], "Topic", resolve=["Automation", "QA"]),

  Skill("Recruitment", ["recruitment", "recruiter", "staffing"], "Topic"),

  Skill("Reliability", ["reliability", "reliable"], "Topic"),

  Skill("Research", ["research", "reseacher"], "Topic"),

  Skill("Robotics", ["robotics", "robocon"], "Topic"),

  Skill("Scalability", ["scalability", "scalable"], "Topic"),

  Skill("Science", ["science(s)", "scientist", "scientific", literal("B.S"), literal("M.S")], "Topic"),

  Skill("Scraping", ["scraping", "webscraping"], "Topic"),

  Skill("Security", ["security", "secure" ], "Topic"),
  Skill("Security", ["sec"], disambiguate=neighbour(2)),
  Skill("Security-Operations", ["securityoperations", "secoperations", "secops"], "Topic", resolve=["Security", "Operations"]),
  Skill("Security-Cyber", ["cyber=security", "cyber=sec", "cyber=defence"], "Topic", resolve=["Security"]),
  Skill("Security-Information", ["information=security", "info=security", "info=sec"], "Topic", resolve=["Security"]),

  Skill("Software", ["software"], "Topic"),
  Skill("Software-Design", ["softwaredesign", "softwaredesigner"], "Topic", resolve=["Software", "Design"]),
  Skill("Software-Engineering", [
    "softwareengineering", "softwareengineer",
    "softwareprogramming", "softwareprogrammer",
    "softwaredeveloper", "softwaredev",
    literal("SDE"), literal("SWE"), # sometimes SE @_@
  ], "Topic", resolve=["Software", "Engineering"]),

  Skill("Solution", ["solution(s)"], "Topic"),
  Skill("Solution-Architecture", ["solutionarchitecture", "solutionarchitect"], "Topic", resolve=["Solution", "Architecture"]),

  Skill("SDLC", ["sdlc"], "Topic", resolve=["Software", "Engineering"]),

  Skill("SRE", [literal("SRE")], "Topic", resolve=["Reliability", "Engineering"]),

  Skill("Statistics", ["statistic(s)", "statistician", "statistical"], "Competence"),

  Skill("System", ["system(s)"], "Topic"), # TODO fix FPs
  Skill("System-Administration", [
    "systemadministration", "systemadministrator", "sysadmin"
  ], "Topic", resolve=["System", "Administration"]),
  Skill("System-Architecture", ["systemarchitecture", "systemarchitect"], "Topic", resolve=["System", "Architecture"]),

  Skill("Testing", ["testing", "tested", "tester"], "Topic"),
  Skill("-Testing", ["battle-tested", "tested to"], "Topic", resolve=[]),

  Skill("UI/UX", ["ui=ux", "ui/ux", "uix", "ui", "ux", "user=interface", "human=interface", "user=experience"], "Topic"),
  Skill("UI-Design", ["uidesign", "uidesigner"], "Topic", resolve=["UI/UX", "Design"]),

  Skill("Unit-Testing", ["unit=testing", "unit=test(s)"], "Topic"),

  Skill("Visualization", ["visualization", "visualizer"], "Topic"),

  Skill("Web", ["web", "website", "webapp"], "Topic"),
  Skill("Web3", ["web3"], "Competence"),
  Skill("Web-Design", ["webdesign", "webdesigner"], "Topic", resolve=["Web", "Design"]),
  Skill("Web-Engineering", [
    "webengineering", "webengineer",
    "webprogramming", "webprogrammer",
    "webdeveloper", "webdev",
    "webcoding", "webcoder",
  ], "Topic", resolve=["Web", "Engineering"]),
  Skill("Web-Security", ["websecurity", "web=sec"], "Topic", resolve=["Web", "Security"]),
]

# malware-analysis = security-research

# def dis_automation() -> Resolve:
#   def disambiguate(ent: Span) -> list[str]:
#     skills: list[str] = []
#     for e in ent.sent.ents:
#       if e == ent: continue
#       if e.label_ in "QA":
#         skills.append("Automated-Testing")
#     return skills if len(skills) else ["Automation"]
#   return disambiguate
#
# def dis_root(root: str, prefixes: set[str]) -> Resolve:
#   def disambiguate(ent: Span) -> list[str]:
#     skills: list[str] = []
#     for e in ent.sent.ents:
#       if e == ent: continue
#       if e.label_ in prefixes:
#         skills.append(e.label_ + "-" + root)
#     return skills if len(skills) else [root]
#   return disambiguate

# Skill("Resilience", ["resilience", "resilient"], "Topic"),
# Skill("Observability", ["observability", "observable"], "Topic"),
# Skill("Usability", ["usability", "usable"], "Topic"),
# Highly Available, High Availability, high performance, high traffic,
# Clustering, Sharding, load balancing
# Replication, Partitioning | Enterprise, large-scale
# Skill("Resiliency", ["resiliency", "resilient"], "Topic"),
# Skill("Deploy", ["deploy"], "Topic"),
# Skill("Integration", ["integration"], "Topic"),
#
# Skill("E-Commerce", ["e=commerce"], "Topic"),
# Skill("Cluster", ["cluster"], "Topic"),
# Skill("Container", ["container"], "Topic"),
