import unittest

from sis_meta import Meta

meta = Meta()

# Manage groups
meta.insert_group('TextGrid')
meta.insert_group('TextGrid/Rolando')
meta.insert_group('TextGrid/Aarón')
meta.insert_group('TextGrid/Javier')

# Insert marks
meta.insert_guide_mark('TextGrid/Javier', 1.753, 2.242, 'Aló')
meta.insert_guide_mark('TextGrid/Aarón', 3.2424, 2.853, 'hola')
meta.insert_guide_mark('TextGrid/Rolando', 5.753, 3.242, 'Estaba pensando en ir')
meta.insert_guide_mark('TextGrid/Aarón', 8.753, 10.242, 'Ahm...')

meta.update_group('TextGrid/Rolando', 'Rolo')
meta.update_group('TextGrid/Javier', 'Javi')

meta.remove_group('TextGrid/Javi')
meta.remove_group('TextGrid/Rolo')
meta.remove_group('TextGrid/Aarón')

for mark in meta:
    print(mark)

print(len(meta))
meta.write('holi.meta')
