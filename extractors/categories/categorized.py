from dataclasses import dataclass
from typing import Literal

type Role = Literal["Dev", "Nondev", "Org", "Student"]

@dataclass
class Categorized:
  role: Role | None
  is_freelancer: bool | None
  is_lead: bool | None
  is_remote: bool | None
  is_hireable: bool | None
