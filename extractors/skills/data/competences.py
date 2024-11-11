from ...utils import noun, propn
from ..utils import Skill, neighbour

__all__ = ["SKILLS"]

SKILLS: list[Skill] = [
  # SOFTWARE ENGINEERING
  Skill("FP", ["fp"], ""),
  Skill("OOP", ["oop"], ""),

  Skill("Backend", ["backend(er)", noun("BE")], "Competence"),   # not detected as PROPN, needs to be retrained
  Skill("API", ["api"], ""),
  Skill("ORM", ["orm"], ""),
  Skill("REST", ["rest=api", propn("rest"), noun("REST")], ""),
  Skill("REST", ["rest"], "", disambiguate=neighbour(2)),
  Skill("RPC", ["rpc=api", "rpc"], ""),
  Skill("SOAP", ["soap"], ""),
  Skill("gRPC", ["grpc"], ""),
  Skill("tRPC", ["trpc"], ""),

  Skill("Frontend", ["frontend(er)", noun("FE")], "Competence"), # not detected as PROPN, needs to be retrained
  Skill("DOM", ["dom"], ""),
  Skill("UI/UX", ["ui", "ux", "user=interface", "user=experience"], ""),
  Skill("Browser", ["browser"], ""),
  Skill("DevTools", ["dev=tools"], ""),

  Skill("Web", ["web", "webdev"], "Competence"),
  Skill("Fullstack", ["fullstack(er)"], "Competence"),

  Skill("Blockchain", ["blockchain"], "Competence"),
  Skill("Web3", ["web3"], "Competence"),
  Skill("dApp", ["dapp(s)"], "Competence"),
  Skill("Crypto", ["crypto"], "Competence"),

  Skill("Low-Code", ["low=code", "no=code"], "Competence"),

  Skill("Mobile", ["mobile", "mobiledev"], "Competence"),
  Skill("Cross-Platform", ["cross=platform"], "Competence"),

  # Skill("Game", ["game", "gamedev"], "Competence"),

  Skill("Infrastructure", ["infrastructure"], "Competence"),
  Skill("Cloud", ["cloud"], "Competence"),
  Skill("Ops", ["ops"], "Competence"), # TODO operations
  Skill("DataOps", ["dataops"], "Competence"),
  Skill("DevOps", ["devops"], "Competence"),
  Skill("MlOps", ["mlops"], "Competence"),
  Skill("SecOps", ["secops"], "Competence"),
  Skill("IaaS", ["iaas"], ""),
  Skill("PaaS", ["paas"], ""),
  Skill("SaaS", ["saas"], ""),
  Skill("Orchestration", ["orchestration"], ""),
  # Deploy

  Skill("Automation", ["automation"], "Competence"),
  Skill("QA", ["qa"], "Competence"),

  Skill("ETL", ["etl"], "Competence"),
  Skill("ELT", ["elt"], "Competence"),
  Skill("DWH", ["dwh"], "Competence"),

  Skill("Performance", ["performance"], "Competence"),
  Skill("Security", ["security"], "Competence"),
  Skill("Network", ["network"], "Competence"), # TODO networking
  Skill("Robotics", ["robotics"], "Competence"),

  Skill("AI", ["artificial=intelligence", "ai"], "Competence"),
  Skill("Big-Data", ["big=data"], "Competence"),
  Skill("Data-Mining", ["data=mining"], "Competence"),
  # Scraping # Data-Extraction
  Skill("Machine-Learning", ["machine=learning"], "Competence"),
  Skill("Deep-Learning", ["deep=learning"], "Competence"),
  Skill("Computer-Vision", ["computer=vision"], "Competence"),
  Skill("Natural-Language-Processing", ["natural=language=processing", "nlp"], "Competence"),
  Skill("Large-Language-Models", ["large=language=model(s)", "llm"], "Competence"),
  # Motion-Prediction
  # Sensor-Fusion

  Skill("Software", ["software"], "Competence"),
  Skill("Hardware", ["hardware"], "Competence"),
  Skill("Firmware", ["firmware"], "Competence"),
  Skill("Embedded", ["embedded"], "Competence"),
  Skill("System", ["system"], "Competence"),

  Skill("IoT", ["iot"], "Competence"),

  # Sciences
  Skill("Biochemistry", ["biochemistry"], "Science"),
  Skill("Informatics", ["informatics"], "Science"),
  Skill("Statistics", ["statisics"], "Science"),

  # Analysis
  Skill("Analysis", ["analysis"], ""),
  Skill("Analytics", ["analytics"], ""),
]

# Non-skills (words that look like skills but are not, might be useful to help with them in UI)
# SOTA: state of the art
