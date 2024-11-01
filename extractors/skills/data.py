from dataclasses import dataclass
from typing import Any

__all__ = ["Skill", "SKILLS"]

IN, LOWER, OP, REGEX, TEXT = "IN", "LOWER", "OP", "REGEX", "TEXT"

def ver1(word: str) -> list[dict[str, Any]]:
  return [
    {LOWER: {REGEX: r"^" + word + r"[-\d.]{0,4}$"}}
  ]

@dataclass
class Skill:
  name: str
  phrases: list[
    str |                # Custom lang (produces exact matches)
    tuple[str, str] |    # Custom shortcut to narrow POS
    list[dict[str, Any]] # Spacy pattern
  ]

SKILLS: list[Skill] = [
  # ANALYSIS
  Skill(name="Excel", phrases=[("excel", "NOUN")]),
  Skill(name="Google-Sheets", phrases=["google=sheets"]),
  Skill(name="Power-BI", phrases=["power=bi"]),
  Skill(name="Tableau", phrases=["tableau"]),

  # CLOUD
  Skill(name="Azure", phrases=["azure"]),
  Skill(name="AWS", phrases=["aws"]),
  Skill(name="Heroku", phrases=["heroku"]),
  Skill(name="Google-Cloud", phrases=["google=cloud", "gcp"]),
  Skill(name="Netlify", phrases=["netlify"]),
  Skill(name="Vercel", phrases=["vercel"]),

  # MOBILE & CROSS-PLATFORM
  Skill(name="Android", phrases=["android"]),
  Skill(name="Cordova", phrases=["cordova", "phonegap"]),
  Skill(name="Dagger2", phrases=["dagger2"]),
  Skill(name="Flutter", phrases=["flutter"]),
  Skill(name="Ionic", phrases=["ionic"]),
  Skill(name="Jetpack-Compose", phrases=["jetpack=compose"]),
  Skill(name="iOS", phrases=["ios"]),
  Skill(name="Lottie", phrases=["lottie"]),
  Skill(name="Onsen UI", phrases=["onsen", "onsen=ui"]),
  Skill(name="Native-Script", phrases=["native=script"]),
  Skill(name="React-Native", phrases=["react=native"]),
  Skill(name="Retrofit", phrases=["retrofit"]),
  Skill(name="Xamarin", phrases=["xamarin"]),
  # Titanium -- disambiguate
  Skill(name="Vue-Native", phrases=["vue=native"]),

  # BIGDATA
  Skill(name="Apache-Kafka", phrases=["apache=kafka", "kafka"]),
  Skill(name="Apache-Hadoop", phrases=["apache=hadoop", "hadoop"]),
  Skill(name="Apache-Spark", phrases=["apache=spark", "spark"]), # also ANALYTICS
  Skill(name="Amazon-Redshift", phrases=["amazon=redshift", "aws=redshift", "redshift"]),
  Skill(name="ELK-Stack", phrases=["elk", "elk=stack"]),
  Skill(name="Google-BigQuery", phrases=["google=bigquery"]),

  # DATABASE
  Skill(name="Apache-Cassandra", phrases=["apache=cassandra", "cassandra"]),
  Skill(name="CouchBase", phrases=["couchbase"]),
  Skill(name="CouchDB", phrases=["couch=db"]),
  Skill(name="DynamoDB", phrases=["dynamo=db"]),
  Skill(name="Elasticsearch", phrases=["elastic=search"]),
  Skill(name="Firebase", phrases=["firebase"]),
  Skill(name="MariaDB", phrases=["maria=db"]),
  Skill(name="Memcached", phrases=["memcache(d)"]),
  Skill(name="MongoDB", phrases=["mongo", "mongo=db"]),
  Skill(name="Microsoft-SQL", phrases=["microsoft=sql", "ms=sql", "sql=server"]),
  Skill(name="MySQL", phrases=["my=sql"]),
  Skill(name="Neo4j", phrases=["neo4j", "neo4j=db"]),
  Skill(name="Oracle", phrases=["oracle", "oracle=db"]),
  Skill(name="PouchDB", phrases=["pouch=db"]),
  Skill(name="PostgreSQL", phrases=["psql", "pgsql", "postgres", "postgre=sql", "postgres=sql"]),
  Skill(name="Redis", phrases=["redis"]),
  Skill(name="S3", phrases=["s3", "aws=s3", "amazon=s3"]),
  Skill(name="SQLite", phrases=[ver1("sqlite")]),

  # DATA SCIENCE
  Skill(name="Anaconda", phrases=["anaconda", "conda", "miniconda"]),
  Skill(name="Beautiful-Soup", phrases=["beautiful=soup"]),
  Skill(name="IPython", phrases=["ipython"]), # interactive shell
  Skill(name="Jupyter", phrases=["jupyter", "jupyter=lab", "jupyter=notebook(s)"]),
  Skill(name="Matplotlib", phrases=["matplotlib"]),
  Skill(name="Numba", phrases=[[{LOWER: "numba"}, {OP: "!", LOWER: {IN: ["1", "one", "wan"]}}]]),
  Skill(name="NumPy", phrases=["numpy"]),
  Skill(name="Pandas", phrases=["pandas"]),
  Skill(name="PyTorch", phrases=["pytorch"]),
  Skill(name="Keras", phrases=["keras"]),
  Skill(name="Scikit-Learn", phrases=["scikit=learn", "sklearn"]),
  Skill(name="SciPy", phrases=["scipy"]),
  Skill(name="Seaborn", phrases=["seaborn"]),
  Skill(name="Spacy", phrases=["spacy"]),
  Skill(name="Tensorflow", phrases=["tensorflow"]),

  # GAME
  Skill(name="Godot-Engine", phrases=["godot", "godot=engine"]),
  Skill(name="Phaser", phrases=["phaser", "phaser.=js"]),
  Skill(name="PixiJS", phrases=["pixi", "pixi.=js"]),
  Skill(name="PyGame", phrases=["pygame"]),
  Skill(name="Solar2D", phrases=["solar2d"]),
  Skill(name="Unity", phrases=["unity", "unity=3d", "unity=platform"]),
  Skill(name="Unreal-Engine", phrases=["unreal", "unreal=engine", "ue4", "ue5", "ue-4", "ue-5"]),
  Skill(name="ThreeJS", phrases=["three.=js"]),

  # WEB BACKEND
  Skill(name="ASP", phrases=["asp", "asp.net"]),
  Skill(name="Blazor", phrases=["blazor"]),
  Skill(name="Bun", phrases=["bun"]),
  Skill(name="CakePHP", phrases=["cake=php"]),
  Skill(name="CherryPy", phrases=["cherry=py"]),
  Skill(name="CodeIgniter", phrases=["code=igniter"]),
  Skill(name="Deno", phrases=["deno"]),
  Skill(name="Django", phrases=["django"]),
  Skill(name="Express", phrases=["express", "express.=js"]),
  Skill(name="FastAPI", phrases=["fast=api"]),
  Skill(name="Fastify", phrases=["fastify"]),
  Skill(name="Flask", phrases=["flask"]),
  Skill(name="Hasura", phrases=["hasura"]),
  Skill(name="Koa", phrases=["koa"]),
  Skill(name="Laravel", phrases=["laravel"]),
  Skill(name="NestJS", phrases=["nest.=js"]),
  Skill(name="Nginx", phrases=["nginx"]),
  Skill(name="Phoenix", phrases=["phoenix"]),
  Skill(name="Ruby-on-Rails", phrases=["rails", "ror", "ruby=on=rails"]),
  Skill(name="SailsJS", phrases=["sails.=js"]),
  Skill(name="Spring", phrases=["spring"]),
  Skill(name="Symfony", phrases=["symfony"]),
  Skill(name="Yii", phrases=["yii"]),

  # WEB FRONTEND
  Skill(name="Angular", phrases=["angular", "angular.=js"]),
  Skill(name="Astro", phrases=["astro", "astro.=js"]),
  Skill(name="Bootstrap", phrases=["bootstrap"]),
  Skill(name="Chakra-UI", phrases=["chakra", "chakra=ui"]),
  Skill(name="D3JS", phrases=["d3", "d3.=js"]),
  Skill(name="EmberJS", phrases=["ember", "ember.=js"]),
  Skill(name="Figma", phrases=["figma"]),
  Skill(name="jQuery", phrases=["jquery"]),
  Skill(name="Material-UI", phrases=["material=ui", "mui"]),
  Skill(name="Photoshop", phrases=["photoshop"]),
  Skill(name="React", phrases=["react", "react.=js"]),
  Skill(name="SolidJS", phrases=["solid.=js"]),
  Skill(name="Svelte", phrases=["svelte", "svelte.=js"]),
  Skill(name="VueJS", phrases=["vue", "vue.=js"]),
  Skill(name="Tailwind-CSS", phrases=["tailwind", "tailwind.=css"]),
  Skill(name="Vite", phrases=["vite"]),
  Skill(name="Webpack", phrases=["webpack"]),

  # WEB FULLSTACK
  Skill(name="GraphQL", phrases=["graphql"]),
  Skill(name="HTMX", phrases=["htmx"]),
  Skill(name="Meteor", phrases=["meteor", "meteor.=js"]),
  Skill(name="MEAN-Stack", phrases=["mean=stack"]), # "mean" TODO
  Skill(name="MERN-Stack", phrases=["mern", "mern=stack"]),
  Skill(name="NextJS", phrases=["next.=js"]), # what about just "Next"
  Skill(name="NuxtJS", phrases=["nuxt", "nuxt.=js"]),
  Skill(name="NodeJS", phrases=["node.=js"]), # just "Node" gives many FP
  Skill(name="SvelteKit", phrases=["svelte=kit"]),
  Skill(name="WebAssembly", phrases=["web=assembly"]),

  # LOW-CODE
  Skill(name="Airtable", phrases=["airtable"]),
  Skill(name="Bitrix", phrases=["bitrix", "bitrix24"]),
  Skill(name="Drupal", phrases=["drupal"]),
  Skill(name="Hygraph", phrases=["hygraph", "graph=cms"]),
  Skill(name="Joomla", phrases=["joomla"]),
  Skill(name="Magento", phrases=["magento"]),
  Skill(name="Power-Apps", phrases=["power=apps"]),
  Skill(name="Power-Automate", phrases=["power=automate"]),
  Skill(name="Power-Platform", phrases=["power=platform"]),
  Skill(name="Shopify", phrases=["shopify"]),
  Skill(name="Strapi", phrases=["strapi"]),
  Skill(name="WooCommerce", phrases=["woo=commerce"]),
  Skill(name="Wordpress", phrases=["wordpress"]),

  # INFRASTRUCTURE
  Skill(name="Apache-Airflow", phrases=["airflow", "apache=airflow"]), # also BIGDATA
  Skill(name="Ansible", phrases=["ansible"]),
  Skill(name="CKA", phrases=["cka"]), # certificate
  Skill(name="CKAD", phrases=["ckad"]), # certificate
  Skill(name="CompTIA-ITOps", phrases=["cios"]), # certificate
  Skill(name="MCSA", phrases=["mcsa"]), # certificate
  Skill(name="Docker", phrases=["docker"]),
  Skill(name="Dokku", phrases=["dokku"]), # also Cloud
  Skill(name="Jenkins", phrases=["jenkins"]),
  Skill(name="Kibana", phrases=["kibana"]), # also BIGDATA
  Skill(name="Kubernetes", phrases=["kubernetes", "k8s"]),
  Skill(name="Logstash", phrases=["logstash"]), # also BIGDATA
  Skill(name="Pulumi", phrases=["pulumi"]),
  Skill(name="Puppet", phrases=["puppet"]),
  Skill(name="Splunk", phrases=["splunk"]), # also BIGDATA & SECURITY
  Skill(name="RHCE", phrases=["rhce"]),   # certificate
  Skill(name="RHCSA", phrases=["rhcsa"]), # certificate
  Skill(name="Terraform", phrases=["terraform"]),
  Skill(name="Vagrant", phrases=["vagrant"]),

  # QA-n-AUTOMATION
  Skill(name="Appium", phrases=["appium"]),
  Skill(name="Cucumber", phrases=["cucumber"]),
  Skill(name="Cypress", phrases=["cypress", "cypress.=js"]),
  Skill(name="Jasmine", phrases=["jasmine"]),
  Skill(name="Jest", phrases=["jest"]),
  Skill(name="JUnit", phrases=["junit"]),
  Skill(name="Playwright", phrases=["playwright"]),
  Skill(name="Postman", phrases=["postman"]),
  Skill(name="Protractor", phrases=["protractor"]),
  Skill(name="PyTest", phrases=["pytest"]),
  Skill(name="Selenium", phrases=["selenium"]),
  Skill(name="TestCafe", phrases=["testcafe"]),
  Skill(name="TestNg", phrases=["testng"]),
  Skill(name="WebdriverIO", phrases=["webdriverio"]),

  # BLOCKCHAIN
  Skill(name="Bitcoin", phrases=["bitcoin"]),
  Skill(name="Ethereum", phrases=["ethereum"]),
  # Skill(name="Web3", phrases=["web3"]), topic/concept, not a skill

  # NETWORKING
  Skill(name="CompTIA-Network+", phrases=["network+", "comptia n(etwork)+"]), # certificate
  Skill(name="Cisco-CNA", phrases=["ccna"]), # certificate
  Skill(name="Cisco-CNP", phrases=["ccnp"]), # certificate
  Skill(name="MTCNA", phrases=["mtcna"]),    # certificate
  Skill(name="Nmap", phrases=["nmap"]),             # also SECURITY
  Skill(name="Wireshark", phrases=["wireshark"]),   # also SECURITY
  Skill(name="Netcat", phrases=["netcat", "ncat"]), # also SECURITY

  # SECURITY
  Skill(name="Burpsuite", phrases=["burpsuite"]),
  Skill(name="CEH", phrases=["ceh"]),     # certificate
  Skill(name="CISA", phrases=["cisa"]),   # certificate
  Skill(name="CISM", phrases=["cism"]),   # certificate
  Skill(name="CISSP", phrases=["ciss", "cissp"]), # certificate
  Skill(name="CompTIA-PenTest+", phrases=["pentest+", "comptia p(entest)+"]), # certificate
  Skill(name="CompTIA-Security+", phrases=["security+", "comptia s(ecurity)+"]), # certificate
  Skill(name="GIAC-CIH", phrases=["gcih"]),   # certificate
  Skill(name="GIAC-SEC", phrases=["gsec"]),   # certificate
  Skill(name="GIAC-REM", phrases=["grem"]),   # certificate
  Skill(name="GIAC-WAPT", phrases=["gwapt"]), # certificate
  Skill(name="SSCP", phrases=["sscp"]),       # certificate
  Skill(name="Metasploit", phrases=["metasploit"]),
  Skill(name="Nessus", phrases=["nessus"]),
  Skill(name="Snort", phrases=[("snort", "NOUN")]),

  # ROBOTICS
  Skill(name="ROS", phrases=["ros"]), # also EMBEDDED-n-SYSTEM
  Skill(name="FreeRTOS", phrases=["freertos"]), # also EMBEDDED-n-SYSTEM

  # EMBEDDED-n-SYSTEM
  Skill(name="Arduino", phrases=["arduino"]),
  Skill(name="ARM", phrases=["arm"]), # CPU family
  Skill(name="AVR", phrases=["avr"]), # microcontrollers
  Skill(name="ESP32", phrases=["esp=32"]), # microcontrollers
  Skill(name="ESP8266", phrases=["esp=8266"]), # microcontrollers
  Skill(name="MicroPython", phrases=["micro=python"]), # compiler
  Skill(name="MSP430", phrases=["msp=430"]), # microcontrollers
  Skill(name="Raspberry-Pi", phrases=["raspberry", "rasp=pi", "raspberry=pi(s)"]),
  Skill(name="STM32", phrases=["stm=32"]), # microcontrollers
  Skill(name="Z80", phrases=["Z=80"]), # microcontrollers

  # DESKTOP
  # Skill(name="Electron", phrases=["electron"]), tons of FP

  # LANGUAGES
  Skill(name="Assembly", phrases=["assembly"]),
  Skill(name="Ada", phrases=["ada"]),
  Skill(name="Apex", phrases=["apex"]),
  Skill(name="C", phrases=["c", "c=lang"]),
  Skill(name="C++", phrases=["c++", "cplusplus"]),
  Skill(name="C#", phrases=["c#", "csharp"]),
  Skill(name="Clojure", phrases=["clojure", "clojurian"]),
  Skill(name="ClojureScript", phrases=["clojure=script"]),
  Skill(name="Cobol", phrases=["cobol"]),
  Skill(name="Crystal", phrases=["crystal", "crystal=lang"]),
  Skill(name="CSS", phrases=[ver1("css")]),
  Skill(name="D", phrases=["d", "d=lang"]),
  Skill(name="Dart", phrases=["dart"]),
  Skill(name="Delphi", phrases=["delphi"]),
  Skill(name="Elixir", phrases=["elixir"]),
  Skill(name="Elm", phrases=["elm"]),
  Skill(name="Erlang", phrases=["erlang"]),
  Skill(name="Fortran", phrases=["fortran"]),
  Skill(name="F#", phrases=["f#", "f=lang", "fsharp"]),
  Skill(name="GDScript", phrases=["gdscript"]),
  Skill(name="Gleam", phrases=["gleam"]),
  Skill(name="Go", phrases=[("go", "NOUN"), "golang"]),
  Skill(name="Groovy", phrases=["groovy"]),
  Skill(name="Haskell", phrases=["haskell"]),
  Skill(name="HTML", phrases=[ver1("html")]),
  Skill(name="Java", phrases=[ver1("java")]),
  Skill(name="JavaScript", phrases=["java=script", "js"]),
  Skill(name="Julia", phrases=["julia"]),
  Skill(name="Kotlin", phrases=["kotlin"]),
  Skill(name="Lisp", phrases=["lisp"]),
  Skill(name="Lua", phrases=["lua"]),
  Skill(name="Nim", phrases=["nim"]),
  Skill(name="Matlab", phrases=["matlab"]),
  Skill(name="Mojo", phrases=["mojo"]),
  Skill(name="Objective-C", phrases=["objective=c"]),
  Skill(name="Ocaml", phrases=["ocaml"]),
  Skill(name="Odin", phrases=["odin"]),
  Skill(name="Perl", phrases=["perl"]),
  Skill(name="PHP", phrases=[ver1("php")]),
  Skill(name="PowerShell", phrases=["power=shell"]),
  Skill(name="Prolog", phrases=["prolog"]),
  Skill(name="Python", phrases=["python", "pythonist(a)"]),
  Skill(name="R", phrases=["r", "r=lang"]),
  Skill(name="Ruby", phrases=["ruby", "ruby=lang"]),
  Skill(name="Rust", phrases=["rust", "rustacean"]),
  Skill(name="SASS", phrases=["sass", "scss"]),
  Skill(name="Scala", phrases=["scala"]),
  Skill(name="Solidity", phrases=["solidity"]),
  Skill(name="Swift", phrases=["swift"]),
  Skill(name="TypeScript", phrases=["type=script", "ts"]),
  Skill(name="Shell", phrases=["bash", "shell"]),
  Skill(name="SQL", phrases=["sql"]),
  Skill(name="XML", phrases=["xml"]),
  Skill(name="V", phrases=["v", "vlang"]),
  Skill(name="Vyper", phrases=["vyper"]),
  Skill(name="Visual-Basic", phrases=["vb(a)", "vb.net", "visual=basic"]),
  Skill(name="Zig", phrases=["zig"]),

  # UNSORTED
  Skill(name="Blender", phrases=["blender"]),
  Skill(name="CompTIA-A+", phrases=["comptia a+"]), # certificate for tech. support and IT ops
  Skill(name="SalesForce", phrases=["salesforce"]),
]

