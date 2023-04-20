"""
Parse GROUPS_SEGMENT into a list of dict. 
"""
import re

GROUP = re.compile(rb'''ID; (?P<id>\d+)

NAME; (?P<name>.+)

COLOR; (?P<color>\d+)

HOTKEY; (?P<hotkey>\d+)

USERPARAM; (?P<userparam>\d+)

'''
)
GROUP_OPEN = re.compile(rb'GROUP(\d+); BEGIN; COMPOSITE;BINARY;(\d+)\n')
#GROUP_CLOSE = re.compile(rb'GROUP\d; END')
SUBGROUP_OPEN = re.compile(rb'SUBGROUPS; BEGIN; COMPOSITE;BINARY;\d+\n')
SUBGROUP_CLOSE = re.compile(rb'SUBGROUPS; END\n')

def discover_grouptree(data, tree):
    """
    Discover group tree structure recursively.

    Parameters
    ----------
    data : :class:`io.BufferedReader` or :class:`io.BytesIO`
        Binary stream.
    tree : list of dict
        It contains the mark groups info.

    Returns
    -------
    list of dict
        Returns the GROUPS_SEGMENT info.
    """
    while True:
        current_position = data.tell()
        line = data.readline()

        # Base case
        if line == b'': # When riching the end of the document
            break

        if GROUP_OPEN.match(line):
            current_position = data.tell()
            data_temp = data.read()

            if GROUP.match(data_temp):
                mark_group_content = GROUP.match(data_temp)
                dict_ = {
                    'id': int(mark_group_content.group('id').decode()),
                    'name': mark_group_content.group('name').decode(),
                    'color': mark_group_content.group('color').decode(),
                    'hotkey': mark_group_content.group('hotkey').decode(),
                    'userparam': mark_group_content.group('userparam').decode(),
                }
                tree.append(dict_)
                current_position+= len(mark_group_content.group(0))
            data.seek(current_position)

        # Recursive condition
        elif SUBGROUP_OPEN.match(line):
            tree[-1]['child'] = discover_grouptree(data, [])

        elif SUBGROUP_CLOSE.match(line):
            break

    return tree
