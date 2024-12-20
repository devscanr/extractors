from dataclasses import dataclass
from ..utils import fix_grammar, normalize
from .extractor import Categorized, CategoryExtractor, Role

categorizer = CategoryExtractor("en_core_web_sm")

@dataclass
class Cats(Categorized):
  role: Role | None = None
  is_freelancer: bool | None = None
  is_lead: bool | None = None
  is_remote: bool | None = None
  is_hireable: bool | None = None

def cats(text: str) -> Cats:
  cs = categorizer.extract(fix_grammar(normalize(text)))
  return Cats(
    role = cs.role,
    is_freelancer = cs.is_freelancer,
    is_lead = cs.is_lead,
    is_remote = cs.is_remote,
    is_hireable = cs.is_hireable
  )

def describe_Categorizer() -> None:
  def describe_extract() -> None:
    def it_works() -> None:
      assert cats("I'm a someone") == Cats()
      assert cats("I'm a student and a freelancer") == Cats("Student", is_freelancer=True)
      assert cats("I'm a lead engineer") == Cats("Dev", is_lead=True)
      assert cats("I'm a freelance manager") == Cats("Nondev", is_freelancer=True)
      assert cats("I'm an engineer and an MBA graduate") == Cats("Dev")
      assert cats("I'm a MIT graduate, soon to become an engineer") == Cats("Student")
      assert cats("I'm a freelance developer") == Cats("Dev", is_freelancer=True)
      # Testing overlaps:
      assert cats("I'm a Dev") == Cats("Dev")
      assert cats("I'm an Ops") == Cats("Dev")
      assert cats("I'm an dev ops") == Cats("Dev")
      assert cats("I'm an devops") == Cats("Dev")

    def describe_is_remote() -> None:
      def it_handles_is_remote_1() -> None:
        assert cats("Remote Software Engineer").is_remote == True
        assert cats("Machine Learning Engineer (Remote Worker)").is_remote == True
        assert cats("Looking for opportunities in remote startup").is_remote == True
        assert cats("work with remote sensing and photogrametry and GIS").is_remote is None
        assert cats("Professor, Remote Sensing").is_remote is None
        assert cats("Collaborative, remote project practice for early career developers").is_remote is None

      def it_handles_is_remote_2() -> None:
        assert cats("in search of a remote job").is_remote == True
        assert cats("remote job seeking...").is_remote == True
        assert cats("Android developer; remote worker. Based in Scotland").is_remote == True
        assert cats("Teaching code remote").is_remote == True
        assert cats("Writing code remotely").is_remote == True

      def it_handles_is_remote_3() -> None:
        assert cats("Accept Freelancer. Remote only!").is_remote == True
        assert cats("PHP & Laravel Developer. Open to remote.").is_remote == True
        assert cats("Remote Fullstack Software Engineer").is_remote == True
        assert cats("A list of semi to fully remote-friendly companies in tech").is_remote == True
        assert cats("The future of tech is Remote.").is_remote == True

      def it_handles_is_remote_4() -> None:
        assert cats("Remote Software Engineer @ Resilience").is_remote == True
        assert cats("Software Engineer | Flutter Developer | IoT Researcher | Open for Remote Job").is_remote == True
        assert cats("iOS Developer | Remote").is_remote == True
        assert cats("17yo dev; @dotcute & @remote-kakao").is_remote is None
        assert cats("# FE Engineer @ remote.com Prev: Panalyt.com").is_remote is None
        assert cats("EE,PhD,Remote Sensing and GIS developer").is_remote is None

      def it_handles_is_remote_5() -> None:
        assert cats("baby girl's father. Looking for a remote work opportunity").is_remote == True
        assert cats("remote haskell developer").is_remote == True
        assert cats("Blockchain Developer Remote/Online").is_remote == True
        assert cats("Remote @ShadowShahriar").is_remote is None
        assert cats("Hacker. Pioneered BlindXSS, Remote git/hg/bzr Pillaging").is_remote is None
        assert cats("0fficial_BlackHat13 Remote_Code_Execution 0day Exploit").is_remote is None

      def it_handles_is_remote_6() -> None:
        assert cats("With great responsibility comes great power | Remote working").is_remote == True
        assert cats("Head of Mobile, #Android, #Engineer, #CS, #GO, #Consultant, #Remote").is_remote == True
        assert cats("IT CONSULTANT | REMOTE SENIOR JAVA SOFTWARE ENGINEER").is_remote == True
        assert cats("CEO/co-founder of Tuple, a tool for remote pair programming").is_remote is None
        assert cats("Principal Engineer working on remote management software").is_remote is None

      def it_handles_is_remote_7() -> None:
        assert cats("CTO | Senior Systems Analyst | Hybrid Remote").is_remote == True
        assert cats("Did learn coding remotely. Now Looking for a remote job").is_remote == True
        assert cats("Remote access everywhere").is_remote is None
        assert cats("Access remotely everywhere").is_remote is None

      def it_handles_is_remote_8() -> None:
        assert cats("Remote. Building stuff with Typescript, Lua, and Swift.").is_remote
        assert cats("Remote iOS Developer").is_remote
        assert cats("Senior Android Developer(Looking for Remote Role)").is_remote
        assert cats("Remote tech").is_remote is None
        assert cats("Remotely possible").is_remote is None

      def it_handles_is_remote_9() -> None:
        assert cats("Full Stack Web Developer | Remote enthusiast | Associate").is_remote
        assert cats("Software Developer, React JS lover. Looking for new challenges in remote projects.").is_remote
        assert cats("Want to join a remote project.").is_remote
        assert cats("Wish to lead a remote position.").is_remote

      def it_handles_is_remote_10() -> None:
        assert cats("Remote Software Engineer").is_remote
        assert cats("Machine Learning Engineer (Remote Worker)").is_remote
        assert cats("Looking for opportunities in remote startup").is_remote
        assert cats("work with remote sensing and photogrametry and GIS").is_remote is None
        assert cats("Professor, Remote Sensing").is_remote is None
        assert cats("Collaborative, remote project practice for early career developers").is_remote is None

      def it_handles_is_remote_11() -> None:
        assert cats("in search of a remote job").is_remote
        assert cats("remote job seeking...").is_remote
        assert cats("Android developer; remote worker. Based in Scotland").is_remote
        assert cats("Teaching code remote").is_remote
        assert cats("Writing code remotely").is_remote

    def describe_is_hireable() -> None:
      def it_handles_is_hireable_1() -> None:
        assert cats("Open for new opportunities").is_hireable == True
        assert cats("Open for hiring").is_hireable == True
        assert cats("Hireable").is_hireable == True
        assert cats("#Hireable").is_hireable == True
        assert cats("Open to work").is_hireable == True
        assert cats("=OpenToWork=").is_hireable == True
        assert cats("Not open for new opportunities").is_hireable == False
        assert cats("Not hireable").is_hireable == False
        assert cats("Not #Hireable").is_hireable == True # by design
        assert cats("Not open to work").is_hireable == False
        assert cats("Foo bar open").is_hireable is None

      def it_handles_is_hireable_2() -> None:
        assert cats("Blah. Hireable. Blah").is_hireable == True
        assert cats("I'm hireable").is_hireable == True
        assert cats("She is hireable").is_hireable == True
        assert cats("hire-able").is_hireable == True
        assert cats("not hire able").is_hireable == False
        assert cats("This tool is to make everyone hireable").is_hireable == True # known FP

      def it_handles_is_hireable_3() -> None:
        assert cats("open to future challenges").is_hireable == True
        assert cats("not open to future challenges").is_hireable == False
        assert cats("always open to work").is_hireable == True
        assert cats("not open to work").is_hireable == False
        assert cats("open for hire").is_hireable == True
        assert cats("not open for hire").is_hireable == False

      def it_handles_is_hireable_4() -> None:
        assert cats("hire-able").is_hireable == True
        assert cats("not hire able").is_hireable == False
        assert cats("This tool is to make everyone hireable").is_hireable == True # known FP
        assert cats("Open to hiring").is_hireable == True
        assert cats("Open to new ideas").is_hireable == True
        assert cats("Open to job offers").is_hireable == True
        assert cats("Open to work proposal").is_hireable == True
        assert cats("Open to proposals").is_hireable == True
        assert cats("Open to something").is_hireable is None

      def it_handles_is_hireable_5() -> None:
        assert cats("Open to opportunities").is_hireable == True
        assert cats("Open to new opportunities").is_hireable == True
        assert cats("Open for interesting opportunities").is_hireable == True
        assert cats("Open to collaborations").is_hireable == True
        assert cats("Open to future challenges").is_hireable == True
        assert cats("Open to future enquiries").is_hireable == True
        assert cats("Open for professional project enquiry").is_hireable == True
        assert cats("Currently open to an opportunity").is_hireable == True
        assert cats("Currently not open to an opportunity").is_hireable == False

      def it_handles_is_hireable_6() -> None:
        assert cats("ready to be hired").is_hireable == True
        assert cats("not ready to be hired").is_hireable == False
        assert cats("She is hireable").is_hireable == True
        assert cats("She is not hireable").is_hireable == False
        assert cats("Open for relocation").is_hireable == True
        assert cats("Open for something").is_hireable is None
        assert cats("Not open for relocation").is_hireable == False
        assert cats("Open to internship and job").is_hireable == True

      def it_handles_is_hireable_7() -> None:
        assert cats("#hireme").is_hireable == True
        assert cats("please hire me").is_hireable == True
        assert cats("Interested in hiring me?").is_hireable == True
        assert cats("Whether you hire me or not, I am overly committed").is_hireable == True

      def it_handles_is_hireable_8() -> None:
        assert cats("Seeking new job opportunities").is_hireable == True
        assert cats("Seeking new work possibilities").is_hireable == True
        assert cats("Seeking well paid job options").is_hireable == True
        assert cats("not seeking a job").is_hireable == False
        assert cats("not seeking an work").is_hireable == False
        assert cats("not seeking anything").is_hireable is None

      def it_handles_is_hireable_9() -> None:
        assert cats("looking for job opportunities").is_hireable == True
        assert cats("looking for new options").is_hireable == True
        assert cats("looking for a position").is_hireable == True
        assert cats("not looking for opportunities").is_hireable == False
        assert cats("looking for something").is_hireable is None

      def it_handles_is_hireable_10() -> None:
        assert cats("looking for job opportunities").is_hireable == True
        assert cats("looking for new options").is_hireable == True
        assert cats("looking for a position").is_hireable == True
        assert cats("Looking for a job now.").is_hireable == True
        assert cats("not looking for opportunities").is_hireable == False
        assert cats("looking for something").is_hireable is None

      def it_handles_is_hireable_11() -> None:
        assert cats("jobseeker").is_hireable == True
        assert cats("job seeker").is_hireable == True
        assert cats("job-seeker").is_hireable == True
        assert cats("jobseeking").is_hireable == True
        assert cats("job seeking").is_hireable == True
        assert cats("job-seeking").is_hireable == True
        assert cats("not jobseeker").is_hireable == False
        assert cats("not a job seeker").is_hireable == False
        assert cats("not a job-seeker").is_hireable == False
        assert cats("not jobseeking").is_hireable == False
        assert cats("not job seeking").is_hireable == False
        assert cats("not job-seeking").is_hireable == False

      def it_handles_is_hireable_21() -> None:
        assert cats("Open to AI/ML Roles").is_hireable == True
        assert cats("Open to a leadership role").is_hireable == True
        assert cats("JS, React, Angular; open to relocation").is_hireable == True
        assert cats("Open to new challenges💻").is_hireable == True
        assert cats("looking for job options intern etc.").is_hireable == True
        assert cats("Digital Entrepreneur | Code Lover | Open for New Opportunities").is_hireable == True
        assert cats("Open for Hire - Full-Stack Software Developer | building railsinit.org").is_hireable == True

      def it_handles_is_hireable_22() -> None:
        assert cats("you can hire me if you want").is_hireable == True
        assert cats("Software Developer, seeking new employment possibilities").is_hireable == True
        assert cats("Seeking challenging employment opportunities").is_hireable == True
        assert cats("Looking for new #rstats opportunities").is_hireable == True
        assert cats("Student. Looking for internships.").is_hireable == True

      def it_handles_is_hireable_23() -> None:
        assert cats("Computer Engineer. Seeking remote contract work.").is_hireable == True
        assert cats("Web developer. Always seeking contract work. Available via Telegram").is_hireable == True
        assert cats("Professional UI/UX Designer, I Am Ready for hire.").is_hireable == True
        assert cats("Mobile Apps & Web Developer | Freelancer | Ready for Hire").is_hireable == True
        assert cats("Don't try to hire me").is_hireable == False
        assert cats("You can not hire me.").is_hireable == False

      def it_handles_is_hireable_24() -> None:
        assert cats("See this: I AM NOT HIREABLE").is_hireable == False
        assert cats("If you enjoy my open source work...").is_hireable is None
        assert cats("Open to interpretation").is_hireable is None
        assert cats("An open source ecosystem to liberate the work").is_hireable is None
        assert cats("A tool to hire best developers. Myself included ;").is_hireable is None
        assert cats("🚀Open To You! 🚀").is_hireable is None

      def it_handles_is_hireable_25() -> None:
        assert cats("I am non hireable").is_hireable == False
        assert cats("always seeking for a job").is_hireable == True
        assert cats("Open to Organizations !").is_hireable is None
        assert cats("🈺 open for business! 🈺").is_hireable is None
        assert cats("🏻 Web Developer | JS ❤ ~ Always open to learn").is_hireable is None
        assert cats("Connect the world of science. Make research open to all.").is_hireable is None
        assert cats("Looking for teleportation").is_hireable is None

      def it_handles_is_hireable_26() -> None:
        assert cats("What are you looking for and what am I looking for?").is_hireable is None
        assert cats("Looking for the next big thing.").is_hireable is None
        assert cats("I'm looking for: Ruby Ninjas,Ember.js Masters, Python Dev, QAs ...if you're one of them, just let me know!").is_hireable is None
        assert cats("I'm a highly motivated Ninja. Always looking for new things to learn.").is_hireable is None

      def it_handles_is_hireable_27() -> None:
        assert cats("Just for fun. Not hirable.").is_hireable == False
        assert cats("I'm not for hire. Thank you for your cooperation").is_hireable == False
        assert cats("Freelance Programmer | Not for Hire").is_hireable == False
        assert cats("@ zhakky studios not hire able.").is_hireable == False
        assert cats("Looking for a PhD position!").is_hireable == True
        assert cats("Working on VR Game w/kobugindustries (Not an expert) NOT FOR HIRE").is_hireable == False

    def describe_is_lead() -> None:
      def it_handles_is_lead1() -> None:
        assert cats("#teamlead").is_lead == True
        assert cats("Engineering Leader").is_lead == True
        assert cats("AI Thought Leader | Cognitive Architecture | Heuristic Imperatives").is_lead == True
        assert cats("Tech leader").is_lead == True
        assert cats("Open Source Enthusiast, Project Leader @OWASP Chapter Leader @OWASP").is_lead == True
        assert cats("Mobile Platform Technical Leader - iOS Engineer").is_lead == True
        assert cats("Team Leader Manager").is_lead == True
        assert cats("People first leader and indie hacker.").is_lead == True
        assert cats("Leader of Ukrainian Rust Community").is_lead == True

      def it_handles_is_lead2() -> None:
        assert cats("Leading anti-cheat @ someplace.").is_lead == True
        assert cats("Software Engineer at @microsoft leading the Copilot UX team").is_lead == True
        assert cats("Designer Developer from Ireland, leading design and dev teams in SF.").is_lead == True
        assert cats("Into kubernetes, typescript, golang, microservices, and leading teams.").is_lead == True
        assert cats("Tech stuff at Leadingly LLC").is_lead is None
        assert cats("mechanical engineer with leading skills").is_lead is None
        assert cats("Building leading data science tools and state-of-the-art ML models").is_lead is None

        # Unclear
        assert cats("Leading a life long learning expedition").is_lead == True
        assert cats("Creating market-leading software products").is_lead == True
        assert cats("Leading talent to expertise").is_lead == True
        assert cats("All roads leading to humanoids").is_lead == True
        assert cats("Captain leading from the front!").is_lead == True

      def it_handles_is_lead3() -> None:
        assert cats("CTO at entro.solutions").is_lead is None
        assert cats("CEO at Microsoft").is_lead is None
        assert cats("VP at Facebook").is_lead is None
        assert cats("SVP at Netflix").is_lead is None
        assert cats("Not a lead").is_lead == False
        assert cats("ex-lead of GitHub QA team").is_lead == False

    def describe_role() -> None:
      def it_handles_student_verbs_1() -> None:
        assert cats("I'm learning Python at the moment").role == "Student"
        assert cats("Learning PHP at the moment").role == "Student"
        assert cats("Carl is studying Django this month").role == "Student"
        assert cats("Adapt is a global, open-source e-learning project aiming to...").role is None
        assert cats("Deep learning resources, including pretrained...").role is None
        assert cats("Making developers awesome at machine learning").role is None

      def it_handles_student_verbs_2() -> None:
        assert cats("Studying to become a therapist.").role == "Student"
        assert cats("Learning the things.").role == "Student"
        assert cats("Currently studying React Ecosystem").role == "Student"
        assert cats("MIT CSAIL's Learning and Intelligent Systems Group").role is None
        assert cats("the Learning&Training Hub of OS Kernel for Students & Developers").role is None
        assert cats("Great Learning is an online learning platform designed to...").role == "Org"
        assert cats("The GitHub repo for Learning Go by Jon Bodner").role is None

      def it_handles_student_verbs_3() -> None:
        assert cats("Studying Bio-medical engineering at Cairo University").role == "Student"
        assert cats("17, studying CS.").role == "Student"
        assert cats("Studying Software Engineering at Yunnan University China").role == "Student"
        assert cats("Studying cybersecurity").role == "Student"
        assert cats("frantically studying the world").role is None
        assert cats("Machine Learning Nut.").role is None
        assert cats("Forever learning").role is None
        assert cats("Always studying").role is None
        assert cats("Never stop studying.").role is None

    def describe_mixed() -> None:
      def it_handles_mixed1() -> None:
        assert cats("""
          Full stack software engineer. Freelance. Some time ago: CTO & co-founder at Nightset
        """) == Cats("Dev", is_freelancer=True)
        assert cats("""
        Freelance. Some time ago: CTO & co-founder at Nightset
        """) == Cats(is_freelancer = True)
        assert cats("""
          Game developer, programmer, bit of an artist; C++, Unreal
        """) == Cats("Dev")

      def it_handles_mixed2() -> None:
        assert cats("Environmental student, Unreal Engine developer") == Cats("Student")
        assert cats("""
          Software engineer working on games, and tools. Currently leading UI on Clip It @ Neura Studios.
        """) == Cats("Dev", is_lead=True)
        assert cats("""
          Founder and CEO of @rangle , the leading lean/agile JavaScript consulting firm.
        """) == Cats("Nondev")

      def it_handles_mixed() -> None:
        assert cats("Game Producer & Lead Development | Network & Systems Admin") == Cats("Nondev", is_lead=True)
        assert cats("Technical Artist. Founder of @Golden-Ram-Studio").role == "Nondev"
        assert cats("Manager, developer, and designer walk into bar").role == "Nondev"

      def it_handles_mixed5() -> None:
        assert cats("UI/UX designer -  Front Stack - iOS/SwiftUI developer").role == "Nondev"
        assert cats("iOS/SwiftUI developer and UI/UX designer").role == "Dev"
        assert cats("Business Analyst | MBA Student").role == "Dev"

      def it_handles_mixed6() -> None:
        assert cats("Software Engineering student") == Cats("Student")
        assert cats("Eng student") == Cats("Student")
        assert cats("Software Engineer student") == Cats("Student")
        assert cats("Project management is not for everyone") == Cats()

      def it_handles_mixed7() -> None:
        assert cats("Computer science masters graduate with a specialization in Data Science.").role == "Student"
        assert cats("Data science undergraduate, proficient in Computer Science.").role == "Student"
        assert cats("Engineering leadership at Square") == Cats("Dev", is_lead=True)
        assert cats("open to remote work") == Cats(is_remote=True, is_hireable=True)
        assert cats("Opened to remote job offers") == Cats(is_remote=True, is_hireable=True)
        assert cats("Currently open to remote / relocated job offers.") == Cats(is_remote=True, is_hireable=True)
        assert cats("open to freelance work") == Cats(is_freelancer=True, is_hireable=True)

      def it_handles_mixed8() -> None:
        assert cats("Machine learning engineer") == Cats("Dev")
        assert cats("Just learning here...") == Cats("Student")
        assert cats("Studying devops for fun and profit.") == Cats("Student")
        assert cats("Deep learning ftw") == Cats()
        assert cats("Peter is a remote jobseeker") == Cats(is_remote=True, is_hireable=True)
        assert cats("Freelance Programmer | Not for Hire") == Cats("Dev", is_freelancer=True, is_hireable=False)

      def it_handles_mixed9() -> None:
        assert cats("Marketing/Data Analyst").role == "Dev"
        assert cats("Yet another software dev").role == "Dev"
        assert cats("""
          daily.dev is a professional network for developers to learn, collaborate, and grow together.
        """) == Cats("Org")
        assert cats("""
          community
        """).role == "Org"
        assert cats("""
          community contributor
        """).role is None
        assert cats("""
          participated in incubating many projects about zero trust and Web3 organization
        """).role is None
        assert cats("Software development done right").role == "Dev"

      def it_handles_mixed10() -> None:
        assert cats("Aspiring Analyst").role == "Student"
        assert cats("Future engineer").role == "Student"
        assert cats("Front-end Developer 👩‍💻 \nPlatzi Student 💚 \nSoftware Engineer").role == "Dev"
        assert cats("Frontend dev by day, backend student by night").role == "Student"
        # ^ Due to invalid token.head: 'dev -> student', should have been 'dev -> dev'

      def it_handles_mixed11() -> None:
        assert cats("""
          Freelance open source developer. Hire me!
        """) == Cats("Dev", is_freelancer=True, is_hireable=True)
        assert cats("""
          I am a freelance front-end developer. you can hire me
        """) == Cats("Dev", is_freelancer=True, is_hireable=True)
        assert cats("""
          Mobile Apps & Web Developer | Freelancer | Ready for Hire
        """) == Cats("Dev", is_freelancer=True, is_hireable=True)
        assert cats("Remote tech hiring, everywhere.") == Cats()

      def it_handles_mixed12() -> None:
        assert cats("A student of life, working as a QA at a Bay Area").role == "Dev"
        assert cats("Life-long student").role is None
        assert cats("Perpetual student").role is None
        assert cats("Constant student").role is None
        assert cats("I was a student").role == "Student" # tense is not currently considered

      def it_handles_mixed13() -> None:
        assert cats("""
          Frontend + DevOp! web3 / DeFi, TypeScript, React/Next/Nest, ex. freelancer
        """) == Cats("Dev", is_freelancer=False)
        assert cats("Ex-engineer, freelancer") == Cats(is_freelancer=True)
        assert cats("Ex freelancer at Bay, forever student") == Cats(is_freelancer=False)

      def it_handles_mixed14() -> None:
        assert cats("ex-Facebook BFDL. Now tech-lead at @AWS") == Cats(is_lead=True)
        assert cats("ex-Yandex padavan. Now teamlead at @Google") == Cats(is_lead = True)
        assert cats("Formerly a manager at Foo. Now a student at Bar") == Cats("Student")
        assert cats("Yandex.Fintech | ITMO SWE '25") == Cats("Dev")

      def it_handles_mixed15() -> None:
        assert cats("Retired backend engineer") == Cats()
        assert cats("I am a data scientist with a passion for learning") == Cats("Dev")
        assert cats("Computer science newbie") == Cats("Student")
        assert cats("CMC MSU bachelor's degree, FCS HSE master student, ex-Data Scientist at Tinkoff bank") == Cats("Student")

      def it_handles_mixed16() -> None:
        assert cats("I want to be a data analyst").role == "Student"
        assert cats("I want to become a computer scientist").role == "Student"
        assert cats("Computer Science Major at NAU").role == "Student"
        assert cats("Computer science major at Stockton university").role == "Student"

      def it_handles_set17() -> None:
        assert cats("Just a beginner").role == "Student"
        assert cats("Mobile novice").role == "Student"
        assert cats("Blockchain noob").role == "Student"
        assert cats("A 2nd year studxnt of the Higher IT School.").role is None
        assert cats("Currently looking for an ML internship").role == "Student"

      def it_handles_set18() -> None:
        assert cats("Working as a Technical Recruiter!").role == "Nondev"
        assert cats("New software developer.").role == "Student"
        assert cats("I'm studying data analytics and here are my first projects").role == "Student"
        assert cats("Hello. I'am Vadim Tikhonov. I study code, data analysis and data science.").role == "Student"
        assert cats("I am new to ML & DL").role == "Student"
        assert cats("Seeking new opportunities;").role is None

      def it_handles_set19() -> None:
        assert cats("Aspiring Python Data Analyst").role == "Student"
        assert cats("CS Undergrad at New Jersey Institute of Technology").role == "Student"
        assert cats("Game developer from New Orlean").role == "Dev"
        assert cats("Intern at Microsoft").role == "Student"
        assert cats("Internship at Netflix").role == "Student"
        assert cats("Financial University under the government of Russia").role is None

      def it_handles_set20() -> None:
        assert cats("Junior Dev @ free lance") == Cats("Dev", is_freelancer=True)
        assert cats("""
          Master of Science in Information Systems student at Stevens Institute of Technology, NJ, USA.
        """) == Cats("Student")
        assert cats("Web developer studying to become a therapist").role == "Dev"
        assert cats("Full time Architect, Consultant, Learner, Author").role == "Dev"
        assert cats("Engineer, learning PHP at the moment").role == "Dev"
        assert cats("I've just learned a bit of HTML & CSS").role is None # too contextual

      def it_handles_set21() -> None:
        assert cats("Software Developer learning Systems Analysis and Development.").role == "Dev"
        assert cats("Software engineer studying mathematics").role == "Dev"
        assert cats("Aspiring engineer studying networking & security.").role == "Student"
        # ^ OK "aspiring" cancels "engineer", then "studying" is captured
        # assert is_student("Aspiring 16 y/o software engineer studying networking & security.")
        # ^ Spacy model fails to parse such a long noun phrase properly, needs to be retrained
        assert cats("iOS architect, studying Rust").role == "Dev"
        assert cats("Frontend dev who currently learning Rust & Elixir").role == "Dev"
        assert cats("Teenager, freelancer, backend developer (TypeScript, C++)") == Cats(
          "Student", is_freelancer = True
        )

      def it_handles_set22() -> None:
        assert cats("Formerly a student at Something").role is None
        assert cats("A former student at Something").role is None
        assert cats("Programming newbie").role == "Student"
        assert cats("Just a noob").role == "Student"

      def it_handles_set23() -> None:
        assert cats("Bachelor student of Comp Sci @ Concordia University").role == "Student"
        assert cats("Bachelor of Comp Sci student @ Concordia University").role == "Student"
        assert cats("Private Pilot | Bachelor of Science").role == "Student"
        assert cats("Computer Engineer & MSc Student").role == "Dev"
        assert cats("MSCS Student").role == "Student"

      def it_handles_set24() -> None:
        assert cats("""
          I am Viktor Klang, a finder, researcher, problem solver, improver of things,
          life-long student, developer/programmer, leader, mentor/advisor, public speaker…
        """) == Cats("Dev", is_lead=True)
        assert cats("""
          Specializing generalist. CS PhD, student of life. Lover of words and hyperbole. Remote.
        """) == Cats("Dev", is_remote=True)
        assert cats("music student java elasticsearch ai subversion git node").role == "Student"
        assert cats("Back-End Developer | Information Systems bachelor").role == "Dev"
        assert cats("CS Bachelor student at USI").role == "Student"
        assert cats("CS Bachelor at USI").role == "Student"

      def it_handles_set25() -> None:
        assert cats("Biotech student and sometimes software developer.").role == "Student"
        assert cats("Software developer and sometimes biotech student.").role == "Dev"
        assert cats("Everlasting student · Freelance · Life lover") == Cats(is_freelancer=True)
        assert cats("rookie front-end developer").role == "Student"
        assert cats("""
          Professor of the Practice in Computer Science, Program Director
          for the Fundamentals of Computing Undergraduate Certificate Program
        """).role == "Nondev"

      def it_handles_set26() -> None:
        assert cats("""
          NET Developer with front-end skills, Freelancer, Photographer and Science Lover
        """) == Cats("Dev", is_freelancer=True)
        assert cats("""
          Arman is a full-stack developer who mainly focuses on web development
        """).role == "Dev"
        assert cats("""
          Teenager, freelancer, backend developer (TypeScript, C++17)
        """) == Cats("Student", is_freelancer=True)
        assert cats("Oleg Rybnikov - a freelancing web artisan specializing in Vite").is_freelancer
        assert cats("#backend #java #freelancer").is_freelancer

      def it_handles_set27() -> None:
        assert cats("""
          applied artificial intelligence student, free to relocate
        """) == Cats("Student")
        assert cats("""
          🇸🇰 Freelancer full-stack developer. #React #ReactNative
        """) == Cats("Dev", is_freelancer=True)
        assert cats("""
          Full stack software engineer at dextra | Freelancer
        """) == Cats("Dev", is_freelancer=True)
        assert cats("""
          Self-taught Developer graded in Back-end Development. -Freelancer
        """) == Cats("Dev", is_freelancer=True)

      def it_handles_set28() -> None:
        assert cats("indie dev • iOS & macOS • freelance") == Cats("Dev", is_freelancer=True)
        assert cats("Freelancer Jedi Padawan") == Cats(is_freelancer=True)
        assert cats("freelance math teacher, freelance front-end developer") == Cats("Nondev", is_freelancer=True)
        assert cats("I'm a Software Engineer, Ethical Hacker, and security enthusiast") == Cats("Dev")
        assert cats("⭐️ Senior Software Developer ⭐️ Blockchain / Backend / ETL") == Cats("Dev")

      def it_handles_set29() -> None:
        assert cats("Gopher. Former TL of Go CDK and author of Wire.") == Cats("Dev", is_lead=False)
        assert cats("TL, JavaScript Developer") == Cats("Dev", is_lead=True)
        assert cats("CTO, TL") == Cats("Nondev", is_lead=True)
        assert cats("Typographer, Tech Lead") == Cats(is_lead=True)
        assert cats("TL;DR : DJ turned software engineer") == Cats("Dev")
        assert cats("Founder and SVP Creative at Frac.tl") == Cats("Nondev")
        assert cats("Senior Site Reliability Engineer, TL") == Cats("Dev", is_lead=True)

      def it_handles_set31() -> None:
        assert cats("✒️ Co-founder of CollBoard.com").role == "Nondev"
        assert cats("Founder").role == "Nondev"
        assert cats("Cofounder").role == "Nondev"
        assert cats("Co founder").role == "Nondev"
        assert cats("Co-founder").role == "Nondev"
        assert cats("Engineer").role == "Dev"
        assert cats("Developer").role == "Dev"
        assert cats("Dev").role == "Dev"
        assert cats("Programmer").role == "Dev"
        assert cats("Coder").role == "Dev"
        assert cats("Mentor").role == "Nondev"
        assert cats("Teacher").role == "Nondev"
        assert cats("Lecturer").role == "Nondev"
        assert cats("Mathematician").role == "Dev"
        assert cats("Agency").role == "Org"
        assert cats("Company").role == "Org"
        assert cats("Solidity developer with 10+ years experience. CTO at entro.solutions").role == "Dev"
        assert cats("company founder at 18yo, programmer, game developer, VR enthusiast").role == "Nondev"
        assert cats("Fullstack web design agency").role == "Org"

      def it_handles_set32() -> None:
        assert cats("AWESOME Developer/Lead") == Cats("Dev", is_lead=True)
        assert cats("Software Dev & Tech Lead") == Cats("Dev", is_lead=True)
        assert cats("Lead Cloud Engineer @ Namecheap") == Cats("Dev", is_lead=True)
        assert cats("Horizon 2020 Project LEAD: Low-Emission logistics") == Cats(is_lead=True)
        assert cats("Technical Content Lead") == Cats(is_lead=True)
        assert cats("IT Sec guy, @zaproxy co-lead") == Cats("Dev", is_lead=True)
        assert cats("Raising the bar for leadership in tech.") == Cats(is_lead=True)
        assert cats("The leading platform for local cloud development") == Cats("Org")

      def it_handles_set34() -> None:
        assert cats("Founder & CEO @QualiSage | Team Lead | Senior Full-Stack Developer") == Cats("Nondev", is_lead=True)
        assert cats("Junior Programmer @BohemiaInteractive | Founder @QX-Interactive") == Cats("Dev")
        assert cats("Lecturer at Rowan University") == Cats("Nondev")
        assert cats("freshman at Rowan University") == Cats("Student")
        assert cats("sophomore at Rowan University") == Cats("Student")

      def it_handles_set35() -> None:
        assert cats("""
          My name is Devin and I am a Senior Gameplay Designer at 
          CD Projekt Red working on the next Witcher.
        """).role == "Nondev"
        assert cats("""
          "Striving to become a front-end developer. Formerly climbing gym founder and co-owner"
        """).role == "Student"
        assert cats("""
          Founder, CBB Analytics. Sports Data Scientist and Web Developer.
        """).role == "Nondev"
        assert cats("""
          Twas brillig, and the slithy toves
          Did gyre and gimble in the wabe
        """).role is None

      def it_handles_set36() -> None:
        assert cats("Bachelor").role == "Student"
        assert cats("Bachelor student").role == "Student"
        assert cats("Bachelor student engineer").role == "Student"
        assert cats("Bachelor engineer student").role == "Student"
        assert cats("Bachelor engineering student").role == "Student"
        assert cats("BS engineering student").role == "Student"
        assert cats("B.S engineering student").role == "Student"
        assert cats("B.Sc engineering student").role == "Student"
        assert cats("Master-of-Science engineering student").role == "Student"
        assert cats("MS engineering student").role == "Student"
        assert cats("M.S engineering student").role == "Student"
        assert cats("M.Sc engineering student").role == "Student"

      def it_handles_set37() -> None:
        assert cats("Head of Design @github.").role == "Nondev"
        assert cats("Associate Professor of CS at Augusta University.").role == "Nondev"
        assert cats("Head of developer advocacy @pieces-app").role == "Nondev"
        assert cats("permanent head damage").role is None
        assert cats("Code samples from the book Head First Go").role is None
        assert cats("Growth Head").role == "Nondev"
        assert cats("Head Coach @nashville-software-school").role == "Nondev"
        assert cats("Head of Engineering @gigs").role == "Nondev"
        assert cats("Head of OSS @huggingface. Open Source developer.").role == "Nondev"
        assert cats("MY HEAD IS IN THE CLOUD!!").role is None
        assert cats("Head of India @lendsmartlabs").role == "Nondev"
        assert cats("Head of Technology").role == "Nondev"
        assert cats("Head down and build").role is None
        assert cats("Head Of Security Research @F5Networks").role == "Nondev"
        assert cats("Head of Flickr.").role == "Nondev"

      def it_handles_set38() -> None:
        assert cats("head hurts...").role is None
        assert cats("Research Head").role == "Nondev"
        assert cats("Hip-hop head... ancora imparo...").role is None
        assert cats("Head of DevOps").role == "Nondev"
        assert cats("Senior Mentor and Java practice Head, Coding Blocks").role == "Nondev"
        assert cats("Head @ Payments by Wix").role == "Nondev"
        assert cats("A small baby head with huge headphones.").role is None
        assert cats("Batfish @ AWS Former head of engineering @ Intentionet").role is None
        assert cats("Physics research head at nvidia").role == "Nondev"
        assert cats("Head of Teaching at SALT").role == "Nondev"
        assert cats("Head of SRE @Billhop").role == "Nondev"
        assert cats("Head of DS @UW").role == "Nondev"
        assert cats("Co-Founder and Training Head @AltCampus").role == "Nondev"
        assert cats("Author of Head First Ruby and Head First Go, published by O'Reilly Media.").role is None
        assert cats("Hot Headed & Stubborn Programmer").role == "Dev"
        assert cats("head in ☁️").role is None
        assert cats("git reset HEAD~1").role is None
        assert cats("Head of Oxford Research Software Engineering").role == "Nondev"

      def it_handles_set39() -> None:
        assert cats("Freelancer and video editor").is_freelancer
        assert cats("Full stack developer, tech consultant").is_freelancer
        assert cats("Backend SWE & consulting").is_freelancer
        assert cats("Java Full-stack Developer at j-labs.pl Crif consultant").is_freelancer
        assert cats("Front-end & WordPress developer, UX consultant. Making stuff for the web since 2005").is_freelancer

      def it_handles_set40() -> None:
        assert cats("Frontend Consultant; Web, Mobile and Desktop Applications Developer").is_freelancer
        assert cats("My name is Jorens, I'm a Full Stack developer, currently freelancing").is_freelancer
        assert cats("WebGL, WebXR, full-stack, consulting").is_freelancer
        assert cats("Full-stack junior software developer, system administrator and IT consultant.").is_freelancer
        assert cats("I have transformed years of freelancing into a full-time career").is_freelancer
        assert cats("Something @ devlance").is_freelancer is None

      def it_handles_set41() -> None:
        assert cats("Freelancer Nasim is a Web Application Developer.").is_freelancer
        assert cats("Opensource enthusiast, Skillbox teacher, Blogger").is_freelancer is None
        assert cats("Free-lancer @ BYTESADMIN • Security Researcher").is_freelancer
        assert cats("Freelance Clojure programmer").is_freelancer
        assert cats("Freelance ⠁⣿⣿ ⣿⣿⣿ ⣿⣿⣿").is_freelancer
        assert cats("Weblancer").is_freelancer is None

      def it_handles_set42() -> None:
        assert cats("I am a passionate student who loves to learn and explore").role == "Student"
        assert cats("undergraduate student of Tongji university").role == "Student"
        assert cats("Undergraduate at UC Berkeley, double major in CS and Math.").role == "Student"
        assert cats("Formerly Stanford CS PhD Student.").role is None

      def it_handles_set43() -> None:
        assert cats("👨 tech enthusiast / applied ai student").role == "Student"
        assert cats("A Ph.D. student in statistical science.").role == "Student"
        assert cats("PhD student at MIT Brain and Cognitive Sciences").role == "Student"
        assert cats("A strong conceptual thinker and a constant student").role is None

      def it_handles_set44() -> None:
        assert cats("Postgraduate student at Lund University.").role == "Student"
        assert cats("Student of Chinese medicine, dance teacher, rare soul & funk music digger").role == "Student"
        assert cats("Graduate Diploma in IT graduate with an undergraduate degree in Bachelor of Laws").role == "Student"
        assert cats("I engineer 'learn by doing' experiences for uni students with lean...").role == "Dev"

      def it_handles_set45() -> None:
        assert cats("My name is Harold Bogg, I am a college student").role == "Student"
        assert cats("Vice Dean for Undergraduate Studies").role == "Nondev"
        assert cats("My name is Josh Student").role == "Student"
        # ^ known false positive. Can't fix due to Spacy model limitations,

      def it_handles_mixed51() -> None:
        assert cats("""
          👨‍💻 developer of 🌐 coora-ai.com 🧭 igapo.xyz / tech enthusiast / applied artificial intelligence student
        """) == Cats("Dev")
        assert cats("""
          👨 VP Eng. at MedScout, storyteller, student of disasters.
        """) == Cats("Nondev")
        assert cats("""
          Technology leader at Gartner (Managing Vice President).
          Graduate student at University of Illinois getting my MBA. Forever an engineer.
        """) == Cats("Nondev", is_lead=True)
        assert cats("""
          Technology entrepreneur, sports lover, network security student.
        """) == Cats("Nondev")
        assert cats("""
          Lawyer. Lecturer. Researcher. Student
        """) == Cats("Nondev")

      def it_handles_mixed52() -> None:
        assert cats("""
          Blockchain student. Crypto investor.
        """) == Cats("Student")
        assert cats("""
          Technology entrepreneur, sports lover, network security student.
        """) == Cats("Nondev")
        assert cats("""
          Hi, I am 22 years old freelance full-stack developer from Czech Republic.
        """) == Cats("Dev", is_freelancer=True)
        assert cats("""
          As a Klingon code warrior, I take seriously the old proverb:
          "ghojwI'pu'lI' tISaH" ('Care about your students').
        """) == Cats()
        assert cats("""
          Dad | Runner | Aviation Student | Dog Lover | Builder of cool shit"
        """) == Cats("Student")

      def it_handles_mixed53() -> None:
        assert cats("""
          On a mission to help every student to reach their potential with technologies")
        """) == Cats("Student") # known issue
        assert cats("""
          TOGAF 9 Certified Enterprise Architect, Pragmatist, Economic Student, Biker,
        """) == Cats("Dev")
        assert cats("""
          Currently a Computer Science graduate student at University
          of the Philippines Diliman working on quantum algorithms.
        """) == Cats("Student")
        assert cats("""
          Over 30 years of experience working with diverse teams of researchers and
          students developing interactive software and hardware for science inquiry.
        """) == Cats("Dev") # because of "developing"
        assert cats("""
          B.Sc. in C.S. and M.Eng. student at the University of Bologna.
        """) == Cats("Student")

      def it_handles_mixed54() -> None:
        assert cats("""
          Software engineer at @GRID-is. Fellow of the Royal Geographical Society.
          Postgraduate student at Lund University.
        """) == Cats("Dev")
        assert cats("""
          Lead AI/ML Engineer at MITRE. Graduate student in Statistics at George Mason University.
          Officer emeritus of @srct, @gmuthetatau, @masonlug
        """) == Cats("Dev", is_lead=True)
        assert cats("""
          Developer at Sky and undergraduated in C.S. in Federal University of South Frontier
        """) == Cats("Dev")
        assert cats("""
          Undergraduate studying 'Software and Information Engineering' at the Vienna University of Technology
        """) == Cats("Student")
        assert cats("""
          Junior UI Designer @ Section BFA Design Art Undergraduate from NTU ADM, Singapore
        """) == Cats("Nondev")

      def it_handles_mixed55() -> None:
        assert cats("""
          Senior Software Engineer at @pagarme | Computer Science undergraduate at Pontifical Catholic University of Paraná
        """) == Cats("Dev")
        assert cats("""
          Full-time software developer and student. Spare-time Japan fan and gamer
        """) == Cats("Dev")

      def it_handles_mixed56() -> None:
        assert cats("""
          Founder & CEO @QualiSage | Team Lead | Senior Full-Stack Developer | 10+ Years
        """) == Cats("Nondev", is_lead=True)
        assert cats("Junior Programmer @BohemiaInteractive | Founder @QX-Interactive") == Cats("Dev")
        assert cats("""
          Full-stack web developer and Zend Certified PHP Engineer. Lead dev @Web3Box and freelancer @toptal
        """) == Cats(
          "Dev", is_freelancer = True, is_lead=True
        )
