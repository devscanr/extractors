from spacy.tokens import Span
from ...utils import IN, LOWER, OP, literal, propn, ver1
from ..utils import Disambiguate, Skill, contextual, contextual_or_neighbour, neighbour, singleletter
from .adobe import SKILLS as ADOBE_SKILLS
from .amazon import SKILLS as AMAZON_SKILLS
from .apache import SKILLS as APACHE_SKILLS
from .apple import SKILLS as APPLE_SKILLS
from .cisco import SKILLS as CISCO_SKILLS
from .companies import SKILLS as COMPANIES_SKILLS
from .google import SKILLS as GOOGLE_SKILLS
from .hashicorp import SKILLS as HASHICORP_SKILLS
from .microsoft import SKILLS as MICROSOFT_SKILLS
from .topics1 import SKILLS as TOPICS1_SKILLS
from .topics2 import SKILLS as TOPICS2_SKILLS
from .yandex import SKILLS as YANDEX_SKILLS

__all__ = ["SKILLS"]

def dis_julia() -> Disambiguate:
  def disambiguate(ent: Span) -> bool:
    for token in ent.sent:
      if token.lower_ in {"'m", "am", "name"}:
        return False
    return True
  return disambiguate

SKILLS: list[Skill] = [
  *ADOBE_SKILLS,
  *AMAZON_SKILLS,
  *APACHE_SKILLS,
  *APPLE_SKILLS,
  *CISCO_SKILLS,
  *COMPANIES_SKILLS,
  *GOOGLE_SKILLS,
  *HASHICORP_SKILLS,
  *MICROSOFT_SKILLS,
  *YANDEX_SKILLS,
  *TOPICS1_SKILLS,
  *TOPICS2_SKILLS,

  # ANALYSIS
  Skill("Tableau", ["tableau"], ""),

  # CLOUD
  Skill("Cloudflare", ["cloudflare"], ""),
  Skill("Heroku", ["heroku"], ""),
  Skill("Netlify", ["netlify"], ""),

  # TOOLS (should mostly be discouraged in UI)
  Skill("Confluence", ["confluence"], ""), # FP, exclude "confluence of" pattern
  Skill("GitHub", ["github"], ""),
  Skill("GitLab", ["gitlab"], ""),
  Skill("Jira", ["jira"], ""),
  Skill("Postman", ["postman"], ""),
  Skill("Swagger", ["swagger"], ""),

  # MOBILE & CROSS-PLATFORM
  # notification, ui, gui, interface, native, web
  # Bluetooth, TCP, USB
  Skill("Android", ["android"], ""),
  Skill("CMake", ["cmake"], ""),
  Skill("Cocoa", ["cocoa"], ""),
  Skill("Cordova", ["cordova", "phonegap"], ""),
  Skill("Dagger2", ["dagger=2"], "Programmable CI/CD engine that runs pipelines in containers"),
  Skill("GTK", ["gtk", "gtk+"], ""),
  Skill("Ionic", ["ionic"], ""),
  Skill("Capacitor", ["capacitor"], ""),
  Skill("Jetpack-Compose", ["jetpack=compose", "jetpack=navigation", "android=compose"], ""), # just Jetpack is ambiguous

  Skill("Lottie", ["lottie"], ""),
  Skill("Onsen UI", ["onsen", "onsen=ui"], ""),
  Skill("Native-Script", ["native=script"], ""),
  Skill("Novu", ["novu"], ""), # open-source notification platform, framework, CMS https://github.com/novuhq/novu
  Skill("QML", ["qml"], ""), # Qt modeling language
  Skill("Qt", ["pyqt", "pyside", "qtruby", "qtjambi", "php=qt", ver1("qt")], ""),
  Skill("React-Native", ["react=native"], ""),
  Skill("Retrofit", ["retrofit"], ""),
  Skill("SDL", ["sdl"], ""),
  Skill("SFML", ["sfml"], ""),
  Skill("Xcode", ["xcode"], ""),
  # Titanium -- disambiguate
  Skill("VoIP", ["voip"], ""), # voice over IP
  Skill("Vue-Native", ["vue=native"], ""),
  Skill("WebRTC", ["webrtc"], ""), # web real-time communication

  # DATABASE, DWH
  Skill("CouchBase", ["couchbase"], ""),
  Skill("CouchDB", ["couch=db"], ""),
  Skill("DynamoDB", ["dynamo=db"], ""),
  Skill("Elasticsearch", ["elastic=search"], ""),
  Skill("Greenplum", ["greenplum"], ""),
  Skill("MariaDB", ["maria=db"], ""),
  Skill("Memcached", ["memcache(d)"], ""),
  Skill("MongoDB", ["mongo=db", ver1("mongo")], ""),
  Skill("MySQL", ["my-sql", "my sql", ver1("mysql"), "(my=)sql=manager"], ""),
  Skill("Neo4j", ["neo4j", "neo4j=db"], ""),
  Skill("Opensearch", ["opensearch"], "Community-driven Elasticsearch fork"),
  Skill("Oracle", ["oracle=db", "oracle", "pl(/)sql"], ""), # Oracle Database or Oracle RDBMS TODO split DB and COMPANY
  Skill("PouchDB", ["pouch=db"], ""),
  Skill("Presto", ["presto"], ""),
  Skill("PostgreSQL", [
    "postgre=sql", "postgres=sql", ver1("postgres"),
    "pgadmin",
    "psql", "pgsql"
  ], ""),
  Skill("Redis", ["redis"], ""),
  Skill("ScyllaDB", ["scylladb"], ""),
  Skill("Supabase", ["supabase"], ""),
  Skill("SQLite", [ver1("sqlite")], ""),
  Skill("Trino", ["trino"], ""), # also ANALYTICS (https://trino.io/ Fast distributed SQL query engine for big data analytics)

  # ORM
  Skill("Django-ORM", ["django=orm"], ""),
  Skill("Drizzle", ["drizzle=orm", "drizzle"], ""),
  Skill("Hibernate", ["hibernate"], ""),
  Skill("Prisma", ["prisma=orm", "prisma"], ""), # Popular word, some FPs
  Skill("Sequelize", ["sequelize"], ""),
  Skill("SQLAlchemy", ["sql=alchemy"], ""),
  Skill("TypeORM", ["type=orm"], ""),

  # DATA SCIENCE
  Skill("Anaconda", ["anaconda", "miniconda", "conda"], ""),
  Skill("Beautiful-Soup", ["beautiful=soup"], ""),
  Skill("IPython", ["ipython"], ""), # interactive shell
  Skill("Jupyter", ["jupyter=lab", "jupyter-notebook(s)", "jupyter"], ""),
  Skill("Matplotlib", ["matplotlib"], ""),
  Skill("NLTK", ["nltk"], ""),
  Skill("Numba", [[{LOWER: "numba"}, {OP: "!", LOWER: {IN: ["1", "one", "wan"]}}]], ""),
  Skill("NumPy", ["numpy"], ""),
  Skill("Pandas", ["pandas"], ""),
  Skill("PyTorch", ["pytorch"], ""),
  Skill("Keras", ["keras"], ""),
  Skill("RAPIDS", [propn("rapids")], ""), # also GAMEDEV (`https://rapids.ai/`)
  Skill("Scikit-Learn", ["scikit=learn", "sklearn"], ""),
  Skill("SciPy", ["scipy"], ""),
  Skill("Seaborn", ["seaborn"], ""),
  Skill("ShowFlake", ["snowflake"], ""), # ~ MS Databricks, ~ AWS Redshift
  Skill("Spacy", ["spacy"], ""),
  Skill("Stan", ["stan"], "", disambiguate=contextual("R", "Python")),
  Skill("Stata", ["stata"], ""),
  Skill("TensorRT", ["tensorrt"], ""), # NVidia

  # GAME
  Skill("BabylonJS", ["babylon.=js"], "Game and rendering engine packed into a JavaScript framework"),
  Skill("CUDA", ["cuda"], ""), # also ROBOTICS, EMBEDDED (GPU computing, NVIDIA)
  Skill("Godot", ["godot=engine", "godot", "gd=script"], ""),
  Skill("Phaser", ["phaser.=js", "phaser"], ""),
  Skill("PixiJS", ["pixi.=js", "pixi"], ""),
  Skill("PlayStation", ["playstation", "ps4", "ps5"], ""),
  Skill("PyGame", ["pygame"], ""),
  Skill("Roblox", ["roblox"], ""),
  Skill("Solar2D", ["solar2d"], ""),
  Skill("Unreal-Engine", ["unreal=engine", "unreal=script", "unreal", "ue-4", "ue-5", "ue4", "ue5"], ""),
  Skill("ThreeJS", ["three.=js"], ""),

  Skill("OpenGL", ["opengl"], ""),

  # WEB BACKEND
  Skill("Bun", ["bun"], ""),
  Skill("CakePHP", ["cake=php"], ""),
  Skill("CherryPy", ["cherry=py"], ""),
  Skill("CodeIgniter", ["code=igniter"], ""),
  Skill("Deno", ["deno"], ""),
  Skill("Django", ["django", "drf"], ""), # django-rest-framework
  Skill("Express", ["express.=js", "express"], ""),
  Skill("FastAPI", ["fast=api"], ""),
  Skill("Fastify", ["fastify"], ""),
  Skill("Flask", ["flask"], ""),
  Skill("Jakarta-EE", ["jakarta(=ee)", "java-ee", "j2ee", "java-platform"], ""),
  Skill("JVM", ["jvm"], "Java Virtual Machine enables a computer to run Java (Kotlin, etc.) programs"),
  Skill("Hasura", ["hasura"], ""),
  Skill("Koa", ["koa"], ""),
  Skill("Laravel", ["laravel"], ""),
  Skill("NestJS", ["nest.=js", propn("nest")], ""),
  Skill("Nginx", ["nginx"], ""),
  Skill("Phoenix", ["phoenix"], ""),
  Skill("Ruby-on-Rails", ["ruby-on-rails", "rails", "ror"], ""),
  Skill("SailsJS", ["sails.=js"], ""),
  Skill("SMTP", ["smtp"], ""),
  Skill("Spring", [
    ver1("spring"), "spring-framework", "spring-boot", "spring-cloud",
    "spring-mvc", "spring-security", "spring-webflux"
  ], ""),
  Skill("Symfony", [ver1("symfony")], ""),
  Skill("Yii", [ver1("yii")], ""),

# #   Key Components of J2EE:
# #
# # Java Servlets: Server-side Java programs that handle requests and responses, enabling dynamic web content generation.
# # JavaServer Pages (JSP): A technology that allows for the creation of dynamic web pages using HTML and Java code.
# # Enterprise JavaBeans (EJB): A server-side component architecture that allows for the development of scalable, transactional, and multi-user applications.
# # Java Message Service (JMS): A messaging standard that allows applications to communicate asynchronously.
# # Java Naming and Directory Interface (JNDI): An API that provides naming and directory functionality to applications, allowing them to look up resources like databases and EJBs.
# # Java Transaction API (JTA): A specification that allows for the management of transactions across multiple resources.

  Skill("Micronaut", ["micronaut"], ""),
  Skill("RabbitMQ", ["rabbit=mq", "rmq"], ""),
  Skill("Vert-X", ["vert.=x"], ""),

  # WEB FRONTEND
  Skill("Angular", ["angular.=js", "angular"], "Web framework for SPA, mobile, PWA development with focus on modularity"),
  Skill("Astro", ["astro.=js", "astro"], "Web framework for content-driven websites, server-first"),
  Skill("Bootstrap", ["bootstrap"], ""),
  Skill("Chakra-UI", ["chakra=ui", "chakra"], ""),
  Skill("D3JS", ["d3.=js", "d3"], ""),
  Skill("EmberJS", ["ember.=js", "ember"], ""),
  Skill("Figma", ["figma"], ""),
  Skill("Framer", ["framer"], ""),
  Skill("jQuery", ["jquery"], ""),
  Skill("Lit", [propn("lit")], ""),
  Skill("Material-UI", ["material=ui", "mui", propn("material")], ""),
  Skill("Materialize", ["materialize"], ""),
  Skill("NgRx", ["ngrx"], "Reactive state management for Angular apps inspired by Redux"),
  Skill("Pinia", ["pinia"], ""),
  Skill("React", ["react.=js", "react"], ""),
  Skill("Redux", ["redux.=js", "redux"], ""),
  Skill("Remix", ["remix.=js", "remix"], ""),
  Skill("RiotJS", ["riot.=js"], ""),
  Skill("SolidJS", ["solid.=js", propn("solid")], ""),
  Skill("Svelte", ["svelte.=js", "svelte"], ""),
  Skill("Tailwind-CSS", ["tailwind.=css", "tailwind"], ""),
  Skill("VueJS", ["vue.=js", ver1("vue")], ""),
  Skill("VueX", ["vuex"], "State management pattern + library for VueJS applications"),

  # WEB FULLSTACK
  Skill("Gulp", ["gulp"], ""),
  Skill("Vaadin", ["vaadin"], ""),
  Skill("Vite", ["vite"], ""),
  Skill("Webpack", ["webpack"], ""),

  Skill("JAM-Stack", ["jam=stack"], resolve=["JavaScript", "API", "Markup"]),
  Skill("MEAN-Stack", ["mean=stack", propn("mean")], resolve=["MongoDB", "Express", "Angular", "NodeJS"]),
  Skill("MERN-Stack", ["mern=stack", "mern"], resolve=["MongoDB", "Express", "React", "NodeJS"]),
  Skill("MEVN-Stack", ["mevn=stack", "mevn"], resolve=["MongoDB", "Express", "VueJS", "NodeJS"]),
  Skill("PERN-Stack", ["pern=stack", "pern"], resolve=["PostgreSQL", "Express", "React", "NodeJS"]),
  Skill("LAMP-Stack", ["lamp=stack", propn("LAMP")], resolve=["Linux", "MySQL", "PHP"]), # Apache

#   Skill("Chrome", ["chrome"], ""),
#   Skill("Firefox", ["firefox"], ""),
#   Skill("Safari", ["safari"], ""),
#   Skill("WebKit", ["webkit"], ""), # browser engine

  Skill("Apollo", ["apollo.=js", "apollo=client", "apollo=server", "apollo"], "GraphQL-centric fullstack tools for web and mobile"),
  Skill("HTMX", ["htmx"], ""),
  Skill("Meteor", ["meteor", "meteor.=js"], ""),
  Skill("Ktor", ["ktor"], ""), # fullstack framework in Kotlin
  Skill("NextJS", ["next.=js", propn("next")], ""),
  Skill("NextJS", ["next"], disambiguate=neighbour(1)), # /
  Skill("NuxtJS", ["nuxt.=js", propn("nuxt")], ""),
  Skill("NodeJS", ["node.=js", propn("node")], ""),
  Skill("SvelteKit", ["svelte=kit"], ""),

  # LOW-CODE
  Skill("1C", ["1c"], ""), # ??
  Skill("Bitrix", [
    "bitrix",
    "1c=bitrix", "bitrix=1c", "1с-битрикс", "битрикс-1с",
    "bitrix=24", "битрикс=24",
  ], ""), # so rare it makes sense to merge them...
  Skill("Airtable", ["airtable"], ""),
  Skill("Drupal", ["drupal"], ""),
  Skill("Gatsby", ["gatsby"], ""),
  Skill("Hygraph", ["hygraph", "graph=cms"], ""),
  Skill("Jekyll", ["jekyll"], ""),
  Skill("Joomla", ["joomla"], ""),
  Skill("MODx", ["modx"], ""),
  Skill("Shopify", ["shopify"], ""),
  Skill("Strapi", ["strapi"], ""),
  Skill("WebFlow", ["webflow"], ""),
  Skill("Wix", ["wix"], ""),
  Skill("WooCommerce", ["woo=commerce"], ""),
  Skill("WordPress", ["wordpress"], ""),

  # OPERATIONS
  Skill("Celery", ["celery"], ""),
  Skill("ELK-Stack", ["elk=stack", "elk"], resolve=["Elasticsearch", "Logstash", "Kibana"]), # , "Beats"
  Skill("Ansible", ["ansible"], "Automation engine for configuration management, application deployment, and task automation"),
  # Skill("Dagger", ["dagger"], "Programmable CI/CD engine that runs pipelines in containers"),
  Skill("CircleCI", ["circleci"], ""),
  Skill("CKA", ["cka"], ""), # certificate
  Skill("CKAD", ["ckad"], ""), # certificate
  Skill("CompTIA-ITOps", ["cios"], ""), # certificate
  Skill("MCSA", ["mcsa"], ""), # certificate
  Skill("Docker", ["docker", "dockerfile"], ""),
  Skill("Docker-Compose", ["docker=compose"], ""),
  Skill("Docker-Swarm", ["docker=swarm"], ""),
  Skill("Dokku", ["dokku"], ""), # also Cloud
  Skill("GitHub-Actions", ["github=actions"], ""),
  Skill("GitLab-CI", ["gitlab=ci"], ""),
  Skill("Grafana", ["grafana"], "Monitoring"),
  Skill("Helm", ["helm"], ""),
  Skill("Jaeger", ["jaeger"], "Distributed tracing platform, CNCF"),
  Skill("Jenkins", ["jenkins"], ""),
  Skill("Kibana", ["kibana"], ""),
  Skill("Kubernetes", ["kubernetes", "k8s", "k3s"], ""),
  Skill("Logstash", ["logstash"], ""),
  Skill("OpenShift", ["openshift"], "Cloud platform, a set of tools and services for application lifecycle"),
  Skill("Prometheus", ["prometheus"], ""),
  Skill("Pulumi", ["pulumi"], ""),
  Skill("Puppet", ["puppet"], ""),
  Skill("Quarkus", ["quarkus"], ""),
  Skill("Spinnaker", ["spinnaker"], ""),
  Skill("Splunk", ["splunk"], ""), # also SECURITY
  Skill("RHCE", ["rhce"], ""),   # certificate
  Skill("RHCSA", ["rhcsa"], ""), # certificate
  Skill("TeamCity", ["teamcity"], ""),
  Skill("Vagrant", ["vagrant"], ""),
  # Good to have Knowledge of modern monitoring solutions (e.g. Nagios, Zabbix, Prometheus, Splunk).
  # Familiarity with monitoring tools such as SolarWinds, Nagios, or similar.

  # QA-n-AUTOMATION (tech & platforms)
  Skill("Appium", ["appium"], ""),
  Skill("Codeception", ["codeception"], ""),
  Skill("Cucumber", ["cucumber"], ""),
  Skill("Cypress", ["cypress", "cypress.=js"], ""),
  Skill("Jasmine", ["jasmine"], "", disambiguate=contextual_or_neighbour(["Jest", "Karma", "QA"], 2)),
  Skill("Jest", ["jest"], ""),
  Skill("JUnit", ["junit"], ""),
  Skill("Karma", ["karma"], "", disambiguate=contextual_or_neighbour(["Jasmine", "Jest", "QA"], 2)),
  Skill("PHPUnit", ["php=unit"], ""),
  Skill("Playwright", ["playwright"], ""),
  Skill("Protractor", ["protractor"], ""),
  Skill("PyTest", ["pytest"], ""),
  Skill("Selenium", ["selenium"], ""),
  Skill("Sentry", ["sentry"], "Monitoring"),
  Skill("TestCafe", ["testcafe"], ""),
  Skill("TestNg", ["testng"], ""),
  Skill("WebdriverIO", ["webdriverio"], ""),

  # BLOCKCHAIN
  Skill("Arweave", ["arweave"], "A permanent and decentralized web inside an open ledger"),
  Skill("Bitcoin", ["bitcoin"], ""),
  Skill("Ethereum", ["ethereum"], ""),
  Skill("EthersJS", ["eithers.=js"], ""),
  Skill("EVM", ["evm"], "Ethereum Virtual Machine"),
  Skill("Solana", ["solana"], ""),
  Skill("Web3JS", ["web3.=js"], ""),
  # Skill("SVM", ["svm"], ""), TODO disambiguate Support-Vector-Machine vs Solana-Virtual-Machine

  # MEDIA
  Skill("FFmpeg", ["ffmpeg"], "Cross-platform solution to record, convert and stream audio and video"),

  # NETWORKS
  Skill("CompTIA-Network+", ["network+", "comptia n(etwork)+"], ""), # certificate
  Skill("F5-Networks", ["f5-networks", "f5"], ""), # Company
  Skill("LoRa", [propn("LoRa")], ""), # transmission tech
  Skill("MTCNA", ["mtcna"], ""),    # certificate
  Skill("MQTT", ["mqtt"], ""),      # IoT messaging standard, also CLOUD
  Skill("Netconf", ["netconf"], "Protocol"),
  Skill("Nmap", ["nmap"], ""),             # also SECURITY
  Skill("Netcat", ["netcat", "ncat"], ""), # also SECURITY
  Skill("Proxyman", ["proxyman"], ""),   # also SECURITY
  Skill("Wireshark", ["wireshark"], ""),   # also SECURITY
  Skill("YANG", [literal("YANG")], "Data modeling language"),
  Skill("Zigbee", ["zigbee"], ""), # protocol spec. also EMBEDDED

  # SECURITY
  Skill("Burp-Suite", ["burp=suite"], "Proprietary vulnerability scanning, penetration testing, and webapp security platform"),
  Skill("CEH", ["ceh"], ""),     # certificate
  Skill("CISA", ["cisa"], ""),   # certificate
  Skill("CISM", ["cism"], ""),   # certificate
  Skill("CISSP", ["ciss", "cissp"], "Certified Information Systems Security Professional"), # certificate
  Skill("CSSLP", ["csslp"], "Certified Secure Software Lifecycle Professional"), # certificate
  Skill("CASE", [literal("CASE")], "Certified Application Security Engineer"), # certificate
  Skill("CompTIA-PenTest+", ["pentest+", "comptia-p(entest)+"], ""), # certificate
  Skill("CompTIA-Security+", ["security+", "comptia-s(ecurity)+"], ""), # certificate
  Skill("GIAC-CIH", ["gcih"], ""),     # certificate
  Skill("GIAC-SEC", ["gsec"], ""),     # certificate
  Skill("GIAC-REM", ["grem"], ""),     # certificate
  Skill("GIAC-WAPT", ["gwapt"], ""),   # certificate
  Skill("OSCP/OSCE", ["oscp", "osce"], ""), # certificate
  Skill("Cobalt-Strike", ["cobalt=strike"], ""),
  Skill("JWT", ["jwt"], ""),
  Skill("Metasploit", ["metasploit"], ""),
  Skill("Nessus", ["nessus"], ""),
  Skill("OAuth", [ver1("oauth")], ""),
  Skill("OpenID", ["openid"], ""),
  Skill("SAML", ["saml"], ""),
  Skill("Snort", [propn("snort")], ""),
  Skill("SSCP", ["sscp"], ""), # certificate
  # CANVAS, Empire, Core Impact -- attack frameworks
  # Relevant certifications (kept only new: CISSP-ISSAP, CCSP, SC-100, CRTSA, GDSA, TOGAF) are highly desirable.

  # SANS (GPEN, GXPN, GWAPT) -- wtf: SANS vs GIAC

  # ROBOTICS
  # Skill("ABB", ["abb"], ""),           # robot brand
  Skill("Fanuc", ["fanuc"], ""),       # robot brand
  Skill("iCub", ["icub"], ""),         # robot brand
  Skill("HyQ", ["hyq"], ""),           # robot brand
  Skill("KUKA", ["kuka"], ""),         # robot brand
  Skill("OpenCV", ["opencv"], ""),     # open source Computer Vision library
  # Skill("Omron", ["omron"], ""),       # electronics corporation
  Skill("FreeRTOS", ["freertos"], ""), # OS, also EMBEDDED-n-SYSTEM
  Skill("ROS", ["ros"], ""),           # OS, also EMBEDDED-n-SYSTEM
  # Skill("SLAM", ["slam", "vslam"], ""), # simultaneous localization and mapping
  # Skill("Yaskawa", ["yaskawa"], ""), # electric and robotics corporation

  Skill("Simulink", ["simulink"], ""), # some lang.

  # SYSTEM
  Skill("FreeBSD", ["freebsd"], ""), # also CROSS-PLATFORM
  Skill("Linux", [
    "linux", "debian", "ubuntu",
  ], ""), # also CROSS-PLATFORM
  Skill("MacOS", ["macos", "osx"], ""), # also CROSS-PLATFORM
  Skill("Unix", ["unix", "*nix"], ""),   # also CROSS-PLATFORM
  Skill("Windows", ["windows", "win32", "win64"], ""), # also CROSS-PLATFORM

  Skill("Clang", ["clang"], ""),
  Skill("MicroPython", ["micropython"], ""), # compiler
  Skill("GCC", ["gcc"], ""), # compiler
  Skill("Kernel", ["kernel"], ""),
  Skill("LLVM", ["llvm"], ""),

  # HARDWARE & EMBEDDED
  # Skill("HPC", ["hpc"], "High performance computing"),
  Skill("Arduino", ["arduino"], "Controller brand"),
  Skill("ASIC", ["asic"], ""), # ASICs are custom-designed circuits for specific applications, offering high performance and efficiency
  Skill("ARC", [propn("ARC")], "CPU family"),
  Skill("ARC", ["arc"], disambiguate=neighbour(2)),
  Skill("AutoCAD", ["autocad"], ""),
  Skill("AVR", ["avr"], "Controller family"),
  Skill("Elbrus-2000", ["elbrus=2000", "e2k"], "CPU"),
  Skill("Embox", ["embox"], ""), # Embox is a configurable RTOS designed for resource constrained and embedded systems
  Skill("ESP32", ["esp=32"], ""), # controller family
  Skill("ESP8266", ["esp=8266"], ""), # controller family
  Skill("FPGA", ["fpga"], ""), # FPGAs are reprogrammable devices that provide flexibility and rapid prototyping capabilities
  Skill("i.MX6", ["i.mx=6"], ""), # platform
  Skill("LabVIEW", ["labview"], ""),
  Skill("KiCad", ["kicad=eda", "kicad"], ""),
  Skill("MicroBlaze", ["microblaze"], ""), # soft core
  Skill("MIPS", ["mips"], ""), # CPU architecture
  Skill("MSP430", ["msp=430"], ""), # controller family
  Skill("PowerPC", ["powerpc"], ""), # CPU architecture
  Skill("Raspberry-Pi", ["raspberry", "rasp=pi", "raspberry=pi(s)", "rpi"], ""), # platform
  Skill("RISC", ["risc", "risc-v"], ""), # CPU architecture
  Skill("SPARC", ["sparc"], ""), # platform
  Skill("Altium-Designer", ["altium=designer"], ""), # tool
  Skill("Altium-365", ["altium=365"], ""), # tool
  Skill("Autodesk-Fusion", ["autodesk-fusion", "fusion=360"], ""), # tool
  Skill("Autodesk-Eagle", ["autodesk-eagle"], ""), # tool
  Skill("Autodesk-Eagle", ["eagle"], disambiguate=contextual("Autodesk", "AutoCAD")), # /
  Skill("Touchdesigner", ["touchdesigner"], "Visual development platform"), #
  Skill("Solidworks", ["solidworks-pcb", "solidworks"], "CB design tool"),
  Skill("STM32", ["stm=32"], ""), # platform
  Skill("Verilog", ["verilog", "sysverilog", "systemverilog"], "Specialized PL"),
  Skill("VHDL", ["vhdl"], "Specialized PL"),
  Skill("VLIW", ["vliw"], "CPU architecture"),
  Skill("x32", ["x32"], "CPU architecture"),
  Skill("x64", ["x64"], "CPU architecture"),
  Skill("x86", ["x86", "x86-32", "x86-64", "i286", "i386"], "Intel CPU architecture"),
  Skill("Yosys", ["yosys"], ""), # https://github.com/YosysHQ/yosys
  Skill("Z80", ["z=80"], "CPU brand"),

  # DESKTOP
  Skill("ElectronJS", ["electron=js"], ""), # tons of FPs for just "electron"

  # MAIN LANGUAGES
  Skill("Ada", ["ada"], ""),
  Skill("Apex", ["apex"], ""),
  Skill("C", ["c-lang"], ""),
  Skill("C", ["c"], disambiguate=singleletter()),
  Skill("C++", ["c++", "cpp", "c=plus=plus"], ""),
  Skill("C#", ["c#", "csharp"], ""),
  Skill("Cairo", ["cairo"], ""),
  Skill("Clojure", ["clojure", "clojurian"], ""),
  Skill("ClojureScript", ["clojure=script"], ""),
  Skill("Cobol", ["cobol"], ""),
  Skill("Crystal", ["crystal-lang", "crystal"], ""),
  Skill("CSS", [ver1("css")], ""),
  Skill("CSV", ["csv"], ""),
  Skill("D", ["d=lang"], ""),
  Skill("D", ["d"], disambiguate=singleletter()),
  Skill("Dart", ["dart"], ""),
  Skill("Delphi", ["delphi"], ""),
  Skill("Elixir", ["elixir"], ""),
  Skill("Elm", ["elm"], ""),
  Skill("Erlang", ["erlang"], ""),
  Skill("Fortran", ["fortran"], ""),
  Skill("F#", ["f#", "f=lang", "fsharp"], ""),
  Skill("GQL", ["gql"], ""), # TODO Cypher
  Skill("Gleam", ["gleam"], ""),
  Skill("Go", ["golang", "gopher", propn("go")], ""),
  Skill("Groovy", ["groovy"], ""),
  Skill("Haskell", ["haskell"], ""),
  Skill("HTML", [ver1("html")], ""),
  Skill("Java", [ver1("java"), "java-se"], ""),
  Skill("JavaScript", ["java=script", "js"], ""),
  Skill("JSON", ["json", "json5"], ""),
  Skill("Julia", ["julia"], "", disambiguate=dis_julia()),
  Skill("Kotlin", ["kotlin"], ""),
  Skill("LESS", [literal("LESS")], ""),
  Skill("Lisp", ["lisp"], ""),
  Skill("Lua", ["lua"], ""),
  Skill("Nim", ["nim"], ""),
  Skill("Makefile", ["makefile"], ""),
  Skill("Markdown", ["markdown", "md"], ""),
  Skill("Matlab", ["matlab"], ""),
  Skill("Mojo", ["mojo"], ""),
  Skill("Ocaml", ["ocaml"], ""),
  Skill("Odin", ["odin"], ""),
  Skill("-Odin", ["odin-project"], resolve=[]),
  Skill("Perl", [ver1("perl")], ""),
  Skill("PHP", [ver1("php"), "phper"], ""),
  Skill("PowerShell", ["power=shell"], ""),
  Skill("Prolog", ["prolog"], ""),
  Skill("Python", [ver1("python"), "py", "pythonist(a)"], ""),
  Skill("R", ["r=lang"], "Programming language for statistical computing and data visualization"),
  Skill("R", ["r"], disambiguate=singleletter()),
  Skill("Ruby", ["ruby=lang", "ruby", "rubyist", "rubist"], ""),
  Skill("Rust", ["rust", "rustacean"], ""),
  Skill("SASS", ["sass", "scss"], ""),
  Skill("Scala", ["scala"], ""),
  Skill("Solidity", ["solidity"], ""),
  Skill("TypeScript", ["type=script", "ts"], ""),
  Skill("Shell", ["shell", "bash", "zsh"], ""),
  Skill("XML", ["xml"], ""),
  Skill("YAML", ["yaml"], ""),
  Skill("V", ["vlang"], ""),
  Skill("V", ["v"], disambiguate=singleletter()),
  Skill("Vala", ["vala"], ""),
  Skill("Vyper", ["vyper"], ""),
  Skill("Visual-Basic", ["visual=basic", "vb(a)", "vb.net"], ""),
  Skill("WebAssembly", ["wasm", "web=assembly"], ""),
  Skill("Zig", ["zig"], ""),

  # LANGUAGE UMBRELLAS
  Skill("Assembly", ["assembly"], "PL category"),
  Skill("GraphQL", ["graphql", "graphiql"], "QL"),
  Skill("SQL", ["sql"], "QL/DB category"),
  Skill("NoSQL", ["nosql"], "DB category"),

  # UNSORTED
  Skill("Blender", ["blender"], ""),
  Skill("CompTIA-A+", ["comptia a+"], ""), # certificate for tech. support and IT ops
  Skill("RxJS", ["rxjs"], ""),
  Skill("Git", ["git"], ""),
  Skill("SVN", ["svn"], ""),
  Skill("gRPC", ["grpc"], "Skill"),
  Skill("tRPC", ["trpc"], "Skill"),
]

