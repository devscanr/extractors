from ..skill import Company, Skill, Tech
from ..utils import dis_context, dis_neighbours

dis_ctx = dis_context("google")

SKILLS: list[Skill] = [
  Company("Google", ["(@)google"], "Company"),

  Tech("Flax", ["flax"], "NN for Jax"),
  Tech("JAX", ["JAX"], "TensorFlow alternative"),
  Tech("JAX", ["jax"], disambiguate=[
    dis_neighbours(),
    dis_context("google", "flax", "tensorflow"),
  ]),
  Tech("TensorFlow", ["tensorflow"]),

  Tech("Flutter", ["flutter"]),

  # CLOUD
  Tech("Google-BigQuery", ["google-bigquery", "bigquery"]), # EE data warehouse
  Tech("Google-Cloud", ["google=cloud", "gcp"]),
  Tech("Google-Cloud", ["gc"], disambiguate=[
    dis_neighbours(),
    dis_context("aws", "azure"),
  ]),
  Tech("Google-Firebase", ["google=firebase", "firebase"]),
  Tech("Google-CloudStorage", ["google-cloud=storage", "gcs"]),
  Tech("Google-Pub/Sub", ["google-pub/sub"]),
  Tech("Google-Sheets", ["google=sheets"]),
  Tech("Google-BigTable", ["google-bigtable"]), # fast flexible noSQL
  Tech("Google-Kubernetes", ["google-kubernetes-engine", "google=ke", "google=ks", "gke", "gks"]), # ~ Amazon-EKS

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
