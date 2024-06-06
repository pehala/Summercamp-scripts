import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property
from typing import Iterable, Self, Optional
from xml.sax.saxutils import escape

from svg import Symbol, Text, Rect, Path, TSpan

from base import generate_tspans
from base.range_dict import RangeKeyDict
from base.text_utils import text_to_id


class EquipmentType(StrEnum):
    HEAD = "Helma"
    ARM = "Ruka"
    BODY = "Tělo"
    MODIFIER = "Bonus"


EQUIPMENT_RARITY = {"1": "grey", "2": "green", "3": "blue", "4": "#DA70D6", "5": "yellow"}
DIFFICULTY = RangeKeyDict(
    {
        (1, 5): "Lehký",
        (5, 10): "Střední",
        (10, 15): "Těžké",
        (15, 20): "Smrtící",
        (20, 30): "Brutální",
        (30, 35): "Ničitel světů",
    }
)


@dataclass(eq=True, frozen=True)
class BaseEntity(ABC):
    amount: int

    @classmethod
    @abstractmethod
    def from_list(cls, raw_data: Iterable) -> Self:
        """Creates entity from raw_data from SpreadSheet"""

    @cached_property
    @abstractmethod
    def symbol(self) -> Symbol:
        """Creates SVG symbol that can be in used in defs"""


@dataclass(eq=True, frozen=True)
class Equipment(BaseEntity):
    name: str
    bonus: int
    type: EquipmentType
    condition: Optional[str]

    @classmethod
    def from_list(cls, raw_data: list) -> Self:
        return cls(
            name=raw_data[0],
            bonus=raw_data[1],
            type=EquipmentType(raw_data[2]),
            condition=raw_data[3] or None,
            amount=int(raw_data[4]),
        )

    @cached_property
    def symbol(self) -> Symbol:
        elements = [
            Rect(
                x=0.5,
                y=0.5,
                width="79",
                height="29",
                fill="none",
                stroke="#000000",
                stroke_width=1,
            ),
            Text(
                x="50%",
                y=10,
                text_anchor="middle",
                dominant_baseline="middle",
                class_=["normal"],
                text=self.name,
            ),
            Text(
                x=35,
                y=20,
                dominant_baseline="middle",
                class_=["big"],
                text=f"+{self.bonus}",
            ),
            Text(
                x=75,
                y=26,
                text_anchor="end",
                dominant_baseline="middle",
                class_=["small"],
                text=self.type,
            ),
            Path(d="M 16,3 62,3", stroke_width=1, stroke=EQUIPMENT_RARITY[self.bonus]),
        ]
        if self.condition:
            elements.append(
                Text(
                    x=2,
                    y=26,
                    dominant_baseline="middle",
                    class_=["small"],
                    text=escape(self.condition),
                )
            )
        symbol = Symbol(id=text_to_id(self.name), elements=elements, viewBox="0 0 80 30")
        return symbol


@dataclass(eq=True, frozen=True)
class Monster(BaseEntity):
    name: str
    level: int

    @classmethod
    def from_list(cls, raw_data: list) -> Self:
        return cls(
            name=raw_data[0],
            level=int(raw_data[1]),
            amount=int(raw_data[2]),
        )

    @cached_property
    def symbol(self) -> Symbol:
        elements = [
            Rect(
                x=0.5,
                y=0.5,
                width="79",
                height="29",
                fill="none",
                stroke="#000000",
                stroke_width=1,
            ),
            Text(
                x="50%",
                y=5,
                text_anchor="middle",
                dominant_baseline="middle",
                class_=["normal"],
                text=self.name,
            ),
            Text(
                x=40,
                y=15,
                text_anchor="middle",
                dominant_baseline="middle",
                class_=["big"],
                text=str(self.level),
            ),
            Text(
                x=50,
                y=15.5,
                dominant_baseline="middle",
                class_=["small"],
                text="Úroveň",
            ),
            Text(
                x=40,
                y=28,
                text_anchor="middle",
                class_=["small"],
                text=DIFFICULTY[self.level],
            ),
        ]
        symbol = Symbol(id=text_to_id(self.name), elements=elements, viewBox="0 0 80 30")
        return symbol


@dataclass(eq=True, frozen=True)
class Curse(BaseEntity):
    name: str
    description: str

    @classmethod
    def from_list(cls, raw_data: list) -> Self:
        return cls(
            name=raw_data[0],
            description=raw_data[1],
            amount=int(raw_data[2]),
        )

    @cached_property
    def symbol(self) -> Symbol:
        elements = [
            Rect(
                x=0.5,
                y=0.5,
                width="79",
                height="29",
                fill="none",
                stroke="#000000",
                stroke_width=1,
            ),
            Text(
                x=40,
                y=10,
                text_anchor="middle",
                class_=["big"],
                text="KLETBA",
            ),
            Text(
                x=40,
                y=13,
                text_anchor="middle",
                dominant_baseline="middle",
                class_=["normal"],
                font_weight="bold",
                text=self.name,
            ),
            Text(x=5, y=16, elements=generate_tspans(self.description, 35, dy=4, x=5, class_=["small"])),
        ]
        symbol = Symbol(id=text_to_id(self.name), elements=elements, viewBox="0 0 80 30")
        return symbol


@dataclass(eq=True, frozen=True)
class Bonus(BaseEntity):
    DESCRIPTION = "Lze použít jen jednou, musí být v batohu"
    name: str
    bonus: int

    @classmethod
    def from_list(cls, raw_data: list) -> Self:
        return cls(
            name=raw_data[0],
            bonus=int(raw_data[1]),
            amount=int(raw_data[3]),
        )

    @cached_property
    def symbol(self) -> Symbol:
        spans = []
        for line in textwrap.wrap(self.DESCRIPTION, 35):
            spans.append(TSpan(text=line, dy=4, x=5, class_=["small"]))
        elements = [
            Rect(
                x=0.5,
                y=0.5,
                width="79",
                height="29",
                fill="none",
                stroke="#000000",
                stroke_width=1,
            ),
            Text(
                x=40,
                y=13,
                text_anchor="middle",
                class_=["big"],
                text=f"BONUS +{self.bonus}",
            ),
            Text(
                x=40,
                y=17,
                text_anchor="middle",
                dominant_baseline="middle",
                class_=["normal"],
                font_weight="bold",
                text=self.name,
            ),
            Text(x=5, y=19, class_=["small"], elements=spans),
            Path(d="M 16,3 62,3", stroke_width=1, stroke=EQUIPMENT_RARITY[str(self.bonus)]),
        ]
        symbol = Symbol(id=text_to_id(self.name), elements=elements, viewBox="0 0 80 30")
        return symbol
