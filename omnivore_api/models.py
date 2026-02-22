from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CreateLabelInput:
    name: str = field(default="", metadata={"validate": lambda x: isinstance(x, str) and bool(x.strip())})
    color: str = field(default="", metadata={"validate": lambda x: isinstance(x, str) and bool(x.strip())})
    description: Optional[str] = None
