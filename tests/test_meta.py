"""
Test GroupsSegment class.
"""
import sys
from pathlib import Path
from pprint import pprint

from sis_meta import Meta

meta = Meta()
groups_segment = meta.manage_groups()

# Praat > TextGrid
groups_segment.insert('TextGrid')
groups_segment.insert('Rolando', 'TextGrid')
groups_segment.insert('José Roberto', 'TextGrid')
groups_segment.insert('Aaron', 'TextGrid')

# Adobe Audition > XMP
groups_segment.insert('Adobe Audition')
groups_segment.insert('José Roberto','Adobe Audition')
groups_segment.insert('Miguel', 'Adobe Audition')
groups_segment.insert('Juan', 'Adobe Audition')
groups_segment.insert('Luis', 'Adobe Audition')

meta.insert_guide_mark('TextGrid/José Roberto', 0.31131, 20.32233, 'Hoooooola')
meta.insert_guide_mark('TextGrid/Rolando', 1.31222, 3.23, 'Hola')
meta.insert_guide_mark('TextGrid/Aaron', 4.2323, 10.32, '¿Cómo te va?')
meta.insert_guide_mark('TextGrid/José Roberto', 9.31222, 3.23, 'Bien, todo tranqui')
meta.insert_guide_mark('TextGrid/Aaron', 15.31222, 3.23, 'Ah ya qué bueno')


meta.insert_guide_mark('Adobe Audition/José Roberto', 13.31222, 3.23, 'jejeje')
meta.insert_guide_mark('Adobe Audition/Luis', 15.31222, 3.23, 'jajaja')

meta.write('sound.wav.meta')
