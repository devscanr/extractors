# from ...utils import ver1, propn
from ..utils import Skill, contextual, contextual_or_neighbour

__all__ = ["SKILLS"]

ctx = contextual("Google")
ctxn = contextual_or_neighbour(["Google"], 2)

SKILLS: list[Skill] = [
  Skill("Google", ["google"]), # company (etc)

  # CLOUD
  Skill("Google-BigQuery", ["google=bigquery"]), # EE data warehouse
  Skill("Google-Cloud", ["google=cloud", "gcp", "gcs"]),
  Skill("Firebase", ["google=firebase", "firebase"]),
  Skill("Google-Sheets", ["google=sheets"]),
  Skill("Google-BigTable", ["google=bigtable"]), # fast flexible noSQL

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
