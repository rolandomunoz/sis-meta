"""
Read meta files.
"""
import re
import struct
from sis_meta import meta

POSITIONS = re.compile(rb'\nPOSITIONS; BEGIN; VECTOR_DOUBLE;BINARY;(\d+)\n(.+)\nPOSITIONS; END', re.DOTALL)
IDS = re.compile(rb'\nIDS; BEGIN; VECTOR_INT;BINARY;(\d+)\n(.+)\nIDS; END', re.DOTALL)
LENGTHS = re.compile(rb'\nLENGTHS; BEGIN; VECTOR_DOUBLE;BINARY;(\d+)\n(.+)\nLENGTHS; END', re.DOTALL)
TEXTS_LONG = re.compile(rb'\nTEXTS; BEGIN; VECTOR_STRING\n(.+)\nTEXTS; END\n', re.DOTALL)
TEXTS_SHORT = re.compile(rb'\nTEXTS; (.+)\n\nTEXT_ATTR_POSITIONS; BEGIN;', re.DOTALL)
HEAD = re.compile(rb'\nID; (\d+?)\n\nNAME; (.+?)\n\n', re.DOTALL)
HEAD_NEW = re.compile(
    rb'(?P<group>GROUP\d+); BEGIN; .+?\n'
    rb'ID; (?P<id>\d+)\n\n'
    rb'NAME; (?P<name>.+?)\n\n'
    rb'COLOR; (?P<color>\d+?)\n\n'
    rb'HOTKEY; (?P<hotkey>\d+?)\n\n'
    rb'USERPARAM; (?P<userparam>\d+?)\n\n\n'
    rb'GROUP\d+?; END\n'
)

def read_from_file(path):
    """
    Read a meta file into a :class:`Meta`.

    Parameters
    ----------
    path : str or path-like object
        The path of meta file.

    Returns
    -------
    :class:`sis_meta.Meta`
        An object that contains marks.
    """
    meta_obj = meta.Meta()
    meta_obj.data = _parse_file(path)
    return meta_obj

def _parse(content):
    """
    Parse MARKS_SEGMENT.

    Parameters
    ----------
    content : bytes
        The content of a meta file

    Returns
    -------
    zip of tuples, [(position, length, text, group_id, group_name), ...]
        A zip of tuples. Each tuple contains the start position,
        length, text, group_id and group_name of a mark.
    """
    # Get the group names
    head_dict = {}
    head = HEAD.findall(content)
    for group_id, group_name in head:
        head_dict[group_id.decode()] = group_name.decode()

    # Read positions
    positions_match = POSITIONS.search(content)
    #position_size = positions_match.group(1)
    positions_bytes = positions_match.group(2)[4:]
    positions = struct.unpack(f'{len(positions_bytes) // 8}d', positions_bytes)

    # Read ids / also known as groups
    ids_match = IDS.search(content)
    #ids_size = ids_match.group(1)
    ids_bytes = ids_match.group(2)[4:]
    group_ids = struct.unpack(f'{len(ids_bytes) // 4}i', ids_bytes)
    group_names = [head_dict[str(group_id)] for group_id in group_ids]

    # Read lengths
    lengths_match = LENGTHS.search(content)
    #lengths_size = lengths_match.group(1)
    lengths_bytes = lengths_match.group(2)[4:]
    lengths = struct.unpack(f'{len(lengths_bytes) // 8}d', lengths_bytes)

    # Read texts
    texts_match = TEXTS_LONG.search(content)
    if texts_match is None:
        texts_match = TEXTS_SHORT.search(content)
    texts_bytes = texts_match.group(1)
    texts = []
    for text_bytes in texts_bytes.split(b';'):
        text_bytes = text_bytes.replace(bytes.fromhex('02'), b'\n') #Start of Text: U+0002
        text_bytes = text_bytes.replace(bytes.fromhex('03'), b';') #End of Text: U+0003
        text_bytes = text_bytes.replace(b'_|!!|_nuse', b'') #End of Text: U+0003
        texts.append(text_bytes.decode())
    return zip(positions, lengths, texts, group_ids, group_names)

def _parse_groups_segment(content):
    """
    Parse GROUPS_SEGMENT into a dict.

    Parameters
    ----------
    content : bytes
        The content of a meta file
    """
    dict_ = {}
    for group in HEAD_NEW.findall(content):
        print(group)
        group_id = int(group[1].decode())
        dict_[group_id] = {
            'group_name': group[2],
            'group_color': group[3],
            'hotkey': group[4],
            'userparam': group[5],
        }
    return dict_

def _parse_file(path):
    """
    Get the marks in a meta file.

    Parameters
    ----------
    path : path-like
        The path of a meta file.

    Returns
    -------
    list of dicts, [
        {
        position: double, 
        length: double, 
        text: str, 
        group_id: int,
        group_name: str
        },
        .
        .
        .
        ]
        A list of dictionaries. Each dictionary contains the start
        position, length, text, group_id and group_name.
    """
    with open(path, 'rb') as metafile:
        content = metafile.read()
    list_ = []
    for mark in _parse(content):
        guide_mark = meta.GuideMark(
            mark[0], # position
            mark[1], # length
            mark[2], # text
            mark[3], # group_id
            mark[4], # group_name
        )
        list_.append(guide_mark)
    return list_
