"""
Serialize MARKS_SEGMENT
"""
from sis_meta.meta import Meta
from sis_meta.io._serialize_marks_segment import serialize_marks_segment

meta = Meta()
meta = Meta()
groups_segment = meta.manage_groups_segment()
groups_segment.insert('TextGrid')
groups_segment.insert('Rolando', 'TextGrid')
groups_segment.insert('Aaron', 'TextGrid')

meta.insert_guide_mark('Speakers/M1', 0.31131, 20.32233, '1')
meta.insert_guide_mark('TextGrid/Rolando', 1.31222, 3.23, 'Hola')
meta.insert_guide_mark('TextGrid/Aaron', 4.2323, 10.32, '¿Cómo te va?')
meta.insert_guide_mark('TextGrid/Rolando', 9.31222, 3.23, 'Bien, todo tranqui')

marks_segment = serialize_marks_segment(meta)
print(marks_segment)
