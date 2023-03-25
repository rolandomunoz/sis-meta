"""
Read meta files.
"""
import sys
from pathlib import Path
sis_meta_path = str(Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, sis_meta_path)
import sis_meta

data_dir = Path(__file__).parent / 'data'
for meta_path in data_dir.glob('*.meta'):
    meta = sis_meta.read_from_file(meta_path)

    print(meta_path.name)
    for mark in meta:
        print(mark)
    print()