# // SECURITY TOOLS
# // Aircrack-ng: 454 repos, 5 users
# // Nikto: 352 repos -- too many false positives
# // John the Ripper: 210 repos, 7 ysers
#
# export const rawSkillTable: Dict<SkillRow> = {
#   ".NET": {pattern: "asp.net, dotnet=core, dotnet, .net=core, .net", category: "platform", role: "Engineer"},
#   // .NET is a general-purpose platform for Windows development
#   // TODO ASP.NET is a framework for web service (backend) development, a part of .NET platform
#   // "Apache": -- ambiguous
#   "Apollo": {pattern: "apollo=js, apollo=client, apollo=server, apollo", category: "platform", role: "Engineer"},
#   "Chef": {pattern: "chef", category: "platform", role: "Engineer"},
#   // should we add new char like "css𝐕" or should we consume numbers after EACH term?
#   // Most skills have versions BUT topics don't @_@
#   // So it can be a per-table configuration
#   "ETL": {pattern: "etl", category: "topic", role: "Engineer"},
#   "FTP": {pattern: "s?ftp", category: "tech"},
#   "HTTP": {pattern: "http", category: "tech"},
#   "Native Android": {pattern: "native=android", category: "platform", role: "Engineer"},
#   "Native iOS": {pattern: "native-ios", category: "platform", role: "Engineer"},
#   "NetBeans": {pattern: "netbeans", category: "tech"},
#   "Octave": {pattern: "octave", category: "lang"},
#   "OpenCV": {pattern: "opencv", category: "tech"},
#   // "Polygon": {pattern: "polygon", category: "tech", role: "Engineer"},
#   "Prisma": {pattern: "prisma", category: "tech", role: "Engineer"},
#   "OpenAPI": {pattern: "open=api", category: "tech"},
#   "OpenAuth": {pattern: "open=auth2?, oauth2?", category: "tech"},
#   "REST": {pattern: "rest=api, !REST", category: "tech"},
#   "tRPC": {pattern: "trpc", category: "tech"},
#   "RPC": {pattern: "rpc", category: "tech"},
#   "RxJS": {pattern: "rx.=js, RX", category: "tech", role: "Engineer"},
#   "Spark": {pattern: "spark", category: "tech", role: "Engineer"}, // or Apache Spark?
#   "Salt": {pattern: "salt", category: "platform", role: "Engineer"},
#   "Vyper": {pattern: "vyper", category: "lang", role: "Engineer"},
#   "Web3.js": {pattern: "web3.js", category: "tech"},
#
#   "Windows": {pattern: "windows", category: "platform", role: "Engineer"},
#   "macOS": {pattern: "mac=os", category: "platform", role: "Engineer"},
#   "Linux": {pattern: "linux, ubuntu", category: "platform", role: "Engineer"},
#   "Unix": {pattern: "unix", category: "platform", role: "Engineer"},
#   "iOS": {pattern: "ios", category: "platform", role: "Engineer"},
#   "Android": {pattern: "android", category: "platform", role: "Engineer"},
#
#   // TOPICS ----------------------------------------------------------------------------------------
#   "Application": {pattern: "application", category: "topic"},
#   "Security": {pattern: "cyber=security, cyber=sec, it=security, security", category: "topic"},
#   "Performance": {pattern: "performance", category: "topic"},
#   "Scalability": {pattern: "scalability", category: "topic"},
#   "Vulnerability": {pattern: "vulnerability, penetration, VA/PT", category: "topic"},
#   "Testing": {pattern: "testing", category: "topic"},
#   "Business": {pattern: "business, biz, !BI", category: "topic"},
#   "Biotech": {pattern: "biotech", category: "topic"},
#   "Fintech": {pattern: "fintech", category: "topic"},
#   "Edtech": {pattern: "edtech", category: "topic"},
#   "E-commerce": {pattern: "e=commerce", category: "topic"},
#   "Open Source": {pattern: "open=source, fl?oss, f?oss", category: "topic"},
#   "Robotics": {pattern: "robotics, robocon", category: "topic"},
#   "Mathematics": {pattern: "mathematics, maths?", category: "topic"},
#   "CI/CD": {pattern: "ci/=cd", category: "topic"},
#   "UI/UX": {pattern: "u[ix]/=u[ix], u[ix], user=interface, human=interface", category: "topic"},
#   "Chemistry": {pattern: "chemistry", category: "topic"},
#   "Physics": {pattern: "physics", category: "topic"},
#   "Photography": {pattern: "photography", category: "topic"},
#   "2D": {pattern: "2d", category: "topic"},
#   "3D": {pattern: "3d", category: "topic"},
#   // "Font": {pattern: "fonts?", category: "topic"}, // disambiguate?
#   "Animation": {pattern: "animation, motion", category: "topic"},
#   "Automation": {pattern: "automation", category: "topic", role: "Engineer"},
#   "Backend": {pattern: "back=end, !BE", category: "topic", role: "Engineer"},
#   "Blockchain": {pattern: "block=chain, smart=contract", category: "topic", role: "Engineer"},
#   "Cloud": {pattern: "cloud=native, cloud", category: "topic", role: "Engineer"},
#   "DevOps": {pattern: "", category: "topic", role: "Engineer"},
#   "Fullstack": {pattern: "full=stack", category: "topic", role: "Engineer"},
#   "Mobile": {pattern: "mobile", category: "topic"},
#   "Game": {pattern: "!game", category: "topic"},
#   "Graphic": {pattern: "graphics?", category: "topic", role: "Designer"},
#   "Software": {pattern: "software, !SW", category: "topic", role: "Engineer"},
#   "Hardware": {pattern: "hardware", category: "topic", role: "Engineer"},
#   "Firmware": {pattern: "firmware", category: "topic", role: "Engineer"},
#   "Frontend": {pattern: "front=end, !FE", category: "topic", role: "Engineer"},
#   "QA": {pattern: "", category: "topic", role: "Engineer"},
#   "Embedded": {pattern: "embedded", category: "topic", role: "Engineer"},
#   "IoT": {pattern: "iot", category: "topic", role: "Engineer"},
#   "Computer Vision": {pattern: "computer=vision", category: "topic"},
#   "AI": {pattern: "artifical=intelligence, ai", category: "topic"},
#   "Level": {pattern: "level", category: "topic"},
#   "Enterprise": {pattern: "enterprise", category: "topic"},
#   "CMS": {pattern: "cms", category: "topic", role: "Engineer"},
#   "Headless CMS": {pattern: "headless=cms", category: "topic", role: "Engineer"},
#   "Low-Code": {pattern: "low=code", category: "topic", role: "Engineer"},
#
#   "Analytics": {pattern: "analytics", category: "topic", role: "Analyst"},
#   "Architecture": {pattern: "architecture", category: "topic", role: "Architect"},
#   "Design": {pattern: "design", category: "topic", role: "Designer"},
#   "Engineering": {pattern: "engineering, R&D", category: "topic", role: "Engineer"},
#   "Development": {pattern: "Development", category: "topic", role: "Engineer"},
#   "Management": {pattern: "management", category: "topic", role: "Manager"},
#   "Science": {pattern: "science", category: "topic", role: "Scientist"},
#
#   // Role-agnostic (multi-role) topics
#   "Data": {pattern: "big=data, data", category: "topic"},
#   "Database": {pattern: "database=design, databases?", category: "topic"},
#   "Infrastructure": {pattern: "infrastructure", category: "topic"}, // role: "Engineer" / "Architect"
#   "Manual": {pattern: "manual", category: "topic"},
#   "Marketing": {pattern: "marketing", category: "topic"},
#   "R&D": {pattern: "r ?& ?d", category: "topic"},
#   "Sales": {pattern: "sales", category: "topic"}, // another problematic word @_@
#   "System": {pattern: "systems?", category: "topic"},
#   "Web": {pattern: "web", category: "topic"},
#   "Typography": {pattern: "typography", category: "topic"},
#   "Startup": {pattern: "startups?", category: "topic"},
#   "Product": {pattern: "!Products?", category: "topic"},
#   "Project": {pattern: "!Projects?", category: "topic"},
#   "Solution": {pattern: "!Solutions?", category: "topic"},
#   "Team": {pattern: "!Teams?", category: "topic"},
#   "Data Science": {pattern: "data=science, DS", category: "topic"},
#   "Computer Science": {pattern: "computer=science, CS", category: "topic"},
#   "Statistics": {pattern: "statistics", category: "topic"},
#   "Machine Learning": {pattern: "machine=learning, ML", category: "topic"},
#   "Deep Learning": {pattern: "deep=learning", category: "topic"},
#   "NLP": {pattern: "natural=language=processing, nlp", category: "topic"},
#   "Functional Programming": {pattern: "functional=programming, fp", category: "topic"},
#   "Object Oriented Programming": {pattern: "object=oriented=programming, oop", category: "topic"},
#   "Tech": {pattern: "tech, technical", category: "topic"},
#   "Crypto": {pattern: "crypto, defi, web=3", category: "topic"}, // crypto enthusiast = crypto-currencies + decentralized finance (DeFi)
#   "E-Commerce": {pattern: "e=commerce", category: "topic"},
#
#   "API": {pattern: "api", category: "topic"},
#   "E2E": {pattern: "end=to=end, e2e", category: "topic"},
#   "TDD": {pattern: "tdd", category: "topic"},
#   "BDD": {pattern: "bdd", category: "topic"},
#   // Crypto vs Blockchain?!?!
#   // Containers?
#   // should nopCommerce -> eCommerce? But then NodeJS -> js, are there INVALID precedents like that?
#   // Cloud vs Web, Cloud-Native
#   //
#   // "Web" is found in "Amazon Web Services": skills vs topics
#
#   /*
#   UI/UX specific words
#   menu
#   button
#   mouse
#   keyboard (can be WEB or CLI)
#   screen
#   scroll, scrollbar
#   form (?)
#   theme
#   animation
#
#   FRONTEND specific words
#   image, img, gif, jpg, jpeg, png, woff
#   svg
#   canvas
#   bundler (webpack, vite)
#
#   BACKEND specific words
#   orm
#   ActiveRecord
#   migration
#   KV store
#
#   WEB specific words
#   mime, header
#   upload, download
#   HTTPs?, s?FTP
#
#
#   OS specific words
#   stdin, stdout, terminal, filesystem, socket, stream, thread, process
#   cli, command line, shell, runtime, schedule
#
#   SECURITY specific words
#   ssh, tls, ssl
#   token, authentication, authorization, jwt, cookie
#   ddos, session
#
#   DEVOPS specific words
#   cluster, container(?)
#   serverless, monitoring, logging
#   development, production, staging
#
#   DEVOPS terms
#   Nomad, Vault, Consul
#
#   ARCHITECT specific words
#   microservice, monolith, monorepo, Event-Driven, Vertical Slice
#   Distributed
#   large-scale
#   saas, paas
#   architectures?
#   scalability
#   performance
#   self-hosted
#
#   QA specific words
#   Reliability
#
#   SWE specific words
#   datastructure, algorithm, oop, fp, !SOLID
#   dependency injection middleware, concept, pattern, anti-patter, idiom, best practice
#   deploy, build, compiler
#   roadmap, computer science
#   coding skills, application ideas
#
#   TODO
#   RabbitMQ, CQRS
#   Kafka
#   ecommerce
#   infrastructure
#   Vulnerability
#   scanner
#   auth0, aws cognito, firebase auth
#   OpenID Connect Identity Provider
#   network
#   command
#
#   ???
#   client, server
#   */
# }
#
# // TODO should we have `ruby=lang` variations if we parse `ruby` nevertheless?
# // Or `=platform` if we really parse without it...
# // It all slows down the parser...
#
# // TODO GitHub Actions, GitLab CI/CD -- how to avoid false positives with GitHub
#
# //     {name: "Architecture", role: "Architect"},
# //     {name: "Analysis", role: "Analyst"},
# //     {name: "Analytics", role: "Analyst"},
# //     {name: "Engineering", role: "Engineer"},
# //     {name: "Development", role: "Engineer"},
#
# // TODO consider to capture "Web Frontend" as just "Frontend" because in such cases "Web"
# // simply clarifies "Frontend". Such person is not a "Web Developer" in the same sense.
#
# // https://github.com/ivan-kleshnin/devscanr/issues/701
#
# // 4. Terms that are useful in repositories but confusing in user bios
# // E.g. toast, menu, carousel, chartjs, palette, flexbox, bundler, webpack, vite, scrollbar
#
# // http://localhost:3000/platform/search/adw0rd
# // Why this profile has experienceYears: undefined?
