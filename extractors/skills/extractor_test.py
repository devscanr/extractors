from ..utils import normalize
from .extractor import SkillExtractor

extractor = SkillExtractor()

def extract_many(texts: list[str]) -> list[list[str]]:
  return extractor.extract_many([normalize(text) for text in texts])

def extract(text: str) -> list[str]:
  return extractor.extract(normalize(text))

def describe_SkillExtractor() -> None:
  def describe_extract_many() -> None:
    def it_works() -> None:
      assert extract_many(["Joomla", "modx"]) == [
        ["Joomla"],
        ["MODx"],
      ]

  def describe_extract() -> None:
    def it_handles_adhoc_set1() -> None:
      assert extract("computer") == ["Computer"]
      assert extract("data") == ["Data"]
      assert extract("my user data") == []
      assert extract("computer and data science") == ["Computer-Science", "Data-Science"]
      assert extract("data & computer science") == ["Data-Science", "Computer-Science"]
      assert extract("data, computer science") == ["Data-Science", "Computer-Science"]
      assert extract("comp-sci") == ["Computer-Science"]
      assert extract("Computer-Science") == ["Computer-Science"]
      assert extract("computer scientist") == ["Computer-Science"]
      assert extract("dataScience") == ["Data-Science"]
      assert extract("data-scientist") == ["Data-Science"]

    def it_handles_adhoc_set2() -> None:
      assert extract("programming") == ["Engineering"]
      assert extract("computer programming") == ["Computer", "Engineering"]
      assert extract("web programming") == ["Web-Engineering"]
      assert extract("php programming") == ["PHP", "Engineering"]
      assert extract("programming with PHP") == ["Engineering", "PHP"]
      assert extract("just programming on computers") == ["Engineering"]

    def it_handles_adhoc_set3() -> None:
      assert extract("software engineering") == ["Software-Engineering"]
      assert extract("software and hardware engineering") == ["Software-Engineering", "Hardware-Engineering"]
      assert extract("engineer of software") == ["Software-Engineering"]
      assert extract("mobile engineer") == ["Mobile-Engineering"]
      assert extract("game engineering") == ["Game-Engineering"]

    def it_handles_adhoc_set4() -> None:
      assert extract("fullstack qa") == ["Fullstack", "QA"]
      # TODO more about QA

    def it_handles_adhoc_set5() -> None:
      assert extract("Development") == ["Engineering"]
      assert extract("Laravel Development") == ["Laravel", "Engineering"]
      assert extract("PHP Development") == ["PHP", "Engineering"]
      assert extract("PHP Tester") == ["PHP", "Testing"]
      assert extract("Backend Development") == ["Backend", "Engineering"]
      assert extract("Web (PHP) Development") == ["PHP", "Web-Engineering"]
      assert extract("Web and PHP programming") == ["PHP", "Web-Engineering"]
      assert extract("Web (PHP) Development. Some engineering") == ["PHP", "Web-Engineering", "Engineering"]

    def it_handles_adhoc_set6() -> None:
      assert extract("Mobile design and engineering") == ["UI-Design", "Mobile-Engineering"]
      assert extract("Web engineering & design") == ["Web-Engineering", "Web-Design"]
      assert extract("Game design/dev") == ["Game-Design", "Game-Engineering"]

    def it_handles_adhoc_set7() -> None:
      assert extract("analysis + analytics") == ["Analysis"]
      assert extract("data and business analyst") == ["Data-Analysis", "Business-Analysis"]
      assert extract("business/data analytics") == ["Business-Analysis", "Data-Analysis"]
      assert extract("analytics for any business") == ["Business-Analysis"]
      assert extract("analizing data for a small business") == ["Data", "Business"] # "analyzing" is not a term for now

    def it_handles_adhoc_set8() -> None:
      assert extract("devops") == ["Dev-Operations"]
      assert extract("data-ops") == ["Data-Operations"]
      assert extract("data-ops") == ["Data-Operations"]
      assert extract("ml and data ops") == ["ML-Operations", "Data-Operations"]
      assert extract("dev-sec-ops") == ["Dev-Operations", "Security-Operations"]
      assert extract("dev/sec ops") == ["Dev-Operations", "Security-Operations"]
      assert extract("1 sec to finish") == []

    def it_handles_adhoc_set9() -> None:
      assert extract("Websec") == ["Web-Security"]
      assert extract("Websecurity") == ["Web-Security"]
      assert extract("Web security") == ["Web-Security"]
      assert extract("Web & Network security") == ["Web-Security", "Network-Security"]

    def it_handles_adhoc_set10() -> None:
      assert extract("Kafka and Pig all the way") == ["Apache-Kafka", "Apache-Pig"]
      assert extract("Guinea Pig loves Science.") == ["Science"]
      assert extract("Guinea Pig loves Science. Hadoop!") == ["Apache-Pig", "Science", "Apache-Hadoop"]
      assert extract("Apache Guinea Pig loves Science.") == ["Apache", "Apache-Pig", "Science"]
      assert extract("My name is Jax") == []
      assert extract("Jax, TensorFlow") == ["JAX", "TensorFlow"]
      assert extract("Jax vs TensorFlow") == ["JAX", "TensorFlow"]

    def it_handles_adhoc_set11() -> None:
      assert extract("I learn v.") == [] # v. is a special case in Spacy, like v.1 for version...
      assert extract("I learn v lang") == ["V"]
      assert extract("I learn v-lang") == ["V"]
      assert extract("I learn v-language") == ["V"]
      assert extract("I learn v-stuff") == []
      assert extract("V-JEPA") == []
      assert extract("I learn c lang") == ["C"]
      assert extract("I learn stuff-c") == []
      assert extract("C. Objective-C. C++") == ["C", "Objective-C", "C++"]
      assert extract("Ph.D. candidate, interested in software security") == ["Software", "Security"]

    def it_handles_adhoc_set12() -> None:
      assert extract("Graphic Designer") == ["Graphic-Design"]
      assert extract("visual design") == ["Visual-Design"]

    def it_handles_adhoc_set13() -> None:
      assert extract("system administration") == ["System-Administration"]
      assert extract("database administration") == ["Database-Administration"]
      assert extract("senior dba") == ["Database-Administration"]

    def it_handles_adhoc_set14() -> None:
      assert extract("automated test") == ["Automated-Testing"]
      assert extract("automated testing") == ["Automated-Testing"]
      assert extract("automated qa") == ["Automated-Testing", "QA"]
      assert extract("test automation") == ["Automated-Testing"]
      assert extract("qa & automation") == ["QA", "Automated-Testing"]
      assert extract("qa & testing") == ["QA", "Testing"]
      assert extract("qa & automation testing") == ["QA", "Automated-Testing"]
      assert extract("tester and qa") == ["Testing", "QA"]
      assert extract("automated tester and qa") == ["Automated-Testing", "QA"]

    def it_handles_natural_set1() -> None:
      assert extract("Self-employed web engineer. #Rust #Wasm #Go #TypeScript #React #REST") == [
        "Web-Engineering", "Rust", "WebAssembly", "Go", "TypeScript", "React", "REST"
      ]
      assert extract("I like Postgres, Kubernetes, Docker, DevOps.") == [
        "PostgreSQL", "Kubernetes", "Docker", "Dev-Operations",
      ]
      assert extract("working with React, Node, Go, and the rest") == [
        "React", "NodeJS", "Go"
      ]
      assert extract("LDM ball cube ball big cube ball next Rest In Peace niflheim vismuth slow wave fast robot keep going! slow ship go! slow ball Auto? fast dual ufo") == []

    def it_handles_natural_set2() -> None:
      assert extract("Po of Open棟梁 Pj / PMP / .NET, .NET Core ≫ OAuth / OIDC, FAPI, FIDO, SAML") == [
        ".NET", "OAuth", "SAML"
      ]
      assert extract("≫ IdMaaS, mBaaS / JavaScript ≫ Frontend, IoT Edge. 静岡 → 新潟 → 東京 → 広島") == [
        "BaaS", "JavaScript", "Frontend", "IoT"
      ]
      assert extract("Node.js, Angular, React.js, PHP, Apollo Data Graph, OpenAPI, More...") == [
        "NodeJS", "Angular", "React", "PHP", "Apollo", "OpenAPI"
      ]
      assert extract("With no desire，at rest and still. All things go right as of their will") == []

    def it_handles_natural_set3() -> None:
      assert extract("Fullstack web developer with focus on front end services.") == [
        "Fullstack", "Web-Engineering", "Frontend"
      ]
      assert extract("Experienced with React/React Native, PHP, MySQL, GraphQL, Angularjs, Prisma, Expo") == [
        "React", "React-Native", "PHP", "MySQL", "GraphQL", "Angular", "Prisma"
      ]
      assert extract("developer with expertise in ASP.Net (Legacy, Core), Angular, Ionic, NativeScript") == [
        "Engineering", "ASP.NET", "Angular", "Ionic", "Native-Script"
      ]
      assert extract("#Python #Jupyter #pandas #docker") == [
        "Python", "Jupyter", "Pandas", "Docker"
      ]
      assert extract("I have no idea how far I can go, but I`m sure I don`t like to stay here for the rest of my life") == []

    def it_handles_natural_set4() -> None:
      assert extract("Web & Blockchain Developer 🎨React(Next), Vue(Nuxt), 🎄Laravel") == [
        "Blockchain", "Web-Engineering", "React", "NextJS", "VueJS", "NuxtJS", "Laravel"
      ]
      assert extract("NumPy, SciPy, Numba, Conda, PyData, NumFocus, Anaconda, Quansight, OpenTeams") == [
        "NumPy", "SciPy", "Numba", "Anaconda"
      ]
      assert extract("✐Python ✎Jupyter Notebook, Flutter 🎈Smart Contract(Solidity)=") == [
        "Python", "Jupyter", "Flutter", "Solidity"
      ]
      assert extract("Debugger debugger at WebStorm JetBrains MSE student at ITMO University") == []

    def it_handles_natural_set5() -> None:
      assert extract("Software Engineer, Tech Lead in Rust, WASM, TypeScript") == [
        "Software-Engineering", "Rust", "WebAssembly", "TypeScript",
      ]
      assert extract("React | Node JS | REST") == [
        "React", "NodeJS", "REST",
      ]
      assert extract("REST | MEAN Stack developer") == [
        "REST", "MongoDB", "Express", "Angular", "NodeJS", "Engineering"
      ]
      assert extract("Senior Backend Developer (.NET) at Dow Jones") == [
        "Backend", "Engineering", ".NET",
      ]
      assert extract("cosmologist | @conda-forge core | @conda steering (emeritus)") == []
      assert extract("Ce qui mérite d'être") == []

    def it_handles_natural_set6() -> None:
      assert extract("Go/Python/Java, Web/K8S") == [
        "Go", "Python", "Java", "Web", "Kubernetes"
      ]
      assert extract("NIT Robocon Member 🥰 Arduino / OpenSiv3D / Qt / WindowsAPI / C / C++ / Roblox") == [
        "Arduino", "Qt", "C", "C++", "Roblox"
      ]
      assert extract("Community-supported HTML5 CSS3 platform extension for Unreal Engine 4") == [
        "HTML", "CSS", "Unreal-Engine"
      ]
      assert extract("@jupyter | @jupyterhub | @ipython | @jupyter-incubator") == []
      assert extract("@jupyter-resources | @jupytercalpoly | @jupyter-attic") == []

    def it_handles_natural_set7() -> None:
      assert extract("Ruby/Rails JavaScript Ember.js Clojure Node.js") == [
        "Ruby", "Ruby-on-Rails", "JavaScript", "EmberJS", "Clojure", "NodeJS"
      ]
      assert extract("Ethereum | Flutter | Hyperledger Fabric") == [
        "Ethereum", "Flutter"
      ]
      assert extract("Unity, ECS EC2, Node.JS Android") == [
        "Unity", "Amazon-ECS", "Amazon-EC2", "NodeJS", "Android"
      ]
      assert extract("Dev & Speaker • Microsoft MVP Azure, .NET, Blazor 🥔 Couch potato") == [
        "Engineering", "Microsoft", "Microsoft-Azure", ".NET", "Blazor"
      ]
      assert extract("far better rest I go to than I have ever known") == []

    def it_handles_natural_set8() -> None:
      assert extract("Engineer on Azure-AWS, Kubernetes AKS-EKS-GKE") == [
        "Engineering", "Microsoft-Azure", "Amazon-WebServices", "Kubernetes",
        "Azure-Kubernetes", "Amazon-EKS", "Google-Kubernetes"
      ]
      assert extract("Terraform, Golang, Ansible, HashiCorp Vault") == [
        "Terraform", "Go", "Ansible"
      ]
      assert extract("Angular || React (NextJs) || Svelte kit || Node || Nest || PHP5 || Couch CMS") == [
        "Angular", "React", "NextJS", "SvelteKit", "NodeJS", "NestJS", "PHP", "CMS"
      ]
      assert extract("Full-stack developer Vue, Nuxt, Wordpress+GraphQL") == [
        "Fullstack", "Engineering", "VueJS", "NuxtJS", "WordPress", "GraphQL"
      ]
      assert extract("I'm learning #go and #rest") == ["Go", "REST"]
      assert extract("I'm learning the rest as I go on") == []
      assert extract("Where projects go to rest") == []

    def it_handles_natural_set9() -> None:
      assert extract("FULL STACK JAVA | NETBEANS | C# | MICROSOFT MANAGEMENT STUDIO | VISUAL CODE | JUPYTER NOTEBOOK | PYTHON & RUBY") == [
        "Fullstack", "Java", "C#", "MS-SQLServer", "Jupyter", "Python", "Ruby"
      ]
      assert extract("Learning ReactJS & Next.js to become a proficient frontender") == [
        "React", "NextJS", "Frontend"
      ]
      assert extract("Power BI, my-sql-manager, Dotnet, Django/Python") == [
        "Power-BI", "MySQL", ".NET", "Django", "Python"
      ]
      assert extract("The java.lang.Math") == [] # "Mathematics"
      assert extract("hey are a bi person, my@sql") == []
      assert extract("PHP phper, Python pythonista") == ["PHP", "Python"]
      assert extract("Where old projects go to live out the rest of their days") == []

    def it_handles_natural_set10() -> None:
      assert extract("I'm Julia, a marketing manager") == ["Julia"] # known FP , "Marketing", "Management"
      assert extract("I learn Julia language") == ["Julia"]
      assert extract("developer:iOS,Robot,Fintech") == ["Engineering", "iOS"] # , "iOS", "Finance"
      assert extract("C Plus Plus programmar from India") == ["C++"]
      assert extract("hey are a bi person, my@sql") == []
      assert extract("PHP phper, Python pythonista") == ["PHP", "Python"]
      assert extract("Where old projects go to live out the rest of their days") == []

    def it_handles_natural_set11() -> None:
      assert extract("Keen user of d3.js, and Raspberry Pi's.") == ["D3JS", "Raspberry-Pi"]
      assert extract("Arduino addict. Java programmer in real life") == ["Arduino", "Java", "Engineering"]
      assert extract("C#,C++,Firebase,Unity") == ["C#", "C++", "Google-Firebase", "Unity"]
      assert extract("R, Matlab, Tableau") == ["R", "Matlab", "Tableau"]
      assert extract("Pulumi, Kotlin, PowerShell | Postgres") == ["Pulumi", "Kotlin", "PowerShell", "PostgreSQL"]
      assert extract("MariaDB for backend | Scss for the FE") == ["MariaDB", "Backend", "SASS", "Frontend"]
      assert extract("To be or not to BE") == [] # no FP!

    def it_handles_natural_set12() -> None:
      assert extract("ARM processors") == ["ARM"]
      assert extract("Hi, my name is Arm") == ["ARM"] # FP
      assert extract("My left arm is stronger than my right arm") == []
      assert extract("I’m doing high-performance computing work on CPU, including x86, arm.") == [
        "Performance", "Computer", "CPU", "x86", "ARM"
      ]
      assert extract("Embrace AI-IoT | RISC-V | ARM | ARC") == ["AI", "IoT", "RISC", "ARM", "ARC"]
      assert extract("PERN afficianado") == ["PostgreSQL", "Express", "React", "NodeJS"]

    def it_handles_natural_set13() -> None:
       assert extract("My favorite language is Jax") == []
       assert extract("My name is Jax") == []
       assert extract("Hi, I'm Jax, an avid computer sorcerer") == ["Computer"]
       assert extract("CUDA C++ , Pytorch RT, JAX(JIT,Haiku enjoyer, FLAX Flexer)") == ["CUDA", "C++", "PyTorch", "JAX", "Flax"]
       assert extract("JAX @NVIDIA") == ["JAX"]
       assert extract("Scientist @ JAX") == ["Science", "JAX"]
       assert extract("I like learning | JAX | Google Brain") == ["JAX", "Google"]
       assert extract("Software Engineer at Google DeepMind working on JAX/Flax") == [
         "Software-Engineering", "Google", "JAX", "Flax"
       ]
       assert extract("Jax + Haiku fan. Self-attention for the win") == [] # known FN
       assert extract("Julia, GraalVM, LLVM, NVidia, CNCF, Program Synthesis, 3D-QSAR") == ["Julia", "LLVM", "NVidia"]
       assert extract("Sample for UE5's CommonConversation Feature") == ["Unreal-Engine"]

    def it_handles_natural_set14() -> None:
      assert extract("Android(Kotlin) | iOS(Swift) | Spring Boot(Java) | Python(Django)") == [
        "Android", "Kotlin", "iOS", "Swift", "Spring", "Java", "Python", "Django"
      ]
      assert extract("ClickHouse, linux, perl, python, C++, kafka") == [
        "ClickHouse", "Linux", "Perl", "Python", "C++", "Apache-Kafka"
      ]
      assert extract("Software Eng @ClickHouse") == ["Software-Engineering"]
      assert extract("Love making games") == [] # for now
      assert extract("""
        I'm a 21 year old embedded systems electronics engineer.
        Mostly interested in robotics, low-level coding and homebrew.
      """) == ["Embedded-Engineering", "System-Engineering", "Robotics", "Engineering"] # , "Electronics"
      assert extract("""
        Programmer, cybersecurity expert, and 2017 penetration tester
      """) == ["Engineering", "Cyber-Security", "Penetration-Testing"]

    def it_handles_set15() -> None:
      assert extract("Blockchain developer, bulding for DeFi.") == ["Blockchain", "Engineering", "DeFi"]
      assert extract("""
        FullStack Web Developer | Penetration Tester
      """) == ["Fullstack", "Web-Engineering", "Penetration-Testing"]
      assert extract("""
        Student in saylani mass it training program and learn web and app
        development and I'm completed my content management system WordPress course.
      """) == ["Web-Engineering", "CMS", "WordPress"]

    def it_handles_natural_set16() -> None:
      assert extract("NVIDIA Technologies for game and application developers") == ["NVidia", "Game"]
      assert extract("Open source continuous integration for games") == ["Open-Source", "CI/CD"]
      assert extract("Game developer.") == ["Game-Engineering"]
      assert extract("Game Server Programmer :)") == ["Game-Engineering"]
      assert extract("I'm a JS / TS specialist focused on web and game development.") == [
        "JavaScript", "TypeScript", "Web-Engineering", "Game-Engineering"
      ]
      assert extract("Game-related tidbits + bytes found on GitHub") == ["Game", "GitHub"]
      assert extract("Working on a Game Engine") == ["Game"]
      assert extract("Game Security & Realtime Rendering") == ["Game", "Security"]
      assert extract("game of game") == ["Game"]
      assert extract("Like world and game") == ["Game"]
      assert extract("Father, hacker, blogger, gamer, & nerd. Bounty Hunter") == [] # "Hacking"

    def it_handles_natural_set17() -> None:
      assert extract("3D game engine development amateur") == ["Game-Engineering"]
      assert extract("Deep Learning Student | Game Dev") == ["Deep-Learning", "Game-Engineering"]
      assert extract("Game Hacking") == ["Game"] # , "Hacking"
      assert extract("ex-game developer") == ["Game-Engineering"]
      assert extract("Like world and game") == ["Game"]
      assert extract("Gaming the game is Gabe's game.") == ["Game"]
      assert extract("Computational Game Theory Research") == [] # "Research"

    def it_handles_natural_set18() -> None:
      assert extract("CS-sophomore | Game-dev (Unity & C#)") == ["Computer-Science", "Game-Engineering", "Unity", "C#"]
      assert extract("Game assets, software and games") == ["Game", "Software"]
      assert extract("JavaScript, the BEST game") == ["JavaScript", "Game"]
      assert extract("I'm a Professional C++ Game and Software Developer from New York.") == [
        "C++", "Game-Engineering", "Software-Engineering"
      ]
      assert extract("Gamedev and shite") == ["Game-Engineering"]
      assert extract("The Game") == ["Game"]

    def it_handles_natural_set19() -> None:
      assert extract("I love to research malware, viruses, and other types of malicious files.") == [
        "Malware" # "Research",
      ]
      assert extract("CS PhD student at Stony Brook University, new to Distributed System.") == [
        "Computer-Science", "Distributed", "System"
      ]
      assert extract("Building Distributed SQL Database") == [
        "Distributed", "SQL", "Database"
      ]
      assert extract("Computer science student with an interest in data science.") == [
        "Computer-Science", "Data-Science"
      ]
      assert extract("Dive into the world of sophistication with U-Glam NYC, your quintessential destination for luxury jewelry, headbands, and pearls.Based in the heart of New York.") == [
        # empty
      ]
      assert extract("Salesforce Guru") == ["SalesForce"]
      assert extract("Aspiring Machine Learning / Data Engineer") == [
        "ML-Engineering", "Data-Engineering"
      ]
      assert extract("Healthcare data analyst freelancer") == [
        "Data-Analysis" # "Health",
      ]
      assert extract("looking to help clients use their data to the fullest.") == []

    def it_handles_set20() -> None:
      assert extract("data-backed decision making: statistical analysis, Computational Fluid Dynamics") == [
        "Data-Analysis"
      ]
      assert extract("Campaign Lead, Data Scientist, Statistician") == [
        "Data-Science", # "Leadership", "Statistics"
      ]
      assert extract("Font-End Website Developer and Software Developer with a Bachelor of Science in Informatics.") == [
        "Web-Engineering", "Software-Engineering", "Science", # "Informatics"
      ]
      assert extract("a Microsoft Technical Trainer specializing in Data & AI") == [
        "Microsoft", "Data", "AI"
      ]
      assert extract("SQL Server/Cloud DBA") == [
        "MS-SQLServer", "Cloud", "Database-Administration"
      ]

# interested in data science, neuroscience, and machine learning
# All About Quantum Computer
# I love making games - FN
