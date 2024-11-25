from extractors.skills.extractor import SkillExtractor
from extractors.utils import normalize

texts: list[str] = [
  # "Postdoc @ CS Princeton",
  # "Political Science data analyst specializing in R",
  # "Passionate about learning new things. I am now learning programming languages for Web development like HTML, CSS, Javascript and React.",
  # "New Front End Web Developer looking to grow my skillset and learn as much as I   can while providing quality service!",
  # "Hey, it's Karim Rowan '28 CS student. Currently, I'm on my freshman year.",
  # "I am an economist / data analyst who enjoys exploring data.",
  # "Full-stack developer on a quest to unlock the full potential of my computer (and maybe yours too) 🚀 Mostly work in JS, React & Java, but always learning more",
  # "Dr. Vinay Shah is an eminent physician, gynaecologist and obstetrician in Clifton, northern New Jersey who has provided top-quality medical care and services.",
  # "PCB Design and Firmware Development",
  # "Cybersecurity Professional: motivated, extroverted, and a self-learner.",
  # "Stevens Institute of Technology 22' Computer Science  ",
  # "Business Analyst | MBA Graduate from Stevens Institute of Technology",
  # "New to Bankless Crypto investing",
  # "Self-taught developer and data enthusiast with a geosciences background",
  # "Cyber security student at Norwegian University of Science and Technology , I love coding. I try always to learn new things",
  # "BHS Robotics Engineer, Coder, and Driver for (Honey-K-Ohms) 16557 :)",
  # "Rohit Kabra (Masters in information System)",
  # "Mathematician turned Programmer and Web Developer",
  # "We Are more than just a stake pool we are part of our community locally and plans the broaden our reach",
  # "Welcome to Forever Young Complete Healthcare & Med Spa in New Jersey. Forever Young Complete Healthcare specializes in Bio-Identical Hormone Therapy, Functional",
  # "2017 Kean University graduate in Computer Science/Information Systems",
  # "MSc in CS from Rochester Institute of Technology",
  # "Hi, I am a recent Rowan University Computer Science graduate, looking to pursue a career in software development!",
  # "Software Developer @climatecentral",
  # "I enjoy discovering new things.  I'm fluent in 5 languages, including german,polish,russian,latin and english.",
  # "Hello everyone! I'm a Software Engineer and hybrid creative graphic designer with over 20 years of experience in the world of web development and UI.",
  # "Hi, my name is Evince (pronounced: 'Ev-ince') Edouard. I am passionate about solving problems and being an awesome team member.",
  # "Software Engineer at Bolt",
  # "PhD student in Theoretical Particle Physics, at TAU/IAS.",
  # "Graduating December 2020, pursuing full time opportunities. Feel free to connect with me on LinkedIn!",
  # "B.S. Computer Science '26 @ Stevens Institute of Technology | EMT, photographer, tech nerd, and EDC enthusiast.",
]

e = SkillExtractor()

for text in texts:
  print("text:", repr(text))
  print(
    e.extract(normalize(text))
  )
  print("----------")

# TODO remove `_.used` extension if it's no longer necessary :)
