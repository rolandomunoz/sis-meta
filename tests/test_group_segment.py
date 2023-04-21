"""
Test GroupsSegment class.
"""
import sys
from pathlib import Path
from pprint import pprint

import sis_meta

#meta_path = Path(sys.argv[1])
meta_path = None
groups_segment = sis_meta.GroupsSegment(meta_path)

# Insert
groups_segment.insert('TextGrid', '', 15)
groups_segment.insert('Luis', 'TextGrid', 15)
groups_segment.insert('Juan', 'TextGrid', 15)
groups_segment.insert('José Roberto', 'TextGrid', 15)
groups_segment.insert('Rolando', 'TextGrid', 15)

groups_segment.insert('Adobe Audition', '', 15)
groups_segment.insert('José Roberto', 'Adobe Audition', 15)
groups_segment.insert('José Roberta', 'Adobe Audition', 15)

# Update
groups_segment.update('TextGrid/Rolando', 'Rolo', 15, 3, 3)
groups_segment.update('TextGrid/Luis', 'Luis Alberto', 15, 3, 3)

# Remove
groups_segment.remove('Adobe Audition/José Roberto')

group_id = groups_segment.get_id('TextGrid/José Roberto')
print(group_id)

#print(groups_segment)
#pprint(groups_segment.data, sort_dicts = False)
