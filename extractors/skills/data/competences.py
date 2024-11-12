from ...utils import literal, noun, propn
from ..utils import Skill, neighbour

__all__ = ["SKILLS"]

SKILLS: list[Skill] = [
  # MANAGEMENT
  Skill("Agile", ["agile", "kanban", "scrum"], ""),

  # SOFTWARE ENGINEERING
  Skill("TDD", ["tdd"], ""),
  Skill("BDD", ["ddd"], ""),
  Skill("DDD", ["ddd"], ""),
  Skill("FP", ["fp", "фп"], ""),
  Skill("OOP", ["oop", literal("SOLID"), "ооп"], ""),
  # YAGNI, DRY, KISS, MVC

  Skill("Backend", ["backend(er)", noun("BE")], "Competence"),   # not detected as PROPN, needs to be retrained
  Skill("API", ["api"], ""),
  Skill("ORM", ["orm"], ""),
  Skill("REST", ["rest=api", propn("rest"), noun("REST")], ""),
  Skill("REST", ["rest"], "", disambiguate=neighbour(2)),
  Skill("RPC", ["rpc=api", "rpc"], ""),
  Skill("SOAP", ["soap"], ""),
  Skill("gRPC", ["grpc"], ""),
  Skill("SSG", ["ssg"], ""),
  Skill("SSR", ["ssr"], ""),
  Skill("tRPC", ["trpc"], ""),

  # FRONTEND
  Skill("Frontend", ["frontend(er)", noun("FE")], "Competence"), # not detected as PROPN, needs to be retrained
  # BEM, БЭМ
  Skill("DOM", ["dom"], ""),
  Skill("UI/UX", ["ui", "ux", "user=interface", "user=experience"], ""),
  Skill("Browser", ["browser"], ""),
  Skill("DevTools", ["dev=tools"], ""),
  Skill("MPA", ["mpa"], ""),
  Skill("SPA", ["spa"], ""),
  Skill("OpenAPI", ["openapi"], ""),
  Skill("IP", ["ip"], ""),
  Skill("TCP", ["tcp"], ""),
  Skill("HTTP", ["http"], ""),
  Skill("HTTPS", ["https"], ""),
  Skill("WebSocket", ["websocket", "ws"], ""),

  Skill("Web", ["web", "webdev"], "Competence"),
  Skill("Fullstack", ["fullstack(er)"], "Competence"),

  Skill("Blockchain", ["blockchain"], "Competence"),
  Skill("Web3", ["web3"], "Competence"),
  Skill("dApp", ["dapp(s)"], "Competence"),
  Skill("Crypto", ["crypto"], "Competence"),

  # LOW-CODE
  Skill("Low-Code", ["low=code", "no=code"], "Competence"),
  Skill("CMS", ["cms"], "Competence"),
  Skill("CRM", ["crm"], "Competence"),
  Skill("IaaS", ["iaas"], ""), # INFRASTRUCTURE
  Skill("PaaS", ["paas"], ""), # INFRASTRUCTURE
  Skill("SaaS", ["saas"], ""),

  # MOBILE
  Skill("Mobile", ["mobile", "mobiledev"], "Competence"),
  Skill("Cross-Platform", ["cross=platform"], "Competence"),

  # Skill("Game", ["game", "gamedev"], "Competence"),

  # DATABASE, QUERY-LANGUAGES
  Skill("Database", ["database(s)"], ""),
  Skill("SQL", ["sql"], ""),
  Skill("NoSQL", ["nosql"], ""),
  Skill("GraphQL", ["graphql"], ""),

  # PL UMBRELLAS
  Skill("Assembly", ["assembly"], ""),

  # INFRASTRUCTURE
  Skill("Infrastructure", ["infrastructure"], "Competence"),
  Skill("Cloud", ["cloud"], "Competence"),
  Skill("Ops", ["ops"], "Competence"), # TODO operations
  Skill("DataOps", ["dataops"], "Competence"),
  Skill("DevOps", ["devops"], "Competence"),
  Skill("MlOps", ["mlops"], "Competence"),
  Skill("SecOps", ["secops"], "Competence"),
  Skill("Orchestration", ["orchestration"], ""),
  # Deploy

  Skill("Automation", ["automation"], "Competence"),
  Skill("QA", ["qa"], "Competence"),

  Skill("ETL", ["etl", "elt"], "Competence"),
  Skill("DWH", ["dwh"], "Competence"),

  # Skill("Accessibility", ["accessibility", "accessible"], "Competence"),
  # Skill("Performance", ["performance", "performant"], "Competence"),
  Skill("Security", ["security", "secure"], "Competence"),
  # Skill("Reliability", ["realibility", "reliable"], "Competence"),
  # Skill("Resilience", ["resilience", "resilient"], "Competence"),
  # Skill("Scalability", ["scalability", "scalable", ], "Competence"),
  # Skill("Observability", ["observability", "observable"], "Competence"),
  # Skill("Usability", ["usability", "usable"], "Competence"),

  Skill("Network", ["network"], "Competence"), # TODO networking

  Skill("Robotics", ["robotics"], "Competence"),
  Skill("Computer-Vision", ["computer=vision"], "Competence"),

  Skill("Decentralized", ["decentralized"], "Competence"),
  Skill("Distributed", ["distributed"], "Competence"),
  Skill("HighLoad", ["high=load"], "Competence"),
  # Highly Available, High Availability, high performance, high traffic,
  # Clustering, Sharding, load balancing
  # Replication, Partitioning | Enterprise, large-scale
  # Big Data  Data-heavy, logic-heavy

  Skill("AI", ["artificial=intelligence", "ai"], "Competence"),
  Skill("Big-Data", ["big=data"], "Competence"),
  Skill("Data-Mining", ["data=mining"], "Competence"),
  # Scraping # Data-Extraction
  Skill("Machine-Learning", ["machine=learning"], "Competence"),
  Skill("Deep-Learning", ["deep=learning"], "Competence"),
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
