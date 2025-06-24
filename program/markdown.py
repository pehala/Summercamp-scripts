"""Markdown utilities"""


def header(level: int, text: str) -> str:
    """Generate a Markdown header."""
    return f"{'#' * level} {text}\n"


def centered_header(level: int, text: str) -> str:
    """Generate a Markdown header."""
    return f"<h{level} style='text-align: center;'>{text}</h{level}>\n\n"


def list_item(text: str) -> str:
    """Generate a Markdown list item."""
    return f"* {text}\n"


def force_page_break() -> str:
    """Generate a Markdown page break."""
    return "<div style='page-break-after: always;'></div>\n"


class Table:
    """Generate a Markdown table."""

    def __init__(self, headers: list[str]):
        self.headers = headers
        self.rows = []

    def add_row(self, row: list[str]) -> None:
        """Add a row to the table."""
        if len(row) != len(self.headers):
            raise ValueError("Row length does not match header length.")
        self.rows.append(row)

    def as_markdown(self) -> str:
        """Convert the table to Markdown format."""
        header_row = "| " + " | ".join(self.headers) + " |\n"
        separator_row = "| " + " | ".join([":---:"] * len(self.headers)) + " |\n"
        data_rows = "\n".join("| " + " | ".join(row) + " |" for row in self.rows)
        return header_row + separator_row + data_rows + "\n"
