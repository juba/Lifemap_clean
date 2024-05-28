#!/usr/bin/python

import os
from argparse import ArgumentParser
from pathlib import Path

LIFEMAP_DIRECTORY = Path("/usr/local/lifemap")

parser = ArgumentParser(
    description="Run all script to get have data ready to explore with Lifemap."
)
parser.add_argument(
    "--lang",
    nargs="?",
    help="Language chosen. FR for french, EN (default) for english",
    choices=["EN", "FR"],
)
parser.add_argument(
    "--simplify",
    nargs="?",
    help="Should the tree be simplified by removing environmental and unindentified species?",
    choices=["True", "False"],
)
args = parser.parse_args()

# write the options chosen to a parameters file for later updates with same options
with open(LIFEMAP_DIRECTORY / "TREEOPTIONS", "w") as f:
    f.write(f"""#!/bin/sh\nlang="{args.lang}"\nsimplify="{args.simplify}"\n""")
os.system(
    f"(cd /usr/local/lifemap/ ; sudo ./Main.py --lang {args.lang} --simplify {args.simplify})"
)
