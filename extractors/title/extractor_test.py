from ..utils import fix_grammar, normalize, omit_parens
from .extractor import TitleExtractor, fix_more_grammar

categorizer = TitleExtractor()

def extract(text: str) -> str:
  ntext = omit_parens(fix_more_grammar(fix_grammar(normalize(text))))
  return categorizer.extract(ntext, category="HUMAN")

def describe_TitleExtractor() -> None:
  def describe_extract() -> None:
    def it_works() -> None:
      assert extract("A developer") == "Developer"
      assert extract("Django developer") == "Django Developer"
      assert extract("other remote Engineer") == "Other Remote Engineer"
      assert extract("I'm a junior PHP coder") == "Junior PHP Coder"
      assert extract("developer, engineer") == "Developer | Engineer"
      assert extract("developer and engineer") == "Developer | Engineer"
      assert extract("Developer | Engineer") == "Developer | Engineer"

    def it_handles_negation_indicators() -> None:
      assert extract("I am a web engineer") == "Web Engineer"
      assert extract("I am not a web engineer") == ""

    def it_handles_past_indicators() -> None:
      assert extract("A php engineer") == "Php Engineer"
      assert extract("A former php engineer") == ""
      assert extract("I am a php developer") == "Php Developer"
      assert extract("I was a php developer") == ""

    def it_handles_future_indicators() -> None:
      assert extract("I am a Laravel developer") == "Laravel Developer"
      assert extract("I will be a Laravel developer") == ""
      assert extract("I am going to be a Laravel developer") == ""
      assert extract("Carl is a striving Laravel developer") == ""
      assert extract("Future Laravel developer") == ""
      assert extract("Aspiring Laravel developer") == ""

    def it_handles_real_set1() -> None:
      assert extract("full-stack quantum chemist") == "Full-Stack Quantum Chemist"
      assert extract("Senior SWE, CS undergraduate") == "Senior SWE | CS Undergraduate"
      assert extract("Healthcare data analyst & freelancer") == "Healthcare Data Analyst | Freelancer"
      assert extract("Machine Learning Engineer (Remote Worker)") == "Machine Learning Engineer"
      assert extract("""
        IT CONSULTANT | REMOTE SENIOR JAVA SOFTWARE ENGINEER
      """) == "IT CONSULTANT | Remote SENIOR JAVA SOFTWARE ENGINEER"
      # ^ another Spacy bug, triggerd by REMOTE capitalization (workarounded in `fix_more_grammar`)

    def it_handles_real_set2() -> None:
      assert extract("""
        Head of Mobile, #Android, #Engineer, #Consultant, #Remote
      """) == "Head of Mobile | Engineer | Consultant"
      assert extract("CEO/co-founder of Tuple, a tool for remote pair programming") == "CEO / Co-Founder of Tuple"
      assert extract("CTO | Senior Systems Analyst | Hybrid Remote") == "CTO | Senior Systems Analyst"
      assert extract("Senior Android Developer(Looking for Remote Role)") == "Senior Android Developer"
      assert extract("""
        Full Stack Web Developer | Remote enthusiast | Associate
      """) == "Full Stack Web Developer | Remote Enthusiast"

    def it_handles_real_set3() -> None:
      assert extract("Professor, Remote Sensing") == "Professor"
      assert extract("""
        Digital Entrepreneur | Code Lover | Open for New Opportunities
      """) == "Digital Entrepreneur"
      assert extract("Student. Looking for internships.") == "Student"
      assert extract("Software Developer, seeking new employment possibilities") == "Software Developer"
      assert extract("Professional UI/UX Designer, I Am Ready for hire.") == "Professional UI/UX Designer"

    def it_handles_real_set4() -> None:
      assert extract("🏻 Web Developer | JS ❤ ~ Always open to learn") == "Web Developer"
      assert extract("""
        I'm a highly motivated Ninja. Always looking for new things to learn.
      """) == "Highly Motivated Ninja"
      assert extract("Freelance Programmer | Not for Hire") == "Freelance Programmer"
      assert extract("AI Thought Leader | Cognitive Architecture | Heuristic Imperatives") == "AI Thought Leader"
      assert extract("""
        Open Source Enthusiast, Project Leader @OWASP Chapter Leader @OWASP
      """) == "Open Source Enthusiast | Project Leader @OWASP Chapter Leader"

    def it_handles_real_set5() -> None:
      assert extract("""
        Mobile Platform Technical Leader - iOS Engineer
      """) == "Mobile Platform Technical Leader - iOS Engineer"
      assert extract("Designer Developer from Ireland") == "Designer Developer"
      assert extract("Captain leading from the front!") == ""
      assert extract("CTO at entro.solutions") == "CTO at Entro.Solutions" # Python `.title()` capitalizes like that :shrug:
      assert extract("Physics research head at nvidia") == "Physics Research Head at Nvidia"

    def it_handles_real_set7() -> None:
      assert extract("""
        Author of Head First Ruby and Head First Go, published by O'Reilly Media.
      """) == "Author of Head First Ruby"
      assert extract("""
        Web (php) engineer and entrepreneur caring about the quality
      """) == "Web Engineer | Entrepreneur"
      assert extract("""
        Cloud, DB and Security analyst.
      """) == "DB and Security Analyst"
      assert extract("""
        VP Eng. at MedScout, storyteller, student of disasters.
      """) == "VP Eng at MedScout | Student of Disasters"
      assert extract("""
        Healthcare data analyst freelancer
      """) == "Healthcare Data Analyst Freelancer"

    def it_handles_real_set8() -> None:
      assert extract("PHP phper, Python pythonista") == "PHP Phper | Python Pythonista"
      assert extract("Head of Decentralized Identity @ Block, Inc.") == "Head of Decentralized Identity"
      assert extract("""
        Campaign Lead, Data Scientist, Statistician
      """) == "Campaign Lead | Data Scientist | Statistician"
      assert extract("""
        Student of secondary programming technical school in Poland
      """) == "Student of Secondary Programming Technical School"
      assert extract("Head of Software at Krystal") == "Head of Software at Krystal"

    def it_handles_real_set9() -> None:
      assert extract("ex-game developer") == ""
      assert extract("Computational Game Theory Researcher") == "Computational Game Theory Researcher"
      assert extract("SQL Server/Cloud DBA") == "SQL Server/Cloud DBA"
      assert extract("Aspiring Machine Learning / Data Engineer") == ""
      assert extract("""
        Programmer, cybersecurity expert, and 2017 penetration tester
      """) == "Programmer | Cybersecurity Expert | 2017 Penetration Tester"

    def it_handles_real_set10() -> None:
      assert extract("""
        Frontend Consultant; Web, Mobile and Desktop Applications Developer
      """) == "Frontend Consultant | Web, Mobile and Desktop Applications Developer"
      assert extract("""
        Full-stack web developer and Zend Certified PHP Engineer
      """) == "Full-Stack Web Developer | Zend Certified PHP Engineer"
      assert extract("""
        Founder & CEO @QualiSage | Team Lead | Senior Full-Stack Developer | 10+ Years
      """) == "Founder | CEO | Team Lead"
      assert extract("""
        Software generalist, father of two
      """) == "Software Generalist"
      assert extract("""
        Arduino addict. Java programmer in real life
      """) == "Java Programmer"

    def it_handles_real_set11() -> None:
      assert extract("""
        3D game engine development amateur
      """) == "Game Engine Development Amateur"
      assert extract("""
        Game Developer, Programmer, Bit of an Artist; C++, Unreal
      """) == "Game Developer | Programmer"
      assert extract("Retired backend engineer") == ""
      assert extract("""
        Retired backend engineer. Now an educator.
      """) == "Educator"
      assert extract("""
        Full stack software engineer. Freelance. Some time ago: CTO & co-founder at Nightset
      """) == "Full Stack Software Engineer" # CTO & Co-Founder at Nightset

    def it_handles_real_set12() -> None:
      assert extract("Salesforce Guru") == "Salesforce Guru"
      assert extract("Great Learning is an online learning platform designed to...") == ""
      assert extract("the Learning&Training Hub of OS Kernel for Students & Developers") == ""
      assert extract("Bachelor of Comp Sci student @ Concordia University") == "Bachelor of Comp Sci Student"
      assert extract("Working as a Technical Recruiter!") == "Technical Recruiter"

    def it_handles_real_set13() -> None:
      assert extract("""
        CS-sophomore | Game-dev (Unity & C#)
      """) == "CS-Sophomore | Game-Dev"
      assert extract("""
        Freelance Programmer | Not for Hire
      """) == "Freelance Programmer"
      assert extract("""
        Computer science newbie
      """) == "Computer Science Newbie"
      assert extract("""
        CMC MSU bachelor's degree, FCS HSE master student, ex-Data Scientist at Tinkoff bank
      """) == "CMC MSU Bachelor | FCS HSE Master Student"
      assert extract("Hello. I'am Vadim Tikhonov. I study code, data analysis and data science.") == ""

    def it_handles_real_set14() -> None:
      assert extract("""
        I'm a Professional C++ Game and Software Developer from New York.
      """) == "Professional C++ Game and Software Developer"
      assert extract("""
        Father, hacker, blogger, gamer, & nerd. Bounty Hunter
      """) == "Hacker"
      assert extract("""
        iOS/SwiftUI developer and UI/UX designer
      """) == "iOS/SwiftUI Developer | UI/UX Designer"
      assert extract("""
        Ph.D. candidate, interested in software security
      """) == "Ph.D Candidate"
      assert extract("""
        Self-employed web engineer #Rust #Wasm #Go #TypeScript #React #REST
      """) == "Self-Employed Web Engineer"

    def it_handles_real_set15() -> None:
      assert extract("Currently studying React Ecosystem") == ""
      assert extract("""
        Blockchain developer, bulding for DeFi.
      """) == "Blockchain Developer"
      assert extract("""
        Environmental student, Unreal Engine developer
      """) == "Environmental Student | Unreal Engine Developer"
      assert extract("""
        CS Undergrad at New Jersey Institute of Technology
      """) == "CS Undergrad at New Jersey Institute"
      assert extract("""
        Arman is a full-stack developer who mainly focuses on web development
      """) == "Full-Stack Developer"

    def it_handles_real_set16() -> None:
      assert extract("""
        Software Engineer, Tech Lead in Rust, WASM, TypeScript
      """) == "Software Engineer | Tech Lead"
      assert extract("""
        Head of web engineering at Temporalio.
      """) == "Head of Web Engineering at Temporalio"
      assert extract("ex-lead of GitHub QA team") == ""
      assert extract("A strong conceptual thinker and a constant student") == ""
      assert extract("""
        I am Viktor Klang, a finder, researcher, problem solver, improver of things,
        life-long student, developer/programmer, leader, mentor/advisor, public speaker…
      """) == "Researcher | Student, Developer | Leader"
      # ^ known issue, caused by Spacy wrong dep. parsing

    def it_handles_real_set17() -> None:
      assert extract("""
        Head of foreign Dev Relations at DXOS.org
      """) == "Head of Foreign Dev Relations"
      # ^ "at DXOS.org" is lost due wrong dep. detection by Scrapy ("at" heads to "Relations" instead of "Head")
      assert extract("Software Engineer, I was Head of Tech of Shinobi Team") == ""
      # ^ "Software Engineer" heads to "was", likely a Spacy mistake
      assert extract("""
        I'm a JS / TS specialist focused on web and game development
      """) == "JS / TS Specialist"
      assert extract("""
        I am a data scientist with a passion for learning
      """) == "Data Scientist"
      assert extract("Business Analyst | MBA Student") == "Business Analyst | MBA Student"

    def it_handles_real_set18() -> None:
      assert extract("""
        21 year old embedded systems electronics engineer.
      """) == "21 Year Old Embedded Systems Electronics Engineer"
      assert extract("Studying to become a therapist.") == ""
      assert extract("""
        Game Producer & Lead Development | Network & Systems Admin
      """) == "Game Producer | Systems Admin"
      assert extract("""
        Game developer from New Orlean
      """) == "Game Developer"
      assert extract("""
        freelance math teacher, freelance front-end developer
      """) == "Freelance Math Teacher | Freelance Front-End Developer"

    def it_handles_real_set19() -> None:
      assert extract("""
        Founder and CEO of @rangle , the leading lean/agile JavaScript consulting firm.
      """) == "Founder and CEO of @Rangle"
      assert extract("""
        Mobile Apps & Web Developer | Freelancer | Ready for Hire
      """) == "Web Developer | Freelancer"
      assert extract("""
        Computer science student with an interest in data science.
      """) == "Computer Science Student"
      assert extract("""
        A student of life, working as a QA at a Bay Area
      """) == "QA at a Bay Area"
      assert extract("Former CEO/co-founder of Tuple, a tool for remote pair programming") == "CEO"
      # ^ known bug caused by Spacy

    def it_handles_real_set20() -> None:
      assert extract("""
        Frontend dev by day, backend student by night
      """) == "Frontend Dev | Backend Student"
      assert extract("""
        a Microsoft Technical Trainer specializing in Data & AI
      """) == "Microsoft Technical Trainer"
      assert extract("""
        ex-Facebook BFDL. Now tech-lead at @AWS
      """) == "Tech-Lead at @AWS"
      assert extract("""
        Technical Artist. Founder of @Golden-Ram-Studio
      """) == "Technical Artist | Founder of @Golden-Ram-Studio"
      assert extract("""
        My name is Devin and I am a Senior Gameplay Designer at
        CD Projekt Red working on the next Witcher.
      """) == "Senior Gameplay Designer at CD Projekt Red"

    def it_handles_real_set21() -> None:
      assert extract("""
        Technology leader at Gartner (Managing Vice President).
        Graduate student at University of Illinois getting my MBA. Forever an engineer.
      """) == "Technology Leader at Gartner | Graduate Student at University"
      assert extract("""
        Computer science masters graduate with a specialization in Data Science.  
      """) == "Computer Science Masters Graduate"
      assert extract("""
        ⭐️ Senior Software Developer ⭐️ Blockchain / Backend / ETL  
      """) == "Senior Software Developer"

