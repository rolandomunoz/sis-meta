"""
Test GROUPS_SEGMENT serializing.
"""
import sys
from pathlib import Path
from pprint import pprint

from sis_meta.io._serialize_groups_segment import serialize_groups_segment
from sis_meta import GroupsSegment

groups_segment = GroupsSegment()
serialize_groups_segment(groups_segment.data)

#pprint(tree, sort_dicts = False)
