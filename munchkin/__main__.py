import argparse
from glob import glob
from pathlib import Path
from textwrap import dedent

from svg import SVG, Defs, Use, Style

from .entity import Equipment, Monster, Curse, Bonus
from .utils import cluster, expand
from base import is_file_path
from base.google_api import GoogleSpreadsheetLoader
from base.pdf import convert_list

ROWS = 7
COLUMNS = 3

EQUIPMENT_RANGE = "'Vybavení'!B2:F"
MONSTER_RANGE = "'Příšerky'!B2:D"
CURSE_RANGE = "'Kletby'!B2:D"
BONUS_RANGE = "'Bonus'!B2:E"


def create_svg():
    svg = SVG(elements=[], width="297mm", height="210mm", viewBox="0 0 297 210")
    svg.elements.append(
        Style(
            text=dedent(
                """
                        .normal { font: 4.23333px sans-serif; }
                        .small { font: 3.88056px sans-serif; }
                        .big { font: 10.5833px sans-serif; }
                    """
            ),
        )
    )
    defs = Defs(elements=[])
    svg.elements.append(defs)
    return svg, defs


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Munchkin card generator")
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
        "-o", "--output", type=Path, metavar="output", help="Output directory", default="output/munchkin"
    )

    # parse the arguments from standard input
    return parser.parse_args()


def main():
    args = parse_cli_arguments()

    loader = GoogleSpreadsheetLoader(client_secret_path=args.secret)
    equipment = [
        Equipment.from_list(value) for value in loader.get_spreadsheet_range(args.spreadsheet_id, EQUIPMENT_RANGE)
    ]
    monsters = [Monster.from_list(value) for value in loader.get_spreadsheet_range(args.spreadsheet_id, MONSTER_RANGE)]
    curses = [Curse.from_list(value) for value in loader.get_spreadsheet_range(args.spreadsheet_id, CURSE_RANGE)]
    bonuses = [Bonus.from_list(value) for value in loader.get_spreadsheet_range(args.spreadsheet_id, BONUS_RANGE)]

    unique_entities = bonuses + monsters + equipment + curses
    entities = cluster(expand(unique_entities), ROWS * COLUMNS)

    output = args.output
    output.mkdir(parents=True, exist_ok=True)

    for count, paged_entities in enumerate(entities):
        svg, defs = create_svg()

        for entity in set(paged_entities):
            defs.elements.append(entity.symbol)

        x = 0
        y = 0
        for equipment in paged_entities:
            svg.elements.append(Use(href="#" + equipment.symbol.id, x=x * 80, y=y * 30, width=80, height=30))
            x += 1
            if x == COLUMNS:
                x = 0
                y += 1

        with open(output.joinpath(f"file{count}.svg"), "w") as file:
            file.write(svg.as_str())

    paths = glob(str(output.joinpath("*.svg")))
    convert_list(paths, str(output.joinpath("output.pdf")))


if __name__ == "__main__":
    main()
