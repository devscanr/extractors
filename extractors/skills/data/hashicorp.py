from ..skill import Skill

SKILLS: list[Skill] = [
  Skill("HashiCorp", ["(@)hashicorp"], "Company"),

  # OPS
  Skill("Consul", ["consul"], "Service-based networking"),
  Skill("HCL", ["hcl"], "Configuration language for infrastructure automation"),
  Skill("Nomad", ["nomad"], "Workload scheduling and orchestration"),
  Skill("Packer", ["packer"], "Build and manage images as code"),
  Skill("Terraform", ["terraform"], "Cloud infrastructure provisioning using a common workflow"),
  Skill("Vault", ["vault"], "Identity-based secrets management"),
]
