"""
Write meta files.
"""
import re
from struct import pack
from importlib.resources import files

MARKS_SEGMENT = re.compile(
    rb'.+MARKS_SEGMENT; BEGIN;.+?(\n.+)\n\nMARKS_SEGMENT; END', re.DOTALL
)
MARKS_GROUPS_DATA = re.compile(
    b'MARKS_GROUPS_DATA; BEGIN;.+?(\n.+)\n\nMARKS_GROUPS_DATA; END', re.DOTALL
)

def write_meta_file(data, meta_path):
    """
    Write a meta file.

    Parameters:
    -----------
    data : {'positions': list of float, 'lengths': list of float,
        'ids': list of int, 'texts': list of str}
        The data needed for writing guide marks.
    meta_path : path-like object
        The path of the meta file.
    """
    meta = build_meta(
        data['positions'],
        data['lengths'],
        data['ids'],
        data['texts']
    )

    # Write file
    meta_path.write_bytes(meta)

def build_meta(positions, lengths, ids, texts):
    """
    Build the content of a meta file.

    Parameters
    -----------
    positions : list of float
        The starting point of the guide marks.
    lengths : list of float
        The duration of the guide marks.
    ids : list of int
        The group each guide mark belong to.
    texts : list of str
        The content of the guide marks.

    Returns
    -------
    bytes
        The content of a meta file.

    Notes
    -----
    The parameters must be equal in length. In the other hand, at this
    moment, ids are limited to the ones existing in the the template: 2
    , 3, 4, 6, 7, 8, 9, 10, 11 and 13. I recommmend to use only 6, 7, 8
    and 9. Those are M1, M2, F1 and F2 groups.

    TEXT_ATTR_POSITIONS, TEXT_ATTR_LENGTHS, TEXT_ATTR_TYPES and 
    TEXT_ATTR_VALUES seem to have the same attributes; so I decided to
    copy the values of TEXT_ATTR_POSITIONS on the other's parts.

    The lists pass as arguments must have the same lenght.
    """
    # Load template
    template_path = files('sis_meta.io') / 'template.meta'
    data = template_path.read_bytes()

    n_items = len(positions)

    # Replace values:
    # MARKS_SEGMENT
    # POSITIONS
    position_size = f'{n_items*8+4}'.encode()
    data = data.replace(b'{{ positions_size }}', position_size)

    bytes_line = pack('L', n_items) + pack(f'{n_items}d', *positions)
    data = data.replace(b'{{ positions }}', bytes_line)

    # LENGTHS
    lengths_size = f'{n_items*8+4}'.encode()
    data = data.replace(b'{{ lengths_size }}', lengths_size)

    bytes_line = pack('L', n_items) + pack(f'{n_items}d', *lengths)
    data = data.replace(b'{{ lengths }}', bytes_line)

    # IDS
    ids_size = bytes(f'{n_items*4+4}', 'utf-8')
    data = data.replace(b'{{ ids_size }}', ids_size)

    bytes_line = pack('L', n_items) + pack(f'{n_items}L', *ids)
    data = data.replace(b'{{ ids }}', bytes_line)

    # TEXTS
    texts_bytes = [text.encode() for text in texts]
    texts_bytes = [text.replace(b'\n', bytes.fromhex('02')) for text in texts_bytes] #Start of Text: U+0002
    texts_bytes = [text.replace(b';', bytes.fromhex('03')) for text in texts_bytes] #End of Text: U+0003
    texts_bytes = [b'_|!!|_nuse' if text == b'' else text for text in texts_bytes]
    bytes_line = b';'.join(texts_bytes)
    data = data.replace(b'{{ texts }}', bytes_line)

    # TEXT_ATTR_POSITIONS
    attr_size = bytes(f'{n_items*4+4}', 'utf-8')
    data = data.replace(b'{{ attr_size }}', attr_size)

    zeroes = [0]*n_items
    bytes_line = pack('I', n_items) + pack(f'{n_items}I', *zeroes)
    data = data.replace(b'{{ text_attr_positions }}', bytes_line)

    # TEXT_ATTR_LENGTHS

    # TEXT_ATTR_TYPES

    # TEXT_ATTR_VALUES

    # Calc sizes
    match = MARKS_SEGMENT.match(data)
    data = data.replace(b'{{ marks_segment_size }}', str(len(match.group(1))).encode())

    match = MARKS_GROUPS_DATA.match(data)
    data = data.replace(b'{{ file_size }}', str(len(match.group(1))).encode())

    return data
