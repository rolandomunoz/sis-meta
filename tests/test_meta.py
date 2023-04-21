"""
Test GroupsSegment class.
"""
import sys
from pathlib import Path
from pprint import pprint

from sis_meta import Meta

meta = Meta()
groups_segment = meta.manage_groups_segment()
groups_segment.insert('TextGrid')
groups_segment.insert('Rolando', 'TextGrid')
groups_segment.insert('Aaron', 'TextGrid')

meta.insert_guide_mark('Speakers/M1', 0.31131, 20.32233, 'Hoooooola')
meta.insert_guide_mark('Speakers/M2', 1.31222, 3.23, 'Hola')
meta.insert_guide_mark('Speakers/M1', 4.2323, 10.32, '¿Cómo te va?')
meta.insert_guide_mark('Speakers/M2', 9.31222, 3.23, 'Bien, todo tranqui')
meta.insert_guide_mark('Speakers/M1', 15.31222, 3.23, 'Ah ya qué bueno')

meta.write('sound.wav.meta')