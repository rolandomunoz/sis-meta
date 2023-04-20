"""
Class for handling MARKS_GROUP in meta file.
"""
import re
import io
from importlib.resources import files
from pprint import pprint

from sis_meta.io._parse_groups_segment import discover_grouptree

GROUPS_SEGMENT= re.compile(
rb'''MARKS_GROUPS_DATA; BEGIN; COMPOSITE;BINARY;\d+
VERSION; 2

GROUPS_SEGMENT; BEGIN; COMPOSITE;BINARY;\d+
(.+)
GROUPS_SEGMENT; END
''', re.DOTALL
)

class MarksGroup:
    """
    A class for handling MARKS_GROUP_DATA
    """
    def __init__(self, path= None):
        self.data = None

        if path is None:
            path = files('sis_meta.io.templates') / 'grouptree.meta'
            with open(path, 'rb') as raw_file:
                self.data = discover_grouptree(raw_file, [])
        else:
            with open(path, 'rb') as raw_file:
                match = GROUPS_SEGMENT.match(raw_file.read())
                if not match:
                    raise IOError(f'{path} is not a meta file.')
                self.data = discover_grouptree(
                    io.BytesIO(match.group(1)),
                    []
                )
        self.group_id = self._find_max_id(self.data)

    def _find_max_id(self, data):
        """
        Find the max group id in a MARK_GROUP tree.
        """
        for dict_ in data:
            max_value = dict_['id']
            if 'child' in dict_:
                current_value = self._find_max_id(dict_['child'])
                max_value = current_value if current_value > max_value else max_value
        return max_value

    def _find_mark_group(self, data, path):
        """
        Find a MARK_GROUP dict.
        """
        mark_group_name = path[0]
        mark_group_name_path = path[1:]

        # Base case
        if len(mark_group_name_path) == 0: # Each element in the path has been consumed
            for dict_ in data:
                if dict_['name'] == mark_group_name:
                    return dict_
            return None

        # Recursive case
        for dict_ in data:
            if not dict_['name'] == mark_group_name:
                continue

            if 'child' in dict_:
                return self._find_mark_group(dict_['child'], mark_group_name_path)

    @staticmethod
    def _norm_path(path):
        """
        Normalize a MARK_GROUP path.

        Parameters
        ----------
        path : str
            The path of a mark group.

        Returns
        -------
        str
            The normalized path.
        """
        if not path.startswith('All marks'):
            path = 'All marks' if path == '' else f'All marks/{path}'
        return path

    def is_path(self, path):
        """
        Check if the MARK_GROUP path exists.

        Parameter
        ---------
        path : str
            The path of a MARK_GROUP.

        Returns
        -------
        bool
            Return `True` if the path exists; otherwise, `False`.
        """
        path_list = self._norm_path(path).split('/')
        path_exists = self._find_mark_group(self.data, path_list)

        if path_exists is None:
            return False
        return True

    def insert(self, path, new_name, color=0, hotkey= 0, userparam=0):
        """
        Insert a mark group.

        Parameters
        ----------
        path : str
            The path of the MARK_GROUP.
        new_name : str
            The name of the new mark group.
        color : int, default 0
            A number representing the color. Unknown yet.
        hotkey : int, default 0
            A shortcut for inserting marks. Use ASCII table references
            to associate a number with a key. 0 means no association.
        userparam : int, default 0
            Unkown yet.

        Examples
        --------
        Insert `M3`, `M4`, `F3` and `F4` at the `Speakers` subgroup.

        >>> marks_group = sis_meta.MarksGroup()
        >>> marks_group.insert('TextGrid', 'Luis', 15)
        >>> marks_group.insert('TextGrid', 'Jorge')
        >>> marks_group.insert('TextGrid', 'Lucho')
        >>> marks_group.insert('TextGrid', 'Javier')
        >>> marks_group.insert('TextGrid', 'Rolando')
        """
        path = self._norm_path(path)
        parent_names = path.split('/')

        mark_group = self._find_mark_group(self.data, parent_names)
        if mark_group is None:
            raise MarkGroupNotFoundError(f'Cannot found {path} path.')

        dict_ = {
            'id': self.group_id,
            'name': new_name,
            'color': str(color),
            'hotkey': str(hotkey),
            'userparam': str(userparam),
        }
        self.group_id += 1
        mark_group.setdefault('child', [])
        mark_group['child'].append(dict_)

    def update(self, path, name= None, color= None, hotkey= None, userparam= None):
        """
        Update the attributes of a MARK_GROUP.

        path : str
            The path of the MARK_GROUP.
        name : str, defaul `None`
            The name of the new mark group
        color : int, default `None`
            A number representing the color. Unknown yet.
        hotkey : int, default `None`
            A shortcut for inserting marks. Use ASCII table references
            to associate a number with a key. 0 means no association.
        userparam : int, default `None` 
            Unkown yet.
        """
        path = self._norm_path(path)
        path_list = path.split('/')

        mark_group = self._find_mark_group(self.data, path_list)
        if mark_group is None:
            raise MarkGroupNotFoundError(f'Cannot found {path} path.')

        if not name is None:
            mark_group['name'] = name

        if not color is None:
            mark_group['color'] = color

        if not hotkey is None:
            mark_group['hotkey'] = hotkey

        if not userparam is None:
            mark_group['userparam'] = userparam

    def remove(self, path):
        """
        Remove a MARK_GROUP.

        Parameters
        ----------
        path : str
            The path of the MARK_GROUP.
        """
        if not self.is_path(path):
            raise MarkGroupNotFoundError(f'Cannot found {path} path.')

        path_list = self._norm_path(path).split('/')
        mark_group_name = path_list[-1]
        mark_group_path = path_list[:-1]
        parent_mark_group = self._find_mark_group(self.data, mark_group_path)

        sub_marks_group = parent_mark_group['child']
        for index_, dict_ in enumerate(sub_marks_group):
            if dict_['name'] == mark_group_name:
                index = index_
                break
        sub_marks_group.pop(index)

        if len(sub_marks_group) == 0:
            parent_mark_group.pop('child')

class MarkGroupNotFoundError(Exception):
    """
    Class for exception.
    """
