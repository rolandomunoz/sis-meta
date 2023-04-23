"""
Test GROUPS_SEGMENT parsing.
"""
import sys
from pathlib import Path
from pprint import pprint

from sis_meta.groups._parse import discover_grouptree

path = Path(sys.argv[1])

with open(path, 'rb') as raw_file:
    tree = discover_grouptree(raw_file, [])

pprint(tree, sort_dicts = False)
