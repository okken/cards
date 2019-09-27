from dataclasses import dataclass, field, asdict
from typing import Union

@dataclass
class Card:
    summary: str = None
    owner: str = None
    done: bool = None
    id: int = field(default=None, compare=False)

@dataclass
class Filter:
    owner: str = None
    no_owner: Union[bool, None] = None
    done: Union[bool, None] = None

