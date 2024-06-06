from dataclasses import dataclass
from typing import Self, Optional


@dataclass
class Person:
    name: str
    position: int
    word: str
    info_before: str
    info_after: str
    before: Optional[Self] = None
    after: Optional[Self] = None

    @classmethod
    def from_list(cls, raw_data: list[str]):
        return cls(
            name=raw_data[0],
            position=int(raw_data[2]),
            word=raw_data[3],
            info_before=raw_data[4],
            info_after=raw_data[5],
        )