# // SECURITY TOOLS
# // Aircrack-ng: 454 repos, 5 users
# // Nikto: 352 repos -- too many false positives
# // John the Ripper: 210 repos, 7 ysers
#
# export const rawSkillTable: Dict<SkillRow> = {
#   "Chef": {pattern: "chef", category: "platform", role: "Engineer"},
#   // should we add new char like "css𝐕" or should we consume numbers after EACH term?
#   // Most skills have versions BUT topics don't @_@
#   // So it can be a per-table configuration
#   "Native Android": {pattern: "native=android", category: "platform", role: "Engineer"},
#   "Native iOS": {pattern: "native-ios", category: "platform", role: "Engineer"},
#   "Octave": {pattern: "octave", category: "lang"},
#   // "Polygon": {pattern: "polygon", category: "tech", role: "Engineer"},
#   "Prisma": {pattern: "prisma", category: "tech", role: "Engineer"},
#   "OpenAuth": {pattern: "open=auth2?, oauth2?", category: "tech"},
#   "RxJS": {pattern: "rx.=js, RX", category: "tech", role: "Engineer"},
#   "Salt": {pattern: "salt", category: "platform", role: "Engineer"},
#   "Web3.js": {pattern: "web3.js", category: "tech"},
#
#   // TOPICS ----------------------------------------------------------------------------------------
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
#   "Mathematics": {pattern: "mathematics, maths?", category: "topic"},
#   "CI/CD": {pattern: "ci/=cd", category: "topic"},
#   "Chemistry": {pattern: "chemistry", category: "topic"}, "chemist"
#   "Physics": {pattern: "physics", category: "topic"},
#   "Photography": {pattern: "photography", category: "topic"},
#   "2D": {pattern: "2d", category: "topic"},
#   "3D": {pattern: "3d", category: "topic"},
#   // "Font": {pattern: "fonts?", category: "topic"}, // disambiguate?
#   "Animation": {pattern: "animation, motion", category: "topic"},
#   "Graphic": {pattern: "graphics?", category: "topic", role: "Designer"},
#   "Enterprise": {pattern: "enterprise", category: "topic"},
#
#   // Role-agnostic (multi-role) topics
#   "Manual": {pattern: "manual", category: "topic"},
#   "R&D": {pattern: "r ?& ?d", category: "topic"},
#   "Sales": {pattern: "sales", category: "topic"}, // another problematic word @_@
#   "Typography": {pattern: "typography", category: "topic"},
#   "Startup": {pattern: "startups?", category: "topic"},
#   "Team": {pattern: "!Teams?", category: "topic"},
#   "Functional Programming": {pattern: "functional-programming, fp", category: "topic"},
#   "Crypto": {pattern: "crypto, defi, web=3", category: "topic"}, // crypto enthusiast = crypto-currencies + decentralized finance (DeFi)
#   // Crypto vs Blockchain?!?!
#   // should nopCommerce -> eCommerce? But then NodeJS -> js, are there INVALID precedents like that?
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
#
# OS specific words
#   stdin, stdout, terminal, filesystem, socket, stream, thread, process
#   cli, command line, shell, runtime, schedule
#
#   SECURITY specific words
#   ssh, tls, ssl
#   token, authentication, authorization, jwt, cookie
#   ddos, session
#
#   DEVOPS specific words
#   development, production, staging
#
#   ARCHITECT specific words
#   microservice, monolith, monorepo, Event-Driven, Vertical Slice
#   Distributed
#   large-scale
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
#   CQRS
#   ecommerce
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
# Experience with OP Stack and Arbitrum works is preferred
# Experience with service mesh technologies like Istio or Linkerd.
# + Room (persistence in SQLite library)
# + SAP MM, SAP PM, and SAP EWM
# Kubeflow, Vertex AI Pipelines, TFX
# Kubeflow, Step Functions, MLflow, TFX
# such as Scikit-learn, XGBoost, MXNet, TensorFlow or PyTorch
# exposition to GenAI and solid understanding of multimodal AI via HuggingFace, Llama, VertexAI, AWS Bedrock or GPT
# + Dask
# • Strong proficiency with CI/CD pipelines and distributed computing frameworks like Ray or Dask.
# • Familiarity with model monitoring, logging, and versioning tools (e.g., MLflow, Weights & Biases).
# • Proficient in designing and deploying agentic systems with modern model serving frameworks (e.g., LangChain, vLLM, FastAPI, or KServe).
# Facebook Instant Games SDK
# hypervisor, hyper-v, vmware (also a company)
# ITIL Service Operation frameworks.
