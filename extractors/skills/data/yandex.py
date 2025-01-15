from ..skill import Skill, Company, Tech
from ..utils import dis_context

dis_ctx = dis_context("yandex")

SKILLS: list[Skill] = [
  Company("Yandex", ["(@)yandex"], "Company"),

  Tech("ClickHouse", ["clickhouse"]),

  # CLOUD
  # Skill("?", ["yt"], ""), # many FPs
  Tech("YDB", ["ydb"], "Distributed SQL database with high availability, scalability, and strong consistency"), # https://ydb.tech/
]
