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
    bytes_block = pack(f'=I{n_items}d', n_items, *positions)
    data = _update_meta(data, bytes_block, '{{ positions_size }}', '{{ positions }}')

    # LENGTHS
    bytes_block = pack(f'=I{n_items}d', n_items, *lengths)
    data = _update_meta(data, bytes_block, '{{ lengths_size }}', '{{ lengths }}')

    # IDS
    bytes_block = pack(f'=I{n_items}L', n_items, *ids)
    data = _update_meta(data, bytes_block, '{{ ids_size }}', '{{ ids }}')

    # TEXTS
    bytes_block = _norm_text(texts)
    data = _update_meta(data, bytes_block, data_tag = '{{ texts }}')

    # TEXT_ATTR_POSITIONS
    zeroes = [0]*n_items
    bytes_block = pack(f'=I{n_items}I', n_items, *zeroes)
    data = _update_meta(data, bytes_block, '{{ attr_size }}', '{{ text_attr_positions }}')

    # TEXT_ATTR_LENGTHS

    # TEXT_ATTR_TYPES

    # TEXT_ATTR_VALUES

    # Calc sizes
    match = MARKS_SEGMENT.match(data)
    data = data.replace(b'{{ marks_segment_size }}', str(len(match.group(1))).encode())

    match = MARKS_GROUPS_DATA.match(data)
    data = data.replace(b'{{ file_size }}', str(len(match.group(1))).encode())

    return data

def _norm_text(text_list):
    """
    Normalize texts in SIS format.

    Parameters
    ----------
    text_list : str
        A list of texts encoded in utf-8.

    Returns
    -------
    bytes
        A block of bytes containing the texts required in SIS format.

    Notes
    -----
    SIS does not allow some characters as texts:
        - Semicolons (``;``) are replaced by ``U+0002``
        - New lines (``\n``) are replaced by ``U+0003``
        - Empty characters (``''``) are replaced by ``_|!!|_nuse``
    """
    texts_bytes = [text.encode() for text in text_list]
    texts_bytes = [text.replace(b'\n', bytes.fromhex('02')) for text in texts_bytes] #Start of Text: U+0002
    texts_bytes = [text.replace(b';', bytes.fromhex('03')) for text in texts_bytes] #End of Text: U+0003
    texts_bytes = [b'_|!!|_nuse' if text == b'' else text for text in texts_bytes]
    return b';'.join(texts_bytes)

def _update_meta(data, bytes_block, size_tag = None, data_tag = None):
    """
    Update the content of the meta template.

    Parameters
    ----------
    data : bytes
        The content of the meta template.
    bytes_block : bytes
        The new data to be inserted in the tags.
    size_tag : str
        The name of the tag where the size of the data given bytes will be replaced
        with. The size is calculated automatically from the ``byte_blocks`` 
        parameter.
    data_tag : str
        The name of the tag where the ``byte_blocks`` will be replaced with.

    Returns
    -------
    bytes
        A new version of the ``data`` parameter where values in tags are 
        replaced with those in ``byte_blocks``.

    Notes
    -----
    These are the valid tags:
        {{ positions_size }}, {{ positions }}
        {{ ids_size }}, {{ ids }}
        {{ lengths_size }}, {{ lengths }}
        {{ attr_size }}, {{ text_attr_positions }}
    """
    if not size_tag is None:
        data = data.replace(size_tag.encode(), f'{len(bytes_block)}'.encode())
    if not data_tag is None:
        data = data.replace(data_tag.encode(), bytes_block)
    return data
