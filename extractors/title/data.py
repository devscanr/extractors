__all__ = [
  "LABELED_PHRASES",
]

type LabeledPhrases = dict[str, list[str]]

LABELED_PHRASES: LabeledPhrases = {
  "HUMAN": [
    # ADMININSTRATORS
    "administrator", "admin",
    "dbadmin", "dba",
    "systemadministrator", "sysadmin",

    # ANALYSTS
    "analyst",
    "businessanalyst",
    "dataanalyst",

    # ARCHITECTS
    "architect",
    "dataarchitect",
    "dbarchitect",

    # DEVELOPERS
    "developer", "dev", "dev.", # TODO verify how "dev." is parsed
    "gamedeveloper", "gamedev",
    "godev", "gopher",
    "mobiledeveloper", "mobiledev",
    "phpdeveloper", "phpdev", "phper",
    "pydev", "pythonist(a)",
    "rubydev", "rubyist", "rubist",
    "rustacean",
    "softwaredeveloper", "softwaredev",
    "systemdeveloper",
    "webdeveloper", "webdev",

    # ENGINEERS
    "engineer", "eng",
    "dataengineer",
    "mlengineer",
    "softwareengineer", "swe", "sde",
    "systemengineer",
    "webengineer",

    # PROGRAMMERS
    "programmer", "coder",
    "gameprogrammer",
    "phpcoder",
    "webprogrammer", "webcoder",

    # OPERATIONS & SECURITY
    "operations", "op(s)",
    "ai=op(s)",
    "dataop(s)",
    "dev=op(s)",
    "dev/sec-ops", "devopssec", "devsecops", "sec/dev-ops", "secdevops",
    "ml=op(s)",
    "net=op(s)",
    "security", "sec",
    "sec=op(s)",
    "sysops",

    # TESTERS & QA
    "qa",
    "tester",
    "pentester",
    "qatester",

    # SCIENCE & ACADEMY
    "mathematician",
    "ph.d",
    "ph.d candidate",
    "researcher",
    "scientist",
    "statistician",

    # OTHER
    "enthusiast",
    "expert",
    "generalist",
    "guru",
    "hacker",
    "investigator",
    "ninja",
    "professional",
    "specialist",
    "wizard",

    # FREELANCERS
    "free=lancer",
    "consultant",

    # LEADS
    "lead",
    "leader",
    "teamlead", "tl",
    "techlead",

    # NONDEVS > DESIGNERS
    "designer",
    "gamedesigner",
    "uidesigner",
    "webdesigner",

    # NONDEVS > OTHER
    "academic",
    "animator",
    "artist",
    "auditor",
    "author",
    "ceo",
    "chemist",
    "coach",
    "co=founder",
    "cto",
    "dean",
    "director",
    "educator",
    "entrepreneur", "businessman",
    "founder",
    "head",
    "informatician",
    "investor",
    "lawyer",
    "lecturer",
    "owner",
    "physicist",
    "president",
    "producer",
    "professor", "prof",
    # postdoc ?
    "manager",
    "mentor",
    "musician",
    "recruiter",
    "svp",
    "teacher",
    "trainer",
    "vp",

    # STUDENTS
    "alumni", "alum",
    "amateur",
    "beginner",
    "bachelor",
    "bachelor of science", "b.s",
    "freshman",
    "graduate",
    "intern",
    "master of science", "m.s",
    "major",
    "learner",
    "newbie", "noob",
    "novice",
    "rookie",
    "sophomore",
    "student",
    "teenager",
    "undergrad(uate)",

    # UNSORTED
    # "employee",
  ],

  "SKIP": [
    "head first"
  ],

  "ORG": [
    "agency",
    "company",
    "community",
    "firm",
    "organization", "org",
    "platform",
    "professional network",
    "social network",
    "team",
  ],
}
