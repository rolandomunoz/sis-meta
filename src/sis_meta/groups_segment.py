"""
Class for handling GROUPS_SEGMENT in meta file.
"""
import re
import io
from importlib.resources import files

from sis_meta.io._parse_groups_segment import discover_grouptree
from sis_meta.io._serialize_groups_segment import serialize_groups_segment

GROUPS_SEGMENT= re.compile(
rb'''MARKS_GROUPS_DATA; BEGIN; COMPOSITE;BINARY;\d+
VERSION; 2

GROUPS_SEGMENT; BEGIN; COMPOSITE;BINARY;\d+
(.+)
GROUPS_SEGMENT; END
''', re.DOTALL
)

class GroupsSegment:
    """
    A class for handling GROUPS_SEGMENT
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

    def __repr__(self):
        return serialize_groups_segment(self.data)

    def _find_max_id(self, data):
        """
        Find the higher ID in GROUPS_SEGMENT.
        """
        for dict_ in data:
            max_value = dict_['id']
            if 'child' in dict_:
                current_value = self._find_max_id(dict_['child'])
                max_value = current_value if current_value > max_value else max_value
        return max_value

    def _find_group(self, data, path):
        """
        Find a GROUP dict.
        """
        group_name = path[0]
        group_name_path = path[1:]

        # Base case
        if len(group_name_path) == 0: # Each element in the path has been consumed
            for dict_ in data:
                if dict_['name'] == group_name:
                    return dict_
            return None

        # Recursive case
        for dict_ in data:
            if not dict_['name'] == group_name:
                continue

            if 'child' in dict_:
                return self._find_group(dict_['child'], group_name_path)

    @staticmethod
    def _norm_path(path):
        """
        Normalize a GROUP path.

        Parameters
        ----------
        path : str
            The path of a GROUP.

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
        Check if the GROUP path exists.

        Parameter
        ---------
        path : str
            The path of a GROUP.

        Returns
        -------
        bool
            Return `True` if the GROUP path exists; otherwise, `False`.
        """
        path_list = self._norm_path(path).split('/')
        path_exists = self._find_group(self.data, path_list)

        if path_exists is None:
            return False
        return True

    def insert(self, name, path = '', color = 0, hotkey = 0, userparam = 0):
        """
        Insert a GROUP.

        Parameters
        ----------
        name : str
            The name of the GROUP to be inserted.
        path : str, default ''
            The path of the GROUP.
        color : int, default 0
            A number representing the color. Unknown yet.
        hotkey : int, default 0
            A shortcut for inserting marks. Use ASCII table references
            to associate a number with a key. 0 means no association.
        userparam : int, default 0
            Unkown yet.

        Examples
        --------
        Insert `TextGrid` as a `GROUP`.

        >>> groups_segment = sis_meta.GroupsSegment()
        >>> groups_segment.insert('TextGrid', '')
        
        Then, insert `Rolando`, `Luis`, `Juan` and `José Roberto` as
        `SUBGROUPS` of `TextGrid`.

        >>> groups_segment.insert('Rolando', 'TextGrid')
        >>> groups_segment.insert('Luis', 'TextGrid', 255, 49, 15)
        >>> groups_segment.insert('Juan', 'TextGrid', userparam = 0)
        >>> groups_segment.insert('José Roberto', 'TextGrid', hotkey = 49)
        """
        path = self._norm_path(path)
        path_list = path.split('/')
        group = self._find_group(self.data, path_list)

        if group is None:
            raise GroupNotFoundError(f'Cannot found the GROUP "{path}".')

        dict_ = {
            'id': self.group_id,
            'name': name,
            'color': str(color),
            'hotkey': str(hotkey),
            'userparam': str(userparam),
        }
        self.group_id += 1
        group.setdefault('child', [])
        group['child'].append(dict_)

    def update(self, path, name= None, color= None, hotkey= None, userparam= None):
        """
        Update the attributes of a GROUP.

        path : str
            The path of the GROUP.
        name : str, default `None`
            The new name of the GROUP. If `None`, nothing happens.
        color : int, default `None`
            A number representing the color. Unknown yet.
        hotkey : int, default `None`. If `None`, nothing happens.
            A shortcut for inserting marks. Use ASCII table references
            to associate a number with a key. 0 means no association.
        userparam : int, default `None`
            Unkown yet. If `None`, nothing happens.
        """
        path = self._norm_path(path)
        path_list = path.split('/')

        group = self._find_group(self.data, path_list)
        if group is None:
            raise GroupNotFoundError(f'Cannot found {path} path.')

        if not name is None:
            group['name'] = name

        if not color is None:
            group['color'] = color

        if not hotkey is None:
            group['hotkey'] = hotkey

        if not userparam is None:
            group['userparam'] = userparam

    def remove(self, path):
        """
        Remove a GROUP.

        Parameters
        ----------
        path : str
            The path of the target GROUP.
        """
        if not self.is_path(path):
            raise GroupNotFoundError(f'Cannot found the GROUP {path}.')

        path_list = self._norm_path(path).split('/')
        group_name = path_list[-1]
        group_path = path_list[:-1]

        group = self._find_group(self.data, group_path)
        subgroups = group['child']

        for index_, dict_ in enumerate(subgroups):
            if dict_['name'] == group_name:
                index = index_
                break
        subgroups.pop(index)

        if len(subgroups) == 0:
            group.pop('child')

class GroupNotFoundError(Exception):
    """
    Class for exception.
    """
