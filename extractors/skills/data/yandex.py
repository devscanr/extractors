from ..skill import Skill
from ..utils import dis_context

dis_ctx = dis_context("yandex")

SKILLS: list[Skill] = [
  Skill("Yandex", ["yandex"], "Company"),

  Skill("ClickHouse", ["clickhouse"], ""),

  # CLOUD
  # Skill("?", ["yt"], ""), # many FPs
  Skill("YDB", ["ydb"], "Distributed SQL database with high availability, scalability, and strong consistency"), # https://ydb.tech/
]