# On a mission to help every student to reach their potential with technologies - FP, discard dep:nsubj?
# TOGAF 9 Certified Enterprise Architect, Pragmatist, Economic Student, Biker,
# senior software engineer at @pagarme | Computer Science undergraduate at Pontifical Catholic University of Paraná
# "CS PhD student at Stony Brook University, new to Distributed System."
# "Website Developer and Software Developer with a Bachelor of Science in Informatics."
#
#       def it_handles_mixed13() -> None:
#         assert cats("""
#           Frontend + DevOp! web3 / DeFi, TypeScript, React/Next/Nest, ex. freelancer
#         """) == Cats("Dev", is_freelancer=False)
#         assert cats("Ex-engineer, freelancer") == Cats(is_freelancer=True)
#         assert cats("Ex freelancer at Bay, forever student") == Cats(is_freelancer=False)
#
#       def it_handles_mixed16() -> None:
#         assert cats("I want to be a data analyst").role == "Student"
#         assert cats("I want to become a computer scientist").role == "Student"
#         assert cats("Computer Science Major at NAU").role == "Student"
#         assert cats("Computer science major at Stockton university").role == "Student"
#
#       def it_handles_set17() -> None:
#         assert cats("Just a beginner").role == "Student"
#         assert cats("Mobile novice").role == "Student"
#         assert cats("Blockchain noob").role == "Student"
#         assert cats("A 2nd year studxnt of the Higher IT School.").role is None
#         assert cats("Currently looking for an ML internship").role == "Student"
#
#       def it_handles_set20() -> None:
#         assert cats("""
#           Master of Science in Information Systems student at Stevens Institute of Technology, NJ, USA.
#         assert cats("Full time Architect, Consultant, Learner, Author").role == "Dev"
#         """) == Cats("Student")
#
#       def it_handles_set21() -> None:
#         assert cats("Software Developer learning Systems Analysis and Development.").role == "Dev"
#         assert cats("Software engineer studying mathematics").role == "Dev"
#         assert cats("Aspiring engineer studying networking & security.").role == "Student"
#         # ^ OK "aspiring" cancels "engineer", then "studying" is captured
#         # assert is_student("Aspiring 16 y/o software engineer studying networking & security.")
#         # ^ Spacy model fails to parse such a long noun phrase properly, needs to be retrained
#         assert cats("iOS architect, studying Rust").role == "Dev"
#         assert cats("Frontend dev who currently learning Rust & Elixir").role == "Dev"
#         assert cats("Teenager, freelancer, backend developer (TypeScript, C++)") == Cats(
#           "Student", is_freelancer = True
#         )
#
#       def it_handles_set24() -> None:
#         assert cats("""
#           Specializing generalist. CS PhD, student of life. Lover of words and hyperbole. Remote.
#         """) == Cats("Dev", is_remote=True)
#         assert cats("music student java elasticsearch ai subversion git node").role == "Student"
#         assert cats("Back-End Developer | Information Systems bachelor").role == "Dev"
#
#       def it_handles_set25() -> None:
#         assert cats("Biotech student and sometimes software developer.").role == "Student"
#         assert cats("Software developer and sometimes biotech student.").role == "Dev"
#         assert cats("Everlasting student · Freelance · Life lover") == Cats(is_freelancer=True)
#         assert cats("rookie front-end developer").role == "Student"
#         assert cats("""
#           Professor of the Practice in Computer Science, Program Director
#           for the Fundamentals of Computing Undergraduate Certificate Program
#         """).role == "Nondev"
#
#       def it_handles_set26() -> None:
#         assert cats("""
#           NET Developer with front-end skills, Freelancer, Photographer and Science Lover
#         """) == Cats("Dev", is_freelancer=True)
#         assert cats("""
#           Teenager, freelancer, backend developer (TypeScript, C++17)
#         """) == Cats("Student", is_freelancer=True)
#         assert cats("Oleg Rybnikov - a freelancing web artisan specializing in Vite").is_freelancer
#         assert cats("#backend #java #freelancer").is_freelancer
#
#       def it_handles_set27() -> None:
#         assert cats("""
#           applied artificial intelligence student, free to relocate
#         """) == Cats("Student")
#         assert cats("""
#           🇸🇰 Freelancer full-stack developer. #React #ReactNative
#         """) == Cats("Dev", is_freelancer=True)
#         assert cats("""
#           Full stack software engineer at dextra | Freelancer
#         """) == Cats("Dev", is_freelancer=True)
#         assert cats("""
#           Self-taught Developer graded in Back-end Development. -Freelancer
#         """) == Cats("Dev", is_freelancer=True)
#
#       def it_handles_set28() -> None:
#         assert cats("indie dev • iOS & macOS • freelance") == Cats("Dev", is_freelancer=True)
#         assert cats("Freelancer Jedi Padawan") == Cats(is_freelancer=True)
#         assert cats("I'm a Software Engineer, Ethical Hacker, and security enthusiast") == Cats("Dev")
#
#       def it_handles_set29() -> None:
#         assert cats("Gopher. Former TL of Go CDK and author of Wire.") == Cats("Dev", is_lead=False)
#         assert cats("TL, JavaScript Developer") == Cats("Dev", is_lead=True)
#         assert cats("CTO, TL") == Cats("Nondev", is_lead=True)
#         assert cats("Typographer, Tech Lead") == Cats(is_lead=True)
#         assert cats("TL;DR : DJ turned software engineer") == Cats("Dev")
#         assert cats("Founder and SVP Creative at Frac.tl") == Cats("Nondev")
#         assert cats("Senior Site Reliability Engineer, TL") == Cats("Dev", is_lead=True)
#         assert cats("Solidity developer with 10+ years experience. CTO at entro.solutions").role == "Dev"
#         assert cats("company founder at 18yo, programmer, game developer, VR enthusiast").role == "Nondev"
#         assert cats("Fullstack web design agency").role == "Org"
#
#       def it_handles_set32() -> None:
#         assert cats("AWESOME Developer/Lead") == Cats("Dev", is_lead=True)
#         assert cats("Software Dev & Tech Lead") == Cats("Dev", is_lead=True)
#         assert cats("Lead Cloud Engineer @ Namecheap") == Cats("Dev", is_lead=True)
#         assert cats("Horizon 2020 Project LEAD: Low-Emission logistics") == Cats(is_lead=True)
#         assert cats("Technical Content Lead") == Cats(is_lead=True)
#         assert cats("IT Sec guy, @zaproxy co-lead") == Cats("Dev", is_lead=True)
#         assert cats("Raising the bar for leadership in tech.") == Cats(is_lead=True)
#         assert cats("The leading platform for local cloud development") == Cats("Org")
#
#       def it_handles_set34() -> None:
#         assert cats("Junior Programmer @BohemiaInteractive | Founder @QX-Interactive") == Cats("Dev")
#         assert cats("""
#           "Striving to become a front-end developer. Formerly climbing gym founder and co-owner"
#         """).role == "Student"
#         assert cats("""
#           Founder, CBB Analytics. Sports Data Scientist and Web Developer.
#         """).role == "Nondev"
#         assert cats("""
#           Twas brillig, and the slithy toves
#           Did gyre and gimble in the wabe
#         """).role is None
#
#       def it_handles_set37() -> None:
#         assert cats("Head of Design @github.").role == "Nondev"
#         assert cats("Associate Professor of CS at Augusta University.").role == "Nondev"
#         assert cats("Head of developer advocacy @pieces-app").role == "Nondev"
#         assert cats("permanent head damage").role is None
#         assert cats("Code samples from the book Head First Go").role is None
#         assert cats("Growth Head").role == "Nondev"
#         assert cats("Head Coach @nashville-software-school").role == "Nondev"
#         assert cats("Head of Engineering @gigs").role == "Nondev"
#         assert cats("Head of OSS @huggingface. Open Source developer.").role == "Nondev"
#         assert cats("MY HEAD IS IN THE CLOUD!!").role is None
#         assert cats("Head of India @lendsmartlabs").role == "Nondev"
#         assert cats("Head of Technology").role == "Nondev"
#         assert cats("Head down and build").role is None
#         assert cats("Head Of Security Research @F5Networks").role == "Nondev"
#         assert cats("Head of Flickr.").role == "Nondev"
#
#       def it_handles_set39() -> None:
#         assert cats("Freelancer and video editor").is_freelancer
#         assert cats("Full stack developer, tech consultant").is_freelancer
#         assert cats("Backend SWE & consulting").is_freelancer
#         assert cats("Java Full-stack Developer at j-labs.pl Crif consultant").is_freelancer
#         assert cats("Front-end & WordPress developer, UX consultant. Making stuff for the web since 2005").is_freelancer
#
#       def it_handles_set40() -> None:
#         assert cats("My name is Jorens, I'm a Full Stack developer, currently freelancing").is_freelancer
#         assert cats("WebGL, WebXR, full-stack, consulting").is_freelancer
#         assert cats("Full-stack junior software developer, system administrator and IT consultant.").is_freelancer
#         assert cats("I have transformed years of freelancing into a full-time career").is_freelancer
#         assert cats("Something @ devlance").is_freelancer is None
#
#       def it_handles_set41() -> None:
#         assert cats("Freelancer Nasim is a Web Application Developer.").is_freelancer
#         assert cats("Opensource enthusiast, Skillbox teacher, Blogger").is_freelancer is None
#         assert cats("Free-lancer @ BYTESADMIN • Security Researcher").is_freelancer
#         assert cats("Freelance Clojure programmer").is_freelancer
#         assert cats("Freelance ⠁⣿⣿ ⣿⣿⣿ ⣿⣿⣿").is_freelancer
#         assert cats("Weblancer").is_freelancer is None
#
#       def it_handles_set43() -> None:
#         assert cats("👨 tech enthusiast / applied ai student").role == "Student"
#         assert cats("A Ph.D. student in statistical science.").role == "Student"
#         assert cats("PhD student at MIT Brain and Cognitive Sciences").role == "Student"
#
#       def it_handles_set44() -> None:
#         assert cats("Postgraduate student at Lund University.").role == "Student"
#         assert cats("Student of Chinese medicine, dance teacher, rare soul & funk music digger").role == "Student"
#         assert cats("Graduate Diploma in IT graduate with an undergraduate degree in Bachelor of Laws").role == "Student"
#         assert cats("I engineer 'learn by doing' experiences for uni students with lean...").role == "Dev"
#
#       def it_handles_set45() -> None:
#         assert cats("My name is Harold Bogg, I am a college student").role == "Student"
#         assert cats("Vice Dean for Undergraduate Studies").role == "Nondev"
#         assert cats("My name is Josh Student").role == "Student"
#         # ^ known false positive. Can't fix due to Spacy model limitations,
#
#       def it_handles_mixed51() -> None:
#         assert cats("""
#           👨‍💻 developer of 🌐 coora-ai.com 🧭 igapo.xyz / tech enthusiast / applied artificial intelligence student
#         """) == Cats("Dev")
#         assert cats("""
#           Technology entrepreneur, sports lover, network security student.
#         """) == Cats("Nondev")
#
#       def it_handles_mixed52() -> None:
#         assert cats("""
#           Technology entrepreneur, sports lover, network security student.
#         """) == Cats("Nondev")
#
#       def it_handles_mixed53() -> None:
#         assert cats("""
#           On a mission to help every student to reach their potential with technologies")
#         """) == Cats("Student") # known issue
#         assert cats("""
#           TOGAF 9 Certified Enterprise Architect, Pragmatist, Economic Student, Biker,
#         """) == Cats("Dev")
#         assert cats("""
#           Currently a Computer Science graduate student at University
#           of the Philippines Diliman working on quantum algorithms.
#         """) == Cats("Student")
#         assert cats("""
#           Over 30 years of experience working with diverse teams of researchers and
#           students developing interactive software and hardware for science inquiry.
#         """) == Cats("Dev") # because of "developing"
#         assert cats("""
#           B.Sc. in C.S. and M.Eng. student at the University of Bologna.
#         """) == Cats("Student")
#
#       def it_handles_mixed54() -> None:
#         assert cats("""
#           Software engineer at @GRID-is. Fellow of the Royal Geographical Society.
#           Postgraduate student at Lund University.
#         """) == Cats("Dev")
#         assert cats("""
#           Lead AI/ML Engineer at MITRE. Graduate student in Statistics at George Mason University.
#           Officer emeritus of @srct, @gmuthetatau, @masonlug
#         """) == Cats("Dev", is_lead=True)
#         assert cats("""
#           Developer at Sky and undergraduated in C.S. in Federal University of South Frontier
#         """) == Cats("Dev")
#         assert cats("""
#           Undergraduate studying 'Software and Information Engineering' at the Vienna University of Technology
#         """) == Cats("Student")
#         assert cats("""
#           Junior UI Designer @ Section BFA Design Art Undergraduate from NTU ADM, Singapore
#         """) == Cats("Nondev")
#
#       def it_handles_mixed55() -> None:
#         assert cats("""
#           Senior Software Engineer at @pagarme | Computer Science undergraduate at Pontifical Catholic University of Paraná
#         """) == Cats("Dev")
#         assert cats("""
#           Full-time software developer and student. Spare-time Japan fan and gamer
#         """) == Cats("Dev")
#

# TODO test:
# - [Dev/Sys/Net]Ops
# - NLP & ML Sys & ML Ops
# - {net | dev | sys} ops
# - ML Engineer / Dev Ops / ML Ops / sys admin
# - dev/sec/sys ops
# - Tech Infra - DevOps - DC ops - Sys Adm
# - Sys/Net/K8S Admin, Developper and Dev/Cloud OPS.
# - Self-taught Dev/Sys/Ops. K8S lover !
# - Cloud Consultant | MCT | Azure | Security | DevOps | Agile
# - SYS-OPS-NET-DEV
# - /^(?:Sys|Net)?(?(?<=Net)Sys|Net)?(?:Admin|(?:Dev)?Ops)$
# - Sys...Ops!
# - Software developer, currently using Go language, VS Code, Linux, Windows for Cloud based sys-ops and performance measurement applications.
# - Front-end Developer { Html/CSS/SCSS/JS.} Part-Time Back-end Developer {Python Django.} IT-Ops / Sys-Admin CCNA MCSA LFCA.
