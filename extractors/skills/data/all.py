from ...utils import IN, LOWER, OP, propn, noun, ver1
from ..utils import Skill, contextual, neighbour
from .amazon import SKILLS as AMAZON_SKILLS
from .apache import SKILLS as APACHE_SKILLS
from .google import SKILLS as GOOGLE_SKILLS
from .microsoft import SKILLS as MICROSOFT_SKILLS

__all__ = ["SKILLS"]

SKILLS: list[Skill] = [
  *AMAZON_SKILLS,
  *APACHE_SKILLS,
  *GOOGLE_SKILLS,
  *MICROSOFT_SKILLS,

  # ANALYSIS
  Skill("Excel", [propn("excel")], ""),
  Skill("Power-BI", ["power=bi"], ""),
  Skill("Tableau", ["tableau"], ""),

  # CLOUD
  Skill("Cloudflare", ["cloudflare"], ""),
  Skill("Heroku", ["heroku"], ""),
  Skill("Netlify", ["netlify"], ""),

  # MOBILE & CROSS-PLATFORM
  # notification, ui, gui, interface, native, web
  # Bluetooth, TCP, USB
  Skill("Android", ["android"], ""),
  Skill("CMake", ["cmake"], ""),
  Skill("Cocoa", ["cocoa"], ""),
  Skill("Cordova", ["cordova", "phonegap"], ""),
  Skill("Dagger2", ["dagger2"], ""),
  Skill("Flutter", ["flutter"], ""),
  Skill("GTK", ["gtk", "gtk+"], ""),
  Skill("Ionic", ["ionic"], ""),
  Skill("Jetpack-Compose", ["jetpack=compose", "android=compose"], ""), # just Jetpack is ambiguous
  Skill("iOS", ["ios"], ""), # also SYSTEM
  Skill("iPadOS", ["ipados"], ""), # also SYSTEM
  Skill("tvOS", ["tvos"], ""), # also SYSTEM
  Skill("watchOS", ["watchos"], ""), # also SYSTEM
  Skill("iMac", ["imac"], ""),
  Skill("iPad", ["ipad"], ""),
  Skill("iPhone", ["iphone"], ""),
  Skill("iWatch", ["iwatch"], ""),
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

  Skill("AppKit", ["appkit"], ""), # framework
  Skill("SwiftUI", ["swiftui"], ""), # framework
  Skill("UIKit", ["uikit"], ""), # framework

  # BIGDATA
  Skill("ELK-Stack", ["elk=stack", "elk"], ""),
  Skill("Trino", ["trino"], ""), # also DATA-SCIENCE, ANALYTICS (https://trino.io/ Fast distributed SQL query engine for big data analytics)

  # DATABASE
  Skill("CouchBase", ["couchbase"], ""),
  Skill("CouchDB", ["couch=db"], ""),
  Skill("DynamoDB", ["dynamo=db"], ""),
  Skill("Elasticsearch", ["elastic=search"], ""),
  Skill("MariaDB", ["maria=db"], ""),
  Skill("Memcached", ["memcache(d)"], ""),
  Skill("MongoDB", ["mongo=db", "mongo"], ""),
  Skill("MySQL", ["my=sql"], ""),
  Skill("Neo4j", ["neo4j", "neo4j=db"], ""),
  Skill("Oracle", ["oracle=db", "oracle", "pl(/)sql"], ""), # Oracle Database or Oracle RDBMS TODO split DB and COMPANY
  Skill("PouchDB", ["pouch=db"], ""),
  Skill("PostgreSQL", ["postgre=sql", "postgres=sql", "postgres", "psql", "pgsql"], ""),
  Skill("Redis", ["redis"], ""),
  Skill("Supabase", ["supabase"], ""),
  Skill("SQLite", [ver1("sqlite")], ""),

  # DATA SCIENCE
  Skill("Anaconda", ["anaconda", "miniconda", "conda"], ""),
  Skill("Beautiful-Soup", ["beautiful=soup"], ""),
  Skill("Flax", ["flax"], ""), # NN for Jax
  Skill("IPython", ["ipython"], ""), # interactive shell
  Skill("JAX", [propn("JAX")], ""), # TensorFlow alternative
  Skill("JAX", ["jax"], "", disambiguate=neighbour(2)), # /
  Skill("Jupyter", ["jupyter=lab", "jupyter=notebook(s)", "jupyter"], ""),
  Skill("Matplotlib", ["matplotlib"], ""),
  Skill("Numba", [[{LOWER: "numba"}, {OP: "!", LOWER: {IN: ["1", "one", "wan"]}}]], ""),
  Skill("NumPy", ["numpy"], ""),
  Skill("Pandas", ["pandas"], ""),
  Skill("PyTorch", ["pytorch"], ""),
  Skill("Keras", ["keras"], ""),
  Skill("RAPIDS", [propn("rapids")], ""), # also BIGDATA, GAMEDEV (`https://rapids.ai/`)
  Skill("Scikit-Learn", ["scikit=learn", "sklearn"], ""),
  Skill("SciPy", ["scipy"], ""),
  Skill("Seaborn", ["seaborn"], ""),
  Skill("ShowFlake", ["snowflake"], ""), # ~ MS Databricks, ~ AWS Redshift
  Skill("Spacy", ["spacy"], ""),
  Skill("Stan", ["stan"], "", disambiguate=contextual("R", "Python")),
  Skill("TensorFlow", ["tensorflow"], ""),

  # GAME
  Skill("BabylonJS", ["babylon.=js"], "Game and rendering engine packed into a JavaScript framework."),
  Skill("CUDA", ["cuda"], ""), # also ROBOTICS, EMBEDDED, BIGDATA (GPU computing, NVIDIA)
  Skill("Godot", ["godot=engine", "godot", "gd=script"], ""),
  Skill("Phaser", ["phaser.=js", "phaser"], ""),
  Skill("PixiJS", ["pixi.=js", "pixi"], ""),
  Skill("PlayStation", ["playstation", "ps4", "ps5"], ""),
  Skill("PyGame", ["pygame"], ""),
  Skill("Roblox", ["roblox"], ""),
  Skill("Solar2D", ["solar2d"], ""),
  Skill("Unreal-Engine", ["unreal=engine", "unreal", "ue-4", "ue-5", "ue4", "ue5"], ""),
  Skill("ThreeJS", ["three.=js"], ""),

  Skill("OpenGL", ["opengl"], ""),

  # WEB BACKEND
  Skill("Bun", ["bun"], ""),
  Skill("CakePHP", ["cake=php"], ""),
  Skill("CherryPy", ["cherry=py"], ""),
  Skill("CodeIgniter", ["code=igniter"], ""),
  Skill("Deno", ["deno"], ""),
  Skill("Django", ["django"], ""),
  Skill("Express", ["express.=js", "express"], ""),
  Skill("FastAPI", ["fast=api"], ""),
  Skill("Fastify", ["fastify"], ""),
  Skill("Flask", ["flask"], ""),
  Skill("Hasura", ["hasura"], ""),
  Skill("Koa", ["koa"], ""),
  Skill("Laravel", ["laravel"], ""),
  Skill("NestJS", ["nest.=js", propn("nest")], ""),
  Skill("Nginx", ["nginx"], ""),
  Skill("Phoenix", ["phoenix"], ""),
  Skill("Ruby-on-Rails", ["ruby=on=rails", "rails", "ror"], ""),
  Skill("SailsJS", ["sails.=js"], ""),
  Skill("SMTP", ["smtp"], ""),
  Skill("Spring", ["spring"], ""),
  Skill("Symfony", ["symfony"], ""),
  Skill("Yii", ["yii"], ""),

  # WEB FRONTEND
  Skill("Angular", ["angular.=js", "angular"], "Web framework for SPA, mobile, PWA development with focus on modularity."),
  Skill("Astro", ["astro.=js", "astro"], "Web framework for content-driven websites. Server-first."),
  Skill("Bootstrap", ["bootstrap"], ""),
  Skill("Chakra-UI", ["chakra=ui", "chakra"], ""),
  Skill("Chrome", ["chrome"], ""),
  Skill("D3JS", ["d3.=js", "d3"], ""),
  Skill("EmberJS", ["ember.=js", "ember"], ""),
  Skill("Figma", ["figma"], ""),
  Skill("Firefox", ["firefox"], ""),
  Skill("jQuery", ["jquery"], ""),
  Skill("Material-UI", ["material=ui", "mui", propn("material")], ""),
  Skill("Materialize", ["materialize"], ""),
  Skill("Photoshop", ["photoshop"], ""),
  Skill("React", ["react.=js", "react"], ""),
  Skill("Safari", ["safari"], ""),
  Skill("SolidJS", ["solid.=js", propn("solid")], ""),
  Skill("Svelte", ["svelte.=js", "svelte"], ""),
  Skill("Tailwind-CSS", ["tailwind.=css", "tailwind"], ""),
  Skill("Vite", ["vite"], ""),
  Skill("VueJS", ["vue.=js", "vue"], ""),
  Skill("Webpack", ["webpack"], ""),
  Skill("WebKit", ["webkit"], ""), # browser engine
  # TODO edge, ambiguous

  # WEB FULLSTACK
  Skill("MEAN-Stack", ["mean=stack", propn("mean")], "", stack=["MongoDB", "Express", "Angular", "NodeJS"]),
  Skill("MERN-Stack", ["mern=stack", "mern"], "", stack=["MongoDB", "Express", "React", "NodeJS"]),
  Skill("MEVN-Stack", ["mevn=stack", "mevn"], "", stack=["MongoDB", "Express", "VueJS", "NodeJS"]),
  Skill("PERN-Stack", ["pern=stack", "pern"], "", stack=["PostgreSQL", "Express", "React", "NodeJS"]),

  Skill("Apollo", ["apollo.=js", "apollo=client", "apollo=server", "apollo"], "GraphQL-centric fullstack tools for web and mobile."),
  Skill("GraphQL", ["graphql"], ""),
  Skill("HTMX", ["htmx"], ""),
  Skill("Meteor", ["meteor", "meteor.=js"], ""),
  Skill("Ktor", ["ktor"], ""), # fullstack framework in Kotlin
  Skill("NextJS", ["next.=js", propn("next")], ""),
  Skill("NextJS", ["next"], "", disambiguate=neighbour(1)), # /
  Skill("NuxtJS", ["nuxt.=js", propn("nuxt")], ""),
  Skill("NodeJS", ["node.=js", propn("node")], ""),
  Skill("OpenAPI", ["openapi"], ""),
  Skill("REST", ["rest=api", propn("rest"), noun("REST")], ""),
  Skill("REST", ["rest"], "", disambiguate=neighbour(2)),
  Skill("RPC", ["rpc=api", "rpc"], ""),
  Skill("tRPC", ["trpc"], ""),
  Skill("SvelteKit", ["svelte=kit"], ""),
  Skill("Swagger", ["swagger"], ""),

  # LOW-CODE
  Skill("Airtable", ["airtable"], ""),
  Skill("Bitrix", ["bitrix", "bitrix24"], ""),
  Skill("Drupal", ["drupal"], ""),
  Skill("Hygraph", ["hygraph", "graph=cms"], ""),
  Skill("Joomla", ["joomla"], ""),
  Skill("Magento", ["magento"], ""),
  Skill("MODx", ["modx"], ""),
  Skill("Power-Apps", ["power=apps"], ""),
  Skill("Power-Automate", ["power=automate"], ""),
  Skill("Power-Platform", ["power=platform"], ""),
  Skill("Shopify", ["shopify"], ""),
  Skill("Strapi", ["strapi"], ""),
  Skill("WooCommerce", ["woo=commerce"], ""),
  Skill("WordPress", ["wordpress"], ""),

  # INFRASTRUCTURE
  Skill("Ansible", ["ansible"], "Automation engine for configuration management, application deployment, and task automation."),
  Skill("CircleCI", ["circleci"], ""),
  Skill("CKA", ["cka"], ""), # certificate
  Skill("CKAD", ["ckad"], ""), # certificate
  Skill("CompTIA-ITOps", ["cios"], ""), # certificate
  Skill("MCSA", ["mcsa"], ""), # certificate
  Skill("Docker", ["docker"], ""),
  Skill("Dokku", ["dokku"], ""), # also Cloud
  Skill("Jenkins", ["jenkins"], ""),
  Skill("Kibana", ["kibana"], ""), # also BIGDATA
  Skill("Kubernetes", ["kubernetes", "k8s", "k3s"], ""),
  Skill("Logstash", ["logstash"], ""), # also BIGDATA
  Skill("Pulumi", ["pulumi"], ""),
  Skill("Puppet", ["puppet"], ""),
  Skill("Splunk", ["splunk"], ""), # also BIGDATA & SECURITY
  Skill("RHCE", ["rhce"], ""),   # certificate
  Skill("RHCSA", ["rhcsa"], ""), # certificate
  Skill("Terraform", ["terraform"], ""),
  Skill("Vagrant", ["vagrant"], ""),

  # QA-n-AUTOMATION
  Skill("Appium", ["appium"], ""),
  Skill("Cucumber", ["cucumber"], ""),
  Skill("Cypress", ["cypress", "cypress.=js"], ""),
  Skill("Jasmine", ["jasmine"], ""),
  Skill("Jest", ["jest"], ""),
  Skill("JUnit", ["junit"], ""),
  Skill("Playwright", ["playwright"], ""),
  Skill("Postman", ["postman"], ""),
  Skill("Protractor", ["protractor"], ""),
  Skill("PyTest", ["pytest"], ""),
  Skill("Selenium", ["selenium"], ""),
  Skill("Sentry", ["sentry"], ""),
  Skill("TestCafe", ["testcafe"], ""),
  Skill("TestNg", ["testng"], ""),
  Skill("WebdriverIO", ["webdriverio"], ""),

  # BLOCKCHAIN
  Skill("Arweave", ["arweave"], "A permanent and decentralized web inside an open ledger."),
  Skill("Bitcoin", ["bitcoin"], ""),
  Skill("Ethereum", ["ethereum"], ""),
  Skill("EVM", ["evm"], ""),
  Skill("Solana", ["solana"], ""),
  Skill("Web3js", ["web3.=js"], ""),
  # Skill("SVM", ["svm"], ""), TODO disambiguate Support-Vector-Machine vs Solana-Virtual-Machine
  # Skill("Web3", ["web3"], ""), topic/concept, not a skill

  # NETWORKING
  Skill("CompTIA-Network+", ["network+", "comptia n(etwork)+"], ""), # certificate
  Skill("Cisco-CNA", ["ccna"], ""), # certificate
  Skill("Cisco-CNP", ["ccnp"], ""), # certificate
  Skill("LoRa", [propn("LoRa")], ""), # transmission tech
  Skill("MTCNA", ["mtcna"], ""),    # certificate
  Skill("MQTT", ["mqtt"], ""),      # IoT messaging standard, also CLOUD
  Skill("Nmap", ["nmap"], ""),             # also SECURITY
  Skill("Netcat", ["netcat", "ncat"], ""), # also SECURITY
  Skill("Zigbee", ["zigbee"], ""), # protocol spec. also EMBEDDED
  Skill("Wireshark", ["wireshark"], ""),   # also SECURITY

  # SECURITY
  Skill("Burp-Suite", ["burp=suite"], "Proprietary vulnerability scanning, penetration testing, and webapp security platform."),
  Skill("CEH", ["ceh"], ""),     # certificate
  Skill("CISA", ["cisa"], ""),   # certificate
  Skill("CISM", ["cism"], ""),   # certificate
  Skill("CISSP", ["ciss", "cissp"], ""), # certificate
  Skill("CompTIA-PenTest+", ["pentest+", "comptia p(entest)+"], ""), # certificate
  Skill("CompTIA-Security+", ["security+", "comptia s(ecurity)+"], ""), # certificate
  Skill("GIAC-CIH", ["gcih"], ""),   # certificate
  Skill("GIAC-SEC", ["gsec"], ""),   # certificate
  Skill("GIAC-REM", ["grem"], ""),   # certificate
  Skill("GIAC-WAPT", ["gwapt"], ""), # certificate
  Skill("JWT", ["jwt"], ""),
  Skill("Metasploit", ["metasploit"], ""),
  Skill("Nessus", ["nessus"], ""),
  Skill("OAuth", [ver1("oauth")], ""),
  Skill("OpenID", ["openid"], ""),
  Skill("SAML", ["saml"], ""),
  Skill("Snort", [propn("snort")], ""),
  Skill("SSCP", ["sscp"], ""), # certificate

  # ROBOTICS
  Skill("ABB", ["abb"], ""),           # robot brand
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
  Skill("Debian", ["debian"], ""),
  Skill("FreeBSD", ["freebsd"], ""), # also CROSS-PLATFORM
  Skill("Linux", ["linux"], ""), # also CROSS-PLATFORM
  Skill("MacOS", ["macos", "osx"], ""), # also CROSS-PLATFORM
  Skill("Ubuntu", ["ubuntu"], ""),
  Skill("Unix", ["unix"], ""),   # also CROSS-PLATFORM
  Skill("Windows", ["windows", "win32", "win64"], ""), # also CROSS-PLATFORM

  Skill("Clang", ["clang"], ""),
  Skill("MicroPython", ["micropython"], ""), # compiler
  Skill("GCC", ["gcc"], ""), # compiler
  Skill("Kernel", ["kernel"], ""),
  Skill("LLVM", ["llvm"], ""),

  # BIGTECH
  Skill("Apple", ["apple"], ""), # company
  Skill("AMD", ["amd", "amd=32", "amd=64"], ""), # company
  Skill("eBay", ["ebay"], ""), # company
  Skill("Facebook", ["facebook"], ""), # company TODO meta
  Skill("Intel", ["intel"], ""), # company
  Skill("Netflix", ["netflix"], ""), # company
  Skill("NVidia", ["nvidia"], ""), # company
  Skill("SalesForce", ["salesforce"], ""),
  Skill("Vercel", ["vercel"], ""),

  # MIXED TOPICS
  Skill("CPU", ["cpu"], ""),
  Skill("GPU", ["gpu"], ""),
  Skill("CLI", ["cli"], ""),
  Skill("GUI", ["gui"], ""),
  Skill("UI", ["ui", "user=interface"], ""),
  Skill("API", ["api"], ""),
  Skill("IaaS", ["iaas"], ""),
  Skill("PaaS", ["paas"], ""),
  Skill("SaaS", ["saas"], ""),
  # Skill("Client", ["client"], ""),
  # Skill("Server", ["server"], ""),
  # Skill("REPL", ["repl"], ""),
  # Skill("Shell", ["shell"], ""), -- too widespread
  # Skill("Terminal", ["terminal"], ""), -- too widespread
  # Skill("Cross-Platform", ["cross=platform"], ""),
  Skill("TDD", ["tdd"], ""),
  Skill("BDD", ["bdd"], ""),
  Skill("Plugin", ["plugin", "plug-in"], ""),
  Skill("Widget", ["widget"], ""),
  Skill("Middleware", ["middleware"], ""),
  Skill("Bindings", ["bindings"], ""),
  Skill("Engine", ["engine"], ""),
  # Skill("Mobile", ["mobile"], ""),
  # Skill("PC", ["pc"], ""),
  # Skill("Web", ["web"], ""),
  # Skill("IoT", ["iot"], ""),
  Skill("CI/CD", ["ci/cd"], ""),
  Skill("Voxel", ["voxel"], ""),
  Skill("Pixel", ["pixel"], ""),
  Skill("Sprite", ["sprite"], ""),
  Skill("Texture", ["texture"], ""),
  # Skill("Byte", ["byte"], ""),
  Skill("Bytecode", ["bytecode"], ""),
  # Skill("2D", ["2d"], ""), -- too widespread
  # Skill("3D", ["3d"], ""), -- too widespread
  Skill("Ray-Tracing", ["ray=tracing"], ""),
  Skill("Compiler", ["compiler"], ""),
  Skill("Singleplayer", ["single=player"], ""),
  Skill("Multiplayer", ["multi=player"], ""),
  # Skill("Entity-Component-System", ["entity=component=system", "ecs"], ""), -- conflicts with AWS-ECS
  Skill("Cron", ["cron", "crond", "cronjob"], ""),
  Skill("IP", ["ip"], ""),
  Skill("TCP", ["tcp"], ""),
  Skill("HTTP", ["http"], ""),
  Skill("HTTPS", ["https"], ""),
  Skill("SSL", ["ssl"], ""),
  Skill("SSH", ["ssh"], ""),
  Skill("FTP", ["ftp"], ""),
  Skill("SFTP", ["sftp"], ""),
  Skill("E2E", ["e2e"], ""),
  Skill("RTOS", ["rtos"], ""),
  Skill("GPOS", ["gpos"], ""),
  # Skill("Analysis", ["analysis"], ""),
  # Skill("Analytics", ["analytics"], ""),
  # Skill("Network", ["network"], ""),
  # Skill("Networking", ["networking"], ""),
  # Skill("Machine-Learning", ["machine=learning", "ML", "ai/ml"], ""),
  # Skill("Deep-Learning", ["deep=learning"], ""),
  # Skill("Embedded", ["embedded"], ""),
  # Skill("Security", ["security", "appsec", "infosec", "cybersec"], ""),
  # Skill("Performance", ["performance"], ""),
  # Skill("Scalability", ["scalability"], ""),
  # Skill("Reliability", ["reliability"], ""),
  # Skill("Resiliency", ["resiliency"], ""),
  # Skill("Database", ["database", "db"], ""),
  # Skill("Deploy", ["deploy"], ""),
  # Skill("Architecture", ["architecture"], ""),
  # Skill("Integration", ["integration"], ""),
  # Skill("QA", ["qa"], ""),
  # Skill("Testing", ["testing"], ""),
  # Skill("Automation", ["automation"], ""),
  # Skill("Scraping", ["scraping"], ""),
  # Skill("Mining", ["mining"], ""), # ambiguous (Data-mining vs Crypto-mining)
  # Skill("Software", ["software"], ""),
  # Skill("Hardware", ["hardware"], ""),
  # Skill("Firmware", ["firmware"], ""),
  # Skill("Algorithm", ["algorithm(s)"], ""),
  # Skill("Science", ["science"], ""),
  # Skill("CMS", ["cms"], ""),
  # Skill("E-Commerce", ["e=commerce"], ""),
  # Skill("Cluster", ["cluster"], ""),
  # Skill("Container", ["container"], ""),
  # Skill("Orchestration", ["orchestration"], ""),
  # Skill("NLP", ["nlp"], ""),

  # HARDWARE & EMBEDDED
  # Skill("HPC", ["hpc"], ""), # high performance computing
  Skill("Arduino", ["arduino"], ""), # controller brand
  Skill("ASIC", ["asic"], ""), # ASICs are custom-designed circuits for specific applications, offering high performance and efficiency
  Skill("ARC", [propn("ARC")], ""), # CPU family
  Skill("ARC", ["arc"], "", disambiguate=neighbour(2)), # /
  Skill("AutoCAD", ["autocad"], ""),
  Skill("AVR", ["avr"], ""), # controller family
  Skill("Elbrus-2000", ["elbrus=2000", "e2k"], ""), # CPU
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
  Skill("Raspberry-Pi", ["raspberry", "rasp=pi", "raspberry=pi(s)"], ""), # platform
  Skill("RISC", ["risc", "risc-v"], ""), # CPU architecture
  Skill("SPARC", ["sparc"], ""), # platform
  Skill("Altium-Designer", ["altium=designer"], ""), # tool
  Skill("Altium-365", ["altium=365"], ""), # tool
  Skill("Autodesk", ["autodesk"], ""), # company
  Skill("Autodesk-Fusion", ["autodesk=fusion", "fusion=360"], ""), # tool
  Skill("Autodesk-Eagle", ["autodesk=eagle"], ""), # tool
  Skill("Autodesk-Eagle", ["eagle"], "", disambiguate=contextual("Autodesk", "AutoCAD")), # /
  Skill("Touchdesigner", ["touchdesigner"], ""), # visual development platform
  Skill("Solidworks", ["solidworks=pcb", "solidworks"], ""), # CB design tool
  Skill("STM32", ["stm=32"], ""), # platform
  Skill("Verilog", ["verilog", "sysverilog", "systemverilog"], ""), # PL
  Skill("VHDL", ["vhdl"], ""), # PL
  Skill("VLIW", ["vliw"], ""), # CPU architecture
  Skill("x32", ["x32"], ""), # CPU architecture umbrella
  Skill("x64", ["x64"], ""), # CPU architecture umbrella
  Skill("x86", ["x86", "x86-32", "x86-64", "i286", "i386"], ""), # CPU architecture
  Skill("Yosys", ["yosys"], ""), # https://github.com/YosysHQ/yosys
  Skill("Z80", ["z=80"], ""), # CPU brand

  # DESKTOP
  # Skill("Electron", ["electron"], ""), tons of FP

  # LANGUAGES
  Skill("Ada", ["ada"], ""),
  Skill("Apex", ["apex"], ""),
  Skill("Assembly", ["assembly"], ""),
  Skill("C", ["c-lang", "c"], ""),
  Skill("C++", ["c++", "cpp", "c=plus=plus"], ""),
  Skill("C#", ["c#", "csharp"], ""),
  Skill("Clojure", ["clojure", "clojurian"], ""),
  Skill("ClojureScript", ["clojure=script"], ""),
  Skill("Cobol", ["cobol"], ""),
  Skill("Crystal", ["crystal=lang", "crystal"], ""),
  Skill("CSS", [ver1("css")], ""),
  Skill("D", ["d", "d=lang"], ""),
  Skill("Dart", ["dart"], ""),
  Skill("Delphi", ["delphi"], ""),
  Skill("Elixir", ["elixir"], ""),
  Skill("Elm", ["elm"], ""),
  Skill("Erlang", ["erlang"], ""),
  Skill("Fortran", ["fortran"], ""),
  Skill("F#", ["f#", "f=lang", "fsharp"], ""),
  Skill("Gleam", ["gleam"], ""),
  Skill("Go", ["golang", propn("go")], ""),
  Skill("Groovy", ["groovy"], ""),
  Skill("Haskell", ["haskell"], ""),
  Skill("HTML", [ver1("html")], ""),
  Skill("Java", [ver1("java")], ""),
  Skill("JavaScript", ["java=script", "js"], ""),
  Skill("Julia", ["julia"], ""),
  Skill("Kotlin", ["kotlin"], ""),
  Skill("Lisp", ["lisp"], ""),
  Skill("Lua", ["lua"], ""),
  Skill("Nim", ["nim"], ""),
  Skill("Makefile", ["makefile"], ""),
  Skill("Matlab", ["matlab"], ""),
  Skill("Mojo", ["mojo"], ""),
  Skill("Objective-C", ["objective=c", "objective=c++", "objective=cpp"], ""),
  Skill("Ocaml", ["ocaml"], ""),
  Skill("Odin", ["odin"], ""),
  Skill("Perl", ["perl"], ""),
  Skill("PHP", [ver1("php"), "phper"], ""),
  Skill("PowerShell", ["power=shell"], ""),
  Skill("Prolog", ["prolog"], ""),
  Skill("Python", ["python", "pythonist(a)"], ""),
  Skill("R", ["r=lang", "r"], ""),
  Skill("Ruby", ["ruby=lang", "ruby", "rubyist", "rubist"], ""),
  Skill("Rust", ["rust", "rustacean"], ""),
  Skill("SASS", ["sass", "scss"], ""),
  Skill("Scala", ["scala"], ""),
  Skill("Solidity", ["solidity"], ""),
  Skill("Swift", ["swift"], ""),
  Skill("TypeScript", ["type=script", "ts"], ""),
  Skill("Shell", ["shell", "bash", "zsh"], ""),
  Skill("SQL", ["sql"], ""),
  # Skill("XML", ["xml"], ""),
  Skill("V", ["v", "vlang"], ""),
  Skill("Vala", ["vala"], ""),
  Skill("Vyper", ["vyper"], ""),
  Skill("Visual-Basic", ["visual=basic", "vb(a)", "vb.net"], ""),
  Skill("WebAssembly", ["wasm", "web=assembly"], ""),
  Skill("Zig", ["zig"], ""),

  # UNSORTED
  Skill("Blender", ["blender"], ""),
  Skill("CompTIA-A+", ["comptia a+"], ""), # certificate for tech. support and IT ops
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
#   "Chef": {pattern: "chef", category: "platform", role: "Engineer"},
#   // should we add new char like "css𝐕" or should we consume numbers after EACH term?
#   // Most skills have versions BUT topics don't @_@
#   // So it can be a per-table configuration
#   "ETL": {pattern: "etl", category: "topic", role: "Engineer"},
#   "Native Android": {pattern: "native=android", category: "platform", role: "Engineer"},
#   "Native iOS": {pattern: "native-ios", category: "platform", role: "Engineer"},
#   "Octave": {pattern: "octave", category: "lang"},
#   // "Polygon": {pattern: "polygon", category: "tech", role: "Engineer"},
#   "Prisma": {pattern: "prisma", category: "tech", role: "Engineer"},
#   "OpenAPI": {pattern: "open=api", category: "tech"},
#   "OpenAuth": {pattern: "open=auth2?, oauth2?", category: "tech"},
#   "RxJS": {pattern: "rx.=js, RX", category: "tech", role: "Engineer"},
#   "Salt": {pattern: "salt", category: "platform", role: "Engineer"},
#   "Vyper": {pattern: "vyper", category: "lang", role: "Engineer"},
#   "Web3.js": {pattern: "web3.js", category: "tech"},
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
