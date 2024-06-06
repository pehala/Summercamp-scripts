import argparse
import os
import textwrap

from svg import TSpan


def is_directory_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def is_file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid file")


def generate_tspans(text, width, **kwargs) -> list[TSpan]:
    spans = []
    for line in textwrap.wrap(text, width):
        spans.append(TSpan(text=line, **kwargs))
    return spans
