from ...utils import literal
from ..utils import Skill, dis_context, dis_sequence

__all__ = ["SKILLS"]

dis_ctx = dis_context("google")

SKILLS: list[Skill] = [
  Skill("Google", ["(@)google"], "Company"),

  Skill("Flax", ["flax"], "NN for Jax"),
  Skill("JAX", [literal("JAX")], "TensorFlow alternative"),
  Skill("JAX", ["jax"], disambiguate=[
    dis_sequence(),
    dis_context("google", "flax", "tensorflow"),
  ]),
  Skill("TensorFlow", ["tensorflow"], ""),

  Skill("Flutter", ["flutter"], ""),

  # CLOUD
  Skill("Google-BigQuery", ["google-bigquery", "bigquery"], ""), # EE data warehouse
  Skill("Google-Cloud", ["google=cloud", "gcp"], ""),
  Skill("Google-Cloud", ["gc"], disambiguate=[
    dis_sequence(),
    dis_context("aws", "azure"),
  ]),
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
