from ...utils import ver1, propn, noun
from ..utils import Skill, contextual, neighbour, contextual_or_neighbour

__all__ = ["SKILLS"]

ctx = contextual("Microsoft")
ctxn = contextual_or_neighbour(["Microsoft"], 2)

SKILLS: list[Skill] = [
  Skill("Microsoft", ["microsoft"], "Company"),

  Skill("MS-Access", ["microsoft-access", "ms-access"], ""),
  Skill("MS-Excel", ["microsoft-excel", "ms-excel", propn("excel")], ""),
  Skill("MS-SQLServer", [
    "microsoft-sql(=server)", "(ms=)sql=server", "ms=sql",
    "(sql=server-)management-studio",
    "(microsoft-)management-studio",
  ], ""),
  # TODO T-SQL
  Skill("MS-Sharepoint", ["microsoft-sharepoint", "ms-sharepoint", "sharepoint"], ""),
  Skill("MS-365", ["microsoft=365", "ms=365"], "New name for MS-Office"),
  Skill("MS-365", ["365"], disambiguate=ctx),

  Skill("Power-Platform", ["power-platform"], ""),
  Skill("Power-Apps", ["power=apps"], ""),
  Skill("Power-Automate", ["power-automate"], ""),
  Skill("Power-BI", ["power=bi"], ""),
  Skill("Power-Pivot", ["power-pivot"], ""),
  Skill("Power-Query", ["power-query"], ""),

  # .NET
  Skill(".NET", [ver1(".net"), "dotnet", "dot.net"], "Cross-platform, open source dev. platform"),

  Skill("ASP.NET", ["asp.net", "asp"], ".NET-based web framework that allows to build dynamic sites, applications and services"),
  Skill("ML.NET", ["ml.net"], "ML framework for .NET"),
  Skill(".NET MAUI", [".net maui", "maui"], "Multi-platform app UI, evolution of Xamarin.Forms"),
  Skill("Blazor", ["blazor"], ".NET-based framework to create fullstack apps"),
  Skill("Unity", ["unity-engine", "unity-platform", "unity=3d", propn("unity")], "Gamedev engine"),
  Skill("Unity", ["unity"], disambiguate=ctxn),
  Skill("WCF", ["wcf"], ""),
  Skill("WPF", ["wpf"], ""),
  Skill("Xamarin", ["xamarin"], "Cross-platform and mobile app development"),

  # SUSPENDED
  # Mono -- non-Windows runtime, acquired together with Xamarin, essentialy a part of .NET now
  # Entity Framework -- ORM for .NET

  # AZURE
  Skill("Microsoft-Azure", ["microsoft-azure", "azure"], ""),
  Skill("Azure-Databricks", ["azure-databricks"], ""), # uses Apache-Spark | unified, open analytics platform for building, deploying, sharing, and maintaining EE data
  Skill("Azure-DataExplorer", ["azure-data=explorer", propn("adx")], ""), # big data platform optimized for analytical queries
  Skill("Azure-CosmosDB", ["azure-cosmosdb"], ""), # noSQL + relational DB
  Skill("Azure-IoT", ["azure-iot"], ""), # IoT platform
  Skill("Azure-Kubernetes", ["azure-kubernetes-service", "azure-ks", "aks"], ""), # ~ Amazon-EKS
  Skill("Azure-Relay", ["azure-relay"], ""), # enables to securely expose services that run in corporate network to the public cloud
  Skill("Azure-SQL", ["azure-sql"], ""), # Managed Cloud Database Service
  Skill("Azure-Synapse", ["azure-synapse"], ""), # service that brings together enterprise data warehousing and bigdata analytics

  # Azure Blob Storage (= AWS S3)
  # Azure Cognitive
  # Azure Container Instances (ACI)
  # Azure DevOps
  # Azure Files (= AWS EFS)
  # Azure Functions -- AWS Lambda
  # Azure Kubernetes Service (AKS)
  # Azure Managed Disks (= AWS EBS)
  # Azure Pipelines

  # HARDWARE
  Skill("ARM", [propn("arm"), noun("ARM")], "CPU family"),
  Skill("ARM", ["arm"], disambiguate=neighbour(2)),
  Skill("ARM32", ["aarch32", "arm32"], "CPU"),
  Skill("ARM64", ["aarch64", "arm64"], "CPU"),
]
