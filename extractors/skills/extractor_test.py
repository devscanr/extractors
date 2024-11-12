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
    def it_disambiguates_set1() -> None:
      assert extract("Kafka and Pig all the way") == ["Apache-Kafka", "Apache-Pig"]
      assert extract("Guinea Pig loves Science.") == []
      assert extract("Guinea Pig loves Science. Hadoop!") == ["Apache-Pig", "Apache-Hadoop"]
      assert extract("Apache Guinea Pig loves Science.") == ["Apache", "Apache-Pig"]
      assert extract("My name is Jax") == []
      assert extract("Jax, TensorFlow") == ["JAX", "TensorFlow"]
      assert extract("Jax vs TensorFlow") == ["JAX", "TensorFlow"]

    def it_handles_set1() -> None:
      assert extract("Self-employed web engineer. #Rust #Wasm #Go #TypeScript #React #REST") == [
        "Web", "Rust", "WebAssembly", "Go", "TypeScript", "React", "REST"
      ]
      assert extract("I like Python, JS/TS, Go, Postgres, Kubernetes, Docker, DevOps.") == [
        "Python", "JavaScript", "TypeScript", "Go", "PostgreSQL", "Kubernetes", "Docker", "DevOps",
      ]
      assert extract("working with React, Node, Go, and the rest") == [
        "React", "NodeJS", "Go"
      ]
      assert extract("LDM ball cube ball big cube ball next Rest In Peace niflheim vismuth slow wave fast robot keep going! slow ship go! slow ball Auto? fast dual ufo") == []

    def it_handles_set2() -> None:
      assert extract("Po of Open棟梁 Pj / PMP / .NET, .NET Core ≫ OAuth / OIDC, FAPI, FIDO, SAML") == [
        ".NET", "OAuth", "SAML"
      ]
      assert extract("≫ IdMaaS, mBaaS / JavaScript ≫ Frontend, IoT Edge. 静岡 → 新潟 → 東京 → 広島") == [
        "JavaScript", "Frontend", "IoT"
      ]
      assert extract("Flutter, Node.js, Angular, React.js, PHP, Apollo Data Graph, OpenAPI, More...") == [
        "Flutter", "NodeJS", "Angular", "React", "PHP", "Apollo", "OpenAPI"
      ]
      assert extract("With no desire，at rest and still. All things go right as of their will") == []

    def it_handles_set3() -> None:
      assert extract("Fullstack web developer with focus on front end services. Experienced with React/React Native, PHP, MySQL, GraphQL, Angularjs, Prisma, Expo") == [
        "Fullstack", "Web", "React", "React-Native", "PHP", "MySQL", "GraphQL", "Angular", "Prisma"
      ]
      assert extract("A Full Stack developer with expertise in ASP.Net (Legacy, Core), Angular, Ionic, NativeScript, nopCommerce and more...") == [
        "ASP.NET", "Angular", "Ionic", "Native-Script"
      ]
      assert extract("#Python #Jupyter #pandas #docker") == [
        "Python", "Jupyter", "Pandas", "Docker"
      ]
      assert extract("I have no idea how far I can go, but I`m sure I don`t like to stay here for the rest of my life") == []

    def it_handles_set4() -> None:
      assert extract("Web & Blockchain Developer 🎨React(Next), Vue(Nuxt), Angular, 🎄Laravel, Node.js, Django 🎗React Native") == [
        "Web", "Blockchain", "React", "NextJS", "VueJS", "NuxtJS", "Angular", "Laravel", "NodeJS", "Django", "React-Native"
      ]
      assert extract("NumPy, SciPy, Numba, Conda, PyData, NumFocus, Anaconda, Quansight, OpenTeams") == [
        "NumPy", "SciPy", "Numba", "Anaconda"
      ]
      assert extract("✐Python ✎Jupyter Notebook, Flutter 🎈Smart Contract(Solidity)=") == [
        "Python", "Jupyter", "Flutter", "Solidity"
      ]
      assert extract("Debugger debugger at WebStorm JetBrains MSE student at ITMO University") == []

    def it_handles_set5() -> None:
      assert extract("Software Engineer, Tech Lead in Rust, WASM, TypeScript") == [
        "Software", "Rust", "WebAssembly", "TypeScript",
      ]
      assert extract("React | Node JS | REST") == [
        "React", "NodeJS", "REST",
      ]
      assert extract("REST | MEAN Stack developer") == [
        "REST", "MongoDB", "Express", "Angular", "NodeJS"
      ]
      assert extract("Senior Backend Developer (.NET) at Dow Jones") == [
        "Backend", ".NET",
      ]
      assert extract("cosmologist | @conda-forge core | @conda steering (emeritus)") == []
      assert extract("Ce qui mérite d'être") == []

    def it_handles_set6() -> None:
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

    def it_handles_set7() -> None:
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
        "Microsoft", "Microsoft-Azure", ".NET", "Blazor"
      ]
      assert extract("far better rest I go to than I have ever known") == []

    def it_handles_set8() -> None:
      assert extract("Engineer on Azure-AWS, Kubernetes AKS-EKS-GKE") == [
        "Microsoft-Azure", "Amazon-WebServices", "Kubernetes", "Azure-Kubernetes", "Amazon-EKS", "Google-Kubernetes"
      ]
      assert extract("Terraform, Golang, Ansible, HashiCorp Vault") == [
        "Terraform", "Go", "Ansible"
      ]
      assert extract("Angular || React (NextJs) || Svelte kit || Node || Nest || PHP5 || Couch CMS") == [
        "Angular", "React", "NextJS", "SvelteKit", "NodeJS", "NestJS", "PHP", "CMS"
      ]
      assert extract("Full-stack developer Vue, Nuxt, Wordpress+GraphQL") == [
        "VueJS", "NuxtJS", "WordPress", "GraphQL"
      ]
      assert extract("I'm learning #go and #rest") == ["Go", "REST"]
      assert extract("I'm learning the rest as I go on") == []
      assert extract("Where projects go to rest") == []

    def it_handles_set9() -> None:
      assert extract("FULL STACK JAVA | NETBEANS | C# | MICROSOFT MANAGEMENT STUDIO | JAVASCRIPT | VISUAL CODE | JUPYTER NOTEBOOK | PYTHON & RUBY") == [
        "Java", "C#", "Microsoft", "JavaScript", "Jupyter", "Python", "Ruby"
      ]
      assert extract("Learning ReactJS & Next.js to become a proficient frontender") == [
        "React", "NextJS", "Frontend"
      ]
      assert extract("Power BI, my-sql-manager, Dotnet, Django/Python") == [
        "Power-BI", "MySQL", ".NET", "Django", "Python"
      ]
      assert extract("The java.lang.Math") == []
      assert extract("hey are a bi person, my@sql") == []
      assert extract("PHP phper, Python pythonista") == ["PHP", "Python"]
      assert extract("Where old projects go to live out the rest of their days") == []

    def it_handles_set10() -> None:
      assert extract("I'm Julia, a marketing manager") == ["Julia"] # known FP
      assert extract("I learn Julia language") == ["Julia"]
      assert extract("developer:iOS,Robot,Fintech") == ["iOS"]
      assert extract("C Plus Plus programmar from India") == ["C++"]
      assert extract("hey are a bi person, my@sql") == []
      assert extract("PHP phper, Python pythonista") == ["PHP", "Python"]
      assert extract("Where old projects go to live out the rest of their days") == []

    def it_handles_set11() -> None:
      assert extract("Keen user of d3.js, and Raspberry Pi's.") == ["D3JS", "Raspberry-Pi"]
      assert extract("Arduino addict. Java programmer in real life") == ["Arduino", "Java"]
      assert extract("C#,C++,Firebase,Unity") == ["C#", "C++", "Google-Firebase", "Unity"]
      assert extract("R, Matlab, Tableau") == ["R", "Matlab", "Tableau"]
      assert extract("Pulumi, Kotlin, PowerShell | Postgres") == ["Pulumi", "Kotlin", "PowerShell", "PostgreSQL"]
      assert extract("MariaDB for backend | Scss for the FE") == ["MariaDB", "Backend", "SASS", "Frontend"]
      assert extract("To be or not to BE") == [] # no FP!

  def it_handles_set12() -> None:
    assert extract("ARM processors") == ["ARM"]
    assert extract("Hi, my name is Arm") == ["ARM"] # FP
    assert extract("My left arm is stronger than my right arm") == []
    assert extract("I’m doing high-performance computing work on CPU, including x86, arm.") == ["CPU", "x86", "ARM"]
    assert extract("Embrace AI-IoT | RISC-V | ARM | ARC") == ["AI", "IoT", "RISC", "ARM", "ARC"]
    assert extract("PERN afficianado") == ["PostgreSQL", "Express", "React", "NodeJS"]

  def it_handles_set13() -> None:
     assert extract("My favorite language is Jax") == []
     assert extract("My name is Jax") == []
     assert extract("Hi, I'm Jax, an avid computer sorcerer") == []
     assert extract("CUDA C++ , Pytorch RT, JAX(JIT,Haiku enjoyer, FLAX Flexer)") == ["CUDA", "C++", "PyTorch", "JAX", "Flax"]
     assert extract("JAX @NVIDIA") == ["JAX"]
     assert extract("Scientist @ JAX") == ["JAX"]
     assert extract("I like learning | JAX | Google Brain") == ["JAX", "Google"]
     assert extract("Software Engineer at Google DeepMind working on JAX/Flax") == ["Software", "Google", "JAX", "Flax"]
     assert extract("Jax + Haiku fan. Self-attention for the win") == [] # known FN
     assert extract("Julia, GraalVM, LLVM, NVidia, CNCF, Program Synthesis, 3D-QSAR") == ["Julia", "LLVM", "NVidia"]
     assert extract("Sample for UE5's CommonConversation Feature") == ["Unreal-Engine"]

  def it_handles_set14() -> None:
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

  def it_handles_set15() -> None:
    assert extract("Android(Kotlin) | iOS(Swift) | Spring Boot(Java) | Python(Django)") == [
      "Android", "Kotlin", "iOS", "Swift", "Spring", "Java", "Python", "Django"
    ]
    assert extract("ClickHouse, linux, perl, python, C++, kafka") == [
      "ClickHouse", "Linux", "Perl", "Python", "C++", "Apache-Kafka"
    ]
    assert extract("Software Eng @ClickHouse") == ["Software"]
