from ...utils import propn
from ..utils import Skill, contextual, contextual_or_neighbour, neighbour

__all__ = ["SKILLS"]

ctx = contextual("Google")
ctxn = contextual_or_neighbour(["Google"], 2)

SKILLS: list[Skill] = [
  Skill("Google", ["(@)google"], "Company"),

  Skill("Flax", ["flax"], "NN for Jax"),
  Skill("JAX", [propn("JAX")], "TensorFlow alternative"),
  Skill("JAX", ["jax"], disambiguate=neighbour(2)),
  Skill("TensorFlow", ["tensorflow"], ""),

  Skill("Flutter", ["flutter"], ""),

  # CLOUD
  Skill("Google-BigQuery", ["google-bigquery", "bigquery"], ""), # EE data warehouse
  Skill("Google-Cloud", ["google=cloud", "gcp"], ""),
  Skill("Google-Cloud", ["gc"], disambiguate=contextual("AWS", "Azure")),
  Skill("Google-Firebase", ["google=firebase", "firebase"], ""),
  Skill("Google-CloudStorage", ["google-cloud=storage", "gcs"], ""),
  Skill("Google-Pub/Sub", ["google-pub/sub"], ""),
  Skill("Google-Sheets", ["google=sheets"], ""),
  Skill("Google-BigTable", ["google-bigtable"], ""), # fast flexible noSQL
  Skill("Google-Kubernetes", ["google-kubernetes-engine", "google=ke", "google=ks", "gke", "gks"], ""), # ~ Amazon-EKS

  # Drive
  # GC Functions
  # GC Firestore (= AWS EFS)
  # GC Storage (= AWS S3)
  # GC SSD (= AWS EBS)
  # GC AI Platform
  # GC Kubernetes Engine (GKE)
  # GC Pub/Sub
  # GC Run
]
