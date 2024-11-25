from spacy.tokens import Span
from ...utils import literal
from ..utils import Resolve, Skill, neighbour

__all__ = ["SKILLS"]

# malware-analysis = security-research

def dis_automation() -> Resolve:
  def disambiguate(ent: Span) -> list[str]:
    skills: list[str] = []
    for e in ent.sent.ents:
      if e == ent: continue
      if e.label_ in "QA":
        skills.append("Automated-Testing")
    return skills if len(skills) else ["Automation"]
  return disambiguate

def dis_root(root: str, prefixes: set[str]) -> Resolve:
  def disambiguate(ent: Span) -> list[str]:
    skills: list[str] = []
    for e in ent.sent.ents:
      if e == ent: continue
      if e.label_ in prefixes:
        skills.append(e.label_ + "-" + root)
    return skills if len(skills) else [root]
  return disambiguate

SKILLS: list[Skill] = [
  Skill("Administration", [
    "administration", "administrator", "admin"
  ], "Competence", resolve=dis_root("Administration", {"Database", "System"})),
  Skill("Database-Administration", ["databaseadministration", "databaseadministrator", "dba"], "Competence"),
  Skill("System-Administration", ["systemadministration", "systemadministrator", "sysadmin"], "Competence"),

  Skill("Analysis", [
    # TODO business intelligence, BI
    "analysis", "analytics", "analyst"
  ], "Competence", resolve=dis_root("Analysis", {"Business", "Data"})),
  Skill("Business-Analyst", ["businessanalysis", "businessanalytics", "businessanalyst"], "Competence"),
  Skill("Data-Analyst", ["dataanalysis", "dataanalytics", "dataanalyst"], "Competence"),

  Skill("Design", [
    "design", # FPs in company names, not sure how to avoid
    "designer"
  ], "Competence", resolve=dis_root("Design", {"Database", "Game", "Hardware", "Mobile", "Software", "UI", "Web"})),
  Skill("Database-Design", ["databasedesign", "dbdesign", "databasedesigner", "dbdesigner"], "Competence"),
  Skill("Game-Design", ["gamedesign", "gamedesigner"], "Competence"),
  Skill("Graphic-Design", ["graphic=design", "graphic=designer"], "Competence"),
  Skill("Visual-Design", ["visual=design", "visual=designer"], "Competence"),
  Skill("Hardware-Design", [
    "hardwaredesign", "hardwaredesigner",
  ], "Competence"),
  Skill("Mobile-Design", [
    "mobiledesign", "mobiledesigner",
  ], "Competence", alias="UI-Design"),
  Skill("Software-Design", [
    "softwaredesign", "softwaredesigner",
  ], "Competence"),
  Skill("UI-Design", ["uidesign", "uidesigner"], "Competence"),
  Skill("Web-Design", ["webdesign", "webdesigner"], "Competence"),

  Skill("Engineering", [
    "engineering", "engineered", "engineer", "eng",
    "coding", "coder",
    "development", "developed", "developer", "dev",
    "programming", "programmer",
  ], "Competence", resolve=dis_root("Engineering", {"Data", "Embedded", "Game", "Hardware", "ML", "Mobile", "Software", "System", "Web"})),
  Skill("Engineering:skip", [
    "dev=mode", # =dev
  ], "Competence", resolve=lambda _: []),
  Skill("Data-Engineering", [
    "dataengineering", "dataengineer",
    "datadeveloper", "datadev"
  ], "Competence"),
  Skill("Embedded-Engineering", [
    "embeddedengineering", "embeddedengineer",
    "embeddedprogramming", "embeddedprogrammer",
    "embeddeddeveloper", "embeddeddev",
  ], "Competence"),
  Skill("Game-Engineering", [
    "gameengineering", "gameengineer",
    "gameprogramming", "gameprogrammer"
    "gamedeveloper", "gamedev"
  ], "Competence"),
  Skill("Hardware-Engineering", [
    "hardwareengineering", "hardwareengineer",
    "hardwaredeveloper", "hardwaredev"
  ], "Competence"),
  Skill("ML-Engineering", [
    "mobileengineering", "mobileengineer",
    "mobileprogramming", "mobileprogrammer",
    "mobiledeveloper", "mobiledev",
  ], "Competence"),
  Skill("Mobile-Engineering", [
    "mobileengineering", "mobileengineer",
    "mobileprogramming", "mobileprogrammer",
    "mobiledeveloper", "mobiledev",
  ], "Competence"),
  Skill("Software-Engineering", [
    "softwareengineering", "softwareengineer",
    "softwareprogramming", "softwareprogrammer",
    "softwaredeveloper", "softwaredev",
    literal("SDE"), literal("SWE"), # sometimes SE @_@
  ], "Competence"),
  Skill("System-Engineering", [
    "systemengineering", "systemengineer",
    "systemprogramming", "systemprogrammer",
    "systemdeveloper", "systemdev",
  ], "Competence"),
  Skill("Web-Engineering", [
    "webengineering", "webengineer",
    "webprogramming", "webprogrammer",
    "webdeveloper", "webdev",
    "webcoding", "webcoder",
  ], "Competence"),

  Skill("Operations", [
    "operations", "ops"
  ], "Competence", resolve=dis_root("Operations", {"Data", "Engineering", "ML", "Security"})), # , {"Engineering": "Dev"}
  Skill("Data-Operations", ["dataoperations", "dataops"], "Competence"),
  Skill("Engineering-Operations", ["devoperations", "devops"], "Competence", alias="Dev-Operations"),
  Skill("ML-Operations", ["mloperations", "mlops", "ai=ops"], "Competence"),
  Skill("Security-Operations", ["securityoperations", "secoperations", "secops"], "Competence"),

  Skill("Science", [
    "science(s)", "scientist"
  ], "Competence", resolve=dis_root("Science", {"Computer", "Data"})),
  Skill("Computer-Science", ["computerscience", "computerscientist", "comp=sci", literal("CS")], "Competence"),
  Skill("Data-Science", ["datascience", "datascientist", "data=sci", literal("DS")], "Competence"),

  Skill("Security", [
    "security", "secure" # move "defence" and "protection" here?
  ], "Competence", resolve=dis_root("Security", {"Data", "Network", "Web"})),
  Skill("Security", ["sec"], "Competence", disambiguate=neighbour(2)),
  Skill("Cyber-Security", ["cyber=security", "cyber=sec", "cyber=defence"], "Competence"),
  Skill("Data-Security", ["datasecurity", "data=sec", "data=protection"], "Competence"),
  Skill("Info-Security", ["information=security", "info=security", "info=sec"], "Competence"),
  Skill("Network-Security", ["networksecurity", "netsecurity", "net=sec"], "Competence"),
  Skill("Web-Security", ["websecurity", "web=sec"], "Competence"),

  # Quality Assurance Automation
  # QA Automation
  # Testing Automation
  # Test Automation
  # Automated Testing

  # Only sequential for now
  Skill("Testing", ["testing", "tested", "tester"], "Competence"), # TODO "test(s)"
  Skill("Testing:skip", ["battle-tested", "tested to"], "Competence", resolve=lambda _: []), # oversimplified, will update later
  Skill("E2E-Testing", ["e2e=testing", "e2e=test(s)", "e2e"], "Competence"),
  Skill("Automated-Testing", [
    "test=automation", "testing=automation",
    "automation=test", "automated=test", "automating=test",
    "automation=tester", "automated=tester", "automating=tester",
    "automation=testing", "automated=testing", "automating=testing",
  ], "Competence"),
  Skill("Integration-Testing", ["integration=testing", "integration=test(s)"], "Competence"),
  Skill("Functional-Testing", ["functional=testing", "functional=test(s)"], "Competence"),
  Skill("Load-Testing", ["load=testing", "load=test(s)"], "Competence"),
  Skill("Penetration-Testing", [
    "penetration=testing", "penetration=test(s)", "penetration=tester",
    "pen=testing", "pen=test", "pen=tester",
  ], "Competence"),
  Skill("Unit-Testing", ["unit=testing", "unit=test(s)"], "Competence"),
  Skill("Vulnerability-Testing", [
    "vulnerability=scanning", "vulnerability=scan(ner)",
    "vulnerability=testing", "vulnerability=test(s)", "vulnerability=tester",
  ], "Competence"),

  # TODO automated-testing vs test-automation @_@

  # Common prefixes
  Skill("AI", ["ai", "artificial-intelligence"], "Competence"),
  Skill("Business", ["business"], "Competence"),
  # ^ "entrepreneurship", "entrepreneur" ???
  Skill("Computer", ["computer", "computing"], "Competence"),
  Skill("Data", ["data"], "Competence"),
  Skill("Data:skip", [
    "personal=data", "user=data",
    "my=data", "your=data", "our=data", "their=data",
    "data=graph",
  ], "Competence", resolve=lambda _: []), # oversimplified, will update later
  Skill("Database", ["database(s)"], "Competence"),
  Skill("BigData", ["big=data"], "Competence"),
  Skill("Embedded", ["embedded"], "Competence"),
  Skill("Firmware", ["firmware"], "Competence"),
  Skill("Game", ["game"], "Competence"),
  Skill("Game:skip", ["game=theory"], "Competence", resolve=lambda _: []), # oversimplified, will update later
  Skill("Hardware", ["hardware"], "Competence"),
  Skill("IoT", ["iot", "internet-of-things"], "Competence"),
  Skill("Malware", ["malware"], "Competence"),
  Skill("ML", ["ml", "machine-learning"], "Competence"),
  Skill("Mobile", ["mobile", "mobileapp"], "Competence"),
  Skill("Network", ["networking", "network"], "Competence"),
  Skill("Robotics", ["robotics"], "Competence"),
  Skill("Software", ["software"], "Competence"),
  Skill("System", ["system(s)"], "Competence"), # TODO fix many FPs
  Skill("UI", ["ui", "user=interface", "human=interface"], "Competence"),
  Skill("UI/UX", ["ui=ux", "ui/ux", "uix"], "Competence"),
  Skill("UX", ["ux", "user=experience"], "Competence"),
  Skill("Web", ["web", "website", "webapp"], "Competence"),

  # Skill("SDLC", ["sdlc"], "Competence", resolve=lambda _: ["Software", "Engineering"]),
  # Skill("Malware", ["malware"], "Competence"),

  # # Common roots
  # Skill("Automation", ["automation", "automated"], "Competence"),
  # # Skill("*:Hacking", ["hacking", "hacker"], "Competence"),
  # # Skill("Learning", ["learning"], "Competence"),
  # Skill("Research", ["research", "reseacher"], "Competence"),
  # Skill("Visualization", ["visualization", "visualizer"], "Competence"),
  # # Skill("Leadership", ["leadership", "leader", "lead"], "Competence"),
  # # Skill("Management", ["management", "manager"], "Competence"),
  # Skill("Research", ["research", "researcher"], "Competence"),
  # Skill("Recruitment", ["recruitment", "recruiter", "staffing"], "Competence"),
  # # Skill("SRE", [literal("SRE")], "Competence"), # resolve=lambda _: ["Reliability", "Engineering"] ???

  Skill("Automation", ["automation", "automated", "automating"], "Competence", resolve=dis_automation()),
  Skill("Architecture", ["architecture"], "Competence"),
  Skill("Accessibility", ["accessibility", "accessible"], "Competence"),
  Skill("Decentralized", ["decentralized"], "Competence"),
  Skill("Distributed", ["distributed"], "Competence"),
  Skill("HighLoad", ["high=load"], "Competence"),
  # Highly Available, High Availability, high performance, high traffic,
  # Clustering, Sharding, load balancing
  # Replication, Partitioning | Enterprise, large-scale
  Skill("Performance", ["performance", "performant"], "Competence"),
  Skill("Scalability", ["scalability", "scalable"], ""),

  # Skill("Resiliency", ["resiliency", "resilient"], ""),
  # Skill("Reliability", ["reliability", "reliable"], "Competence"),
  # Skill("Deploy", ["deploy"], ""),
  # Skill("Integration", ["integration"], ""),
  # Skill("Scraping", ["scraping"], ""),
  # Skill("Algorithm", ["algorithm(s)"], ""),
  # Skill("CMS", ["cms"], ""),
  # Skill("E-Commerce", ["e=commerce"], ""),
  # Skill("Cluster", ["cluster"], ""),
  # Skill("Container", ["container"], ""),
  # Skill("Orchestration", ["orchestration"], ""),

  # STACKS
  Skill("DevSecOps:stack", [
    "dev/sec-ops", "sec/dev-ops",
    "dev-sec-ops", "sec-dev-ops",
    "devsecops", "secdevops",
  ], "Competence", resolve=lambda _: ["Dev-Operations", "Security-Operations"]),
  # Skill("ITOps", ["itops"], "Competence"), # ???

  # UNSORTED
  Skill("QA", ["quality-assurance", "qa"], "Competence"),
]
