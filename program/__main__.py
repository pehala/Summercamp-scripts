import argparse
import datetime
import locale
import logging
import pathlib
from functools import partial

from base import is_file_path
from base.google_api import GoogleSpreadsheetLoader
from program.entity import DayPart, Day, ProgramType
from program.markdown import header, list_item, centered_header, Table, force_page_break

SUMMARY_RANGE = "'Přehled'!B2:E15"
SHEET_PREFIX="den "
DAY_PARTS = {"Dopo", "Odpo", "Večer"}

locale.setlocale(locale.LC_ALL, 'cs_CZ.UTF-8')
logger = logging.getLogger(__name__)

def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Overview generator")
    parser.add_argument("spreadsheet_id", type=str, help="Google spreadsheet ID with data to based cards on")
    parser.add_argument(
        "-s",
        "--secret",
        type=is_file_path,
        metavar="secret",
        default="client_secret.json",
        help="Path to the secret file, see https://developers.google.com/identity/openid-connect/openid-connect",
    )
    parser.add_argument(
        "-o", "--output", type=pathlib.Path, metavar="output", help="Output directory", default="output/"
    )
    parser.add_argument("--date", "-d", type=datetime.date.fromisoformat, required=True)

    # parse the arguments from standard input
    return parser.parse_args()


def main():
    args = parse_cli_arguments()

    output = args.output
    output.mkdir(parents=True, exist_ok=True)

    loader = GoogleSpreadsheetLoader(client_secret_path=args.secret)
    sheets = loader.get_spreadsheet(spreadsheet_id=args.spreadsheet_id)["sheets"]
    get_range = partial(loader.get_spreadsheet_range, args.spreadsheet_id)
    day_names = [sheet["properties"]["title"] for sheet in sheets if sheet["properties"]["title"].startswith(SHEET_PREFIX)]

    days = []
    # Summary parsing will be here
    date = args.date
    summary_raw = loader.get_spreadsheet_range(args.spreadsheet_id, SUMMARY_RANGE)
    for number, row in enumerate(summary_raw):
        days.append(Day.from_row(row, date, number + 1, day_names[number]))
        date = date + datetime.timedelta(days=1)


    for day in days:
        rows = get_range(f"'{day.sheet_name}'!A1:I8")
        for i in range(3):
            start = (i*3)
            day_part_name = rows[start][0].split(":")[0].strip()
            if not day_part_name:
                logger.warning(f"{i+1} part of the day not found for sheet {day.sheet_name}")
                continue

            values = {key: value.strip() for key, value in zip(rows[start][1:-1], rows[start+1][1:-1]) if value.strip()}
            day_part = DayPart(name=day_part_name,
                          values=values,
                          cth=rows[start+1][-1] == "TRUE")
            day.parts[ProgramType(day_part_name)] = day_part

    result = ""
    summary_table = Table(headers=["Den", "Fyzická/Psychická", "Dopo", "Odpo", "Večer", "Garanti"])
    for day in days:
        summary_table.add_row([
            day.get_week_day(),
            f"{day.physical}/{day.psychical}",
            day.get_specific_value(ProgramType.MORNING, "Název") or "",
            day.get_specific_value(ProgramType.AFTERNOON, "Název") or "",
            day.get_specific_value(ProgramType.EVENING, "Název") or "",
            day.guarantees
        ])
#         result += f"""
# <div style="display: flex;justify-content: space-between;">
#   <h4 style="align-self: end">{day.date.strftime('%d.%m.%Y')}</h4>
#   <h1 style="align-self: end">{day.sheet_name}</h1>
#   <h4 style="align-self: end">{day.guarantees}</h4>
# </div>\n
# """
        result += f"""
<h1 style="text-align: center">{day.sheet_name} - {day.date.strftime('%d.%m.%Y')}</h1>
<p style="text-align: center"><b>{day.guarantees}</b></p>\n
"""
        for program_type, day_part in day.parts.items():
            if day_part.values:
                heading = f"{program_type.value} (CTH)" if day_part.cth else program_type.value
                result += header(level=3, text=heading)
                for key, value in day_part.values.items():
                    formatted_value = value.replace("\n", "<br>").strip()
                    result += list_item(f"**{key}**: {formatted_value}\n")

    with open(output.joinpath("summary.md"), "w") as file:
        file.write(centered_header(level=1, text="Přehled") + summary_table.as_markdown() + result)


if __name__ == "__main__":
    main()
