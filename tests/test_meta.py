import unittest

from sis_meta import Meta

meta = Meta()

# Manage groups
meta.insert_group('Praat')
meta.insert_group('Praat/Rolando', color= (255, 255, 255), userparam = 0, hotkey = 'a')
meta.insert_group('Praat/Aarón', color= (8, 7, 10))
meta.insert_group('Praat/Javier', color= (200, 100, 100))
meta.insert_group('Praat/Maxi', color= (150, 123, 31))

# Insert marks
meta.insert_guide_mark('Praat/Javier', 1.753, 2.242, 'Aló')
meta.insert_guide_mark('Praat/Aarón', 3.2424, 2.853, 'hola')
meta.insert_guide_mark('Praat/Rolando', 5.753, 3.242, 'Estaba pensando en ir')
meta.insert_guide_mark('Praat/Aarón', 8.753, 10.242, 'Ahm...')
meta.insert_guide_mark('Praat/Maxi', 8.753, 10.242, 'Ahm...')

#meta.update_group('Praat/Rolando', 'Rolo')
#meta.update_group('Praat/Javier', 'Javi')

#meta.remove_group('Praat/Javi')
#meta.remove_group('Praat/Rolo')
#meta.remove_group('Praat/Aarón')

for mark in meta:
    print(mark)

print(len(meta))
meta.write('sound.wav.meta')
