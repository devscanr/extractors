from ..utils import Skill, contextual, contextual_or_neighbour

__all__ = ["SKILLS"]

ctx = contextual("Apache")
ctxn = contextual_or_neighbour(["Apache"], 2)

SKILLS: list[Skill] = [
  Skill("Yandex", ["yandex"], "Company"),

  Skill("ClickHouse", ["clickhouse"], ""),

  # CLOUD
  # Skill("?", ["yt"], ""), # many FPs
  Skill("YDB", ["ydb"], "Distributed SQL database with high availability, scalability, and strong consistency"), # https://ydb.tech/
]
