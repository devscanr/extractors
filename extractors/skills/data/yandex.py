from ..utils import Skill, contextual, contextual_or_neighbour

__all__ = ["SKILLS"]

ctx = contextual("Apache")
ctxn = contextual_or_neighbour(["Apache"], 2)

SKILLS: list[Skill] = [
  Skill("Yandex", ["yandex"], ""), # company (etc)

  Skill("ClickHouse", ["clickhouse"], ""),

  # CLOUD
  # Skill("?", ["yt"], ""), # many FPs
  Skill("YDB", ["ydb"], "Distributed SQL Database that combines high availability and scalability with strong consistency and ACID transactions."), # https://ydb.tech/
]
