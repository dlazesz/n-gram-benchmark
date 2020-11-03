#!/usr/bin/env python3

import argparse
from lorem_text import lorem

parser = argparse.ArgumentParser()
parser.add_argument(
    '--words', '-w',
    help='Number of dummy words',
    type=int)

args = parser.parse_args()
print(lorem.words(args.words))
