import unittest

from sis_meta import Meta

meta = Meta()

# Manage groups
groups = meta.manage_groups()
groups.insert('TextGrid')
groups.insert('Rolando', 'TextGrid')
groups.insert('Aarón', 'TextGrid')

# Insert marks
meta.insert_guide_mark('TextGrid/Rolando', 1.753, 2.242, 'Aló')
meta.insert_guide_mark('TextGrid/Aarón', 3.2424, 2.853, 'hola')
meta.insert_guide_mark('TextGrid/Rolando', 5.753, 3.242, 'Estaba pensando en ir')
meta.insert_guide_mark('TextGrid/Aarón', 8.753, 10.242, 'Ahm...')
