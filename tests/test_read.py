"""
Read meta files.
"""
import sys
from pathlib import Path

from sis_meta import read_from_file

meta_path_in = Path(__file__).parent / 'data' / 'sound3.wav.meta'
meta_path_out = meta_path_in.parent / f'{meta_path_in.stem}.metatest'

meta = read_from_file(meta_path_in)
meta.write(meta_path_out)
