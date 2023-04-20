"""
Test GROUPS_SEGMENT serializing.
"""
import sys
from pathlib import Path
from pprint import pprint

from sis_meta.io._serialize_groups_segment import serialize_groups_segment
from sis_meta import GroupsSegment

groups_segment = GroupsSegment()
groups_segment_str = serialize_groups_segment(groups_segment.data)

with open('test-output.meta', 'w', newline = '\n') as file_text:
    file_text.write(groups_segment_str)
