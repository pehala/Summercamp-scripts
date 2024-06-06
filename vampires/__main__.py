import argparse
import pathlib
from glob import glob
from itertools import islice
from textwrap import dedent

from svg import SVG, Style, Line, Text

from base import is_file_path, generate_tspans
from base.google_api import GoogleSpreadsheetLoader
from base.pdf import convert_list
from vampires.entity import Person

RANGE = "'zaklinadlo'!A2:F"


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Vampires lineage card generator")
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
        "-o", "--output", type=pathlib.Path, metavar="output", help="Output directory", default="output/vampires"
    )

    # parse the arguments from standard input
    return parser.parse_args()


def create_svg():
    svg = SVG(elements=[], width="210mm", height="297mm", viewBox="0 0 210 297")
    svg.elements.append(
        Style(
            text=dedent(
                """
                        .small { font: 3.88056px sans-serif; }
                        .normal { font: 9px sans-serif; }
                        .big { font: 10.5833px sans-serif; }
                        .dashed { stroke-width: 1; stroke-dasharray: 0.5; stroke: black; }
                        .line { stroke-width: 2; stroke: black;}
                    """
            ),
        )
    )
    return svg


def main():
    args = parse_cli_arguments()

    output = args.output
    output.mkdir(parents=True, exist_ok=True)

    loader = GoogleSpreadsheetLoader(client_secret_path=args.secret)
    people = [Person.from_list(value) for value in loader.get_spreadsheet(args.spreadsheet_id, RANGE)]
    people.sort(key=lambda x: x.position)

    # Create Double-linked linked list
    previous = people[0]
    for person in islice(people, 1, None):
        person.before = previous
        previous.after = person
        previous = person

    person = people[0]
    while person.after is not None:
        front_page = create_svg()
        elements = [
            Line(y1="148.5", y2="148.5", x1=0, x2=210, class_=["dashed"]),
            Line(y1="178.5", y2="178.5", x1=0, x2=210, class_=["line"]),
            Line(y1=297, y2="178.5", x1=70, x2=70, class_=["line"]),
            Line(y1=297, y2="178.5", x1=140, x2=140, class_=["line"]),
            Text(
                y=190,
                x=105,
                text_anchor="middle",
                class_=["big"],
                text="Slovo",
            ),
            Text(
                y=190,
                x=35,
                text_anchor="middle",
                class_=["big"],
                text="Před",
            ),
            Text(
                y=190,
                x=175,
                text_anchor="middle",
                class_=["big"],
                text="Po",
            ),
            Text(
                y=237,
                x=105,
                text_anchor="middle",
                class_=["normal"],
                text=person.word,
            ),
        ]
        if person.before:
            elements.append(
                Text(
                    y=233,
                    x=35,
                    text_anchor="middle",
                    elements=generate_tspans(person.before.info_before.capitalize(), 30, dy=4, x=35, class_=["small"]),
                ),
            )
        if person.after:
            elements.append(
                Text(
                    y=233,
                    x=175,
                    text_anchor="middle",
                    dominant_baseline="middle",
                    elements=generate_tspans(person.after.info_after.capitalize(), 30, dy=4, x=175, class_=["small"]),
                ),
            )
        front_page.elements.extend(elements)
        with open(output.joinpath(f"front{person.position}.svg"), "w") as file:
            file.write(front_page.as_str())

        cover_page = create_svg()
        elements = [
            Line(y1="178.5", y2="178.5", x1=0, x2=210, class_=["dashed"]),
            Line(y1="148.5", y2="148.5", x1=0, x2=210, class_=["dashed"]),
            Text(
                y=233,
                x=105,
                text_anchor="middle",
                dominant_baseline="text-bottom",
                class_=["big"],
                text=person.name,
            ),
        ]
        cover_page.elements.extend(elements)
        with open(output.joinpath(f"cover{person.position}.svg"), "w") as file:
            file.write(cover_page.as_str())

        person = person.after
    paths = glob(str(output.joinpath("*.svg")))
    convert_list(paths, str(output.joinpath("output.pdf")))


if __name__ == "__main__":
    main()
