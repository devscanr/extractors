from extractors.utils import Pattern, verb

__all__ = ["LABELED_PHRASES"]

type LabeledPhrases = dict[str, list[str | Pattern]]

LABELED_PHRASES: LabeledPhrases = {
  "DEV": [
    verb("coding"),
    verb("developing"),
    verb("programming"),
    verb("engineering"),

    # ADMINISTRATORS
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

    # DEVS
    "developer", "dev",
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
    "aiops",
    "dataops",
    "dev=op(s)",
    "dev/sec-ops", "devopssec", "devsecops", "sec/dev-ops", "secdevops",
    "ml=op(s)",
    "net=ops",
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
    "researcher",
    "scientist",

    # OTHER
    # expert
    # generalist
    "hacker",
    "investigator",
    # professional
    # specialist
  ],
  "FREELANCER": [
    "free=lance(r)",
    "free=lancing",
    "consultancy",
    "consultant",
    "consulting",
  ],
  "LEAD": [
    "lead",
    "leader",
    verb("leading"),
    "leadership",
    "teamlead", "tl",
    "techlead",
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
  ],
  "NONDEV": [
    "academic",
    "artist",
    "auditor",
    "ceo",
    "coach",
    "co=founder",
    "cto",
    "dean",
    "designer",
    "gamedesigner",
    "uidesigner",
    "webdesigner",
    verb("designing"),
    "director",
    "educator",
    "entrepreneur", "businessman",
    "founder",
    verb("founding"),
    "head",
    verb("hiring"),
    "investor",
    "lawyer",
    "lecturer",
    verb("lecturing"),
    "owner",
    "president",
    "producer",
    verb("producing"),
    "professor", "prof",
    "postdoc",
    "manager",
    verb("managing"),
    "mentor",
    verb("mentoring"),
    "musician",
    "recruiter", # recruiters?
    verb("recruiting"),
    "svp",
    "teacher",
    verb("teaching"),
    "vp",
  ],
  "STUDENT": [
    "alumni", "alumnus", "alum",
    "beginner",
    "graduate",
    "bachelor",
    "bachelor of science",
    "b.s",
    "freshman",
    "intern",
    "internship",
    # just "master"
    "master of science",
    "m.s",
    "major",
    "learner",
    verb("learn"),
    verb("learning"),
    "newbie", "noob",
    "new to",
    "novice",
    "rookie",
    "sophomore",
    "student",
    verb("study"),
    verb("studying"),
    "teenage", # TODO should be smth. like "teenage [NOUN]
    "teenager",
    "undergrad(uate)",
  ],
  "REMOTE": [
    "remote",
    "remotely",
  ],
  "HIREABLE": [
    "for=hire",
    "hire=able",
    "hirable",
    "hire=me",
    "hire=us",
    "hiring=me",
    "job=seeker",
    "job=seeking",
    "job=wanted",
    "open=to=work",
    "open=for=work",
  ],
  "OPEN-TO": [
    "available for",
    "available to",
    "consider(ing)",
    "look(ing) for",
    "open(ed) for",
    "open(ed) to",
    "ready for",
    "ready to",
    "search(ing)",
    "seeking",
  ],
}

# ("guru", "expert", "ninja", "magician", "wizard") were previously used
# to cancel "Student" role. Not applied yet, not sure...
