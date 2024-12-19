from ..utils import Skill

__all__ = ["SKILLS"]

SKILLS: list[Skill] = [
  Skill("Cisco", ["(@)cisco", "cysco=systems"], "Company"),

  # NETWORKS
  Skill("Cisco-ACI", ["cisco=aci"], "Software-defined networking (SDN) solution for data centers"),
  Skill("Cisco-Nexus", ["cisco=nexus"], "Modular and fixed port network switches for data centers"),

  # CERTIFICATES
  Skill("Cisco-CNA", ["ccna"], "Certificate"), #
  Skill("Cisco-CNP", ["ccnp"], "Certificate"), # TODO "CCNP or equivalent required; CCIE or other advanced certs are preferred."
]
