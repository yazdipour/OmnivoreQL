from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateLabelInput:
    name: str
    color: str
    description: Optional[str] = None
