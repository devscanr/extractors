from ...xpatterns import ver1, propn
from ..skill import Skill
from ..utils import dis_context, dis_neighbours

dis_ctx = dis_context("microsoft")

SKILLS: list[Skill] = [
  Skill("Microsoft", ["(@)microsoft"], "Company"),

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
  Skill("MS-365", ["365"], disambiguate=[
    dis_neighbours(),
    dis_context("microsoft", "office")
  ]),

  Skill("Power-Platform", ["power-platform"], ""),
  Skill("Power-Apps", ["power=apps"], ""),
  Skill("Power-Automate", ["power-automate"], ""),
  Skill("Power-BI", ["power=bi"], ""),
  Skill("Power-Pivot", ["power-pivot"], ""),
  Skill("Power-Query", ["power-query"], ""),

  # .NET
  Skill(".NET", [ver1(".net"), "dotnet", "dot.net"], "Cross-platform, open source dev. platform"),

  Skill("ASP.NET", ["asp.net", "asp"], ".NET-based web framework that allows to build dynamic sites, apps and services"),
  Skill("ML.NET", ["ml.net"], "ML framework for .NET"),
  Skill(".NET MAUI", [".net maui", "maui"], "Multi-platform app UI, evolution of Xamarin.Forms"),
  Skill("Blazor", ["blazor"], ".NET-based framework to create fullstack apps"),
  Skill("Unity", ["unity-engine", "unity-platform", "unity=3d"], "Gamedev engine"), # , propn("unity")
  Skill("Unity", ["unity"], disambiguate=[
    dis_neighbours(),
    dis_context("c#", "microsoft", "framework")
  ]),
  Skill("WCF", ["wcf"], "Windows Communication Foundation: framework for service-oriented apps"),
  Skill("WPF", ["wpf"], "Windows Presentation Foundation: UI framework for desktop apps"),
  Skill("Xamarin", ["xamarin"], "Cross-platform and mobile app development"),

  # SUSPENDED
  # Mono -- non-Windows runtime, acquired together with Xamarin, essentialy a part of .NET now
  # Entity Framework -- ORM for .NET

  # AZURE
  Skill("Microsoft-Azure", [
    "microsoft-azure", "azure",
    "log-analytics", "application-insights",
  ], ""),
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
  Skill("ARM", [
    "aarch32", "arm32",
    "aarch64", "arm64",
  ], "CPU family"),
  Skill("ARM", ["arm"], disambiguate=[
    dis_neighbours(),
    dis_context("microsoft", "cpu", "x86", "x32", "x64", "risc", "arc", "processor(s)")
  ]),
]
