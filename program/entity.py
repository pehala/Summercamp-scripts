from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


@dataclass
class DayPart:
    """
    Represents a part of the day with all its attributes.
    """
    name: str
    cth: bool
    values: dict[str, str]

class ProgramType(StrEnum):
    MORNING = "Dopo"
    AFTERNOON = "Odpo"
    EVENING = "Večer"

@dataclass
class Day:
    """
    Represents a complete program for the day
    """
    day_number: int
    date: datetime
    sheet_name: str
    guarantees: str
    theme: str
    physical: int
    psychical: int
    parts: dict[ProgramType, DayPart] = field(default_factory=dict)

    def get_display_name(self) -> str:
        """
        Returns a display name for the day, formatted as "Sheet Name - Theme"
        """
        return f"{self.sheet_name} ({self.date.strftime('%d.%m.')}) - {self.guarantees}"

    def get_week_day(self):
        """
        Returns the name of the day of the week
        """
        return self.date.strftime("%a")

    def get_specific_value(self, program_type: ProgramType, key: str) -> str | None:
        """
        Returns a specific value for the given program type and key.
        If the program type or key does not exist, returns None.
        """
        if program_type in self.parts:
            return self.parts[program_type].values.get(key, None)
        return None

    @classmethod
    def from_row(cls, row, date: datetime, number: int, sheet_name: str) -> "Day":
        return cls(
            day_number=number,
            date=date,
            sheet_name=sheet_name,
            physical=int(row[0]),
            psychical=int(row[1]),
            theme=row[2].strip(),
            guarantees=row[3]
        )