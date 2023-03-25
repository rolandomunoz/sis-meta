"""
Read meta files.
"""
import sys
from pathlib import Path
sis_meta_path = str(Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, sis_meta_path)
import sis_meta

meta_path = Path(__file__).parent / 'data' / 'sound5.wav.meta'

# Test
positions = [1.64505565987125, 3.1312, 20.2901113197425, 31.3131, 40.3121434114]
lengths = [15.313, 10.322, 2.32322, 20.1221, 2]
ids = [6, 7, 8, 9, 8]
texts = ['Hola, me llamo Akuma', 'Yo me llamo Lala', 'miau', 'raul', 'abuela']

data = {
    'positions': positions,
    'lengths': lengths,
    'ids': ids,
    'texts': texts,
}
meta = sis_meta.write_meta_file(data, meta_path)
