__all__ = ["LABELED_PHRASES"]

type LabeledPhrases = dict[
  str,
  list[str | tuple[str, str]]
]

LABELED_PHRASES: LabeledPhrases = {
  "DEV": [
    "admin",
    "analyst",
    "architect",
    "coder",
    ("coding", "VERB"),
    ("developing", "VERB"),
    ("programming", "VERB"),
    "dba", # DB admin
    "dev",
    "dev=op(s)",
    "developer",
    "development",
    "eng",
    "engineer",
    "engineering",
    "gopher",
    "hacker",
    "investigator",
    "mathematician",
    "ml=op(s)",
    "op(s)",
    "pentester",
    "ph.d",
    "pythonist(a)",
    "programmer",
    "qa",
    "rustacean",
    "researcher",
    "scientist",
    "sec",
    "sec=op(s)",
    "sde",
    "swe",
    "tester",
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
    ("leading", "VERB"),
    "leadership",
    "teamlead",
    "techlead",
    "tl",
  ],
  "ORG": [
    "agency",
    "company",
    "community",
    "firm",
    "organization",
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
    "cofounder",
    "co-founder",
    "cto",
    "dean",
    "designer",
    ("designing", "VERB"),
    "director",
    "educator",
    "entrepreneur",
    "founder",
    ("founding", "VERB"),
    "head",
    ("hiring", "VERB"),
    "investor",
    "lawyer",
    "lecturer",
    ("lecturing", "VERB"),
    "owner",
    "president",
    "producer",
    ("producing", "VERB"),
    "prof",
    "professor",
    "postdoc",
    "manager",
    ("managing", "VERB"),
    "mentor",
    ("mentoring", "VERB"),
    "musician",
    "recruiter", # recruiters?
    ("recruiting", "VERB"),
    "svp",
    "teacher",
    ("teaching", "VERB"),
    "vp",
  ],
  "STUDENT": [
    "alumni", "alumnus", "alum",
    "beginner",
    "graduate",
    "bachelor",
    "b.s",
    "freshman",
    "intern",
    "internship",
    "master of science",
    "m.s",
    "major",
    "learner",
    ("learn", "VERB"),
    ("learning", "VERB"),
    "newbie",
    "new to",
    "noob",
    "novice",
    "rookie",
    "sophomore",
    "student",
    ("study", "VERB"),
    ("studying", "VERB"),
    "teenage",
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
    "hiring=me",
    "job=seeker",
    "job=seeking",
    "open=to=work",
    "open=for=work",
  ],
  "OPEN-TO": [
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

# ("specialist", "generalist", "guru", "expert", "ninja", "magician", "professional", "wizard") were previously used
# to cancel "Student" role. Not applied yet, not sure...
