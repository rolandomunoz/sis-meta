"""
Class for handling MARKS_GROUP in meta file.
"""
import re
import io
from importlib.resources import files

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
                self.data = discover_grouptree(raw_file, {})
        else:
            with open(path, 'rb') as raw_file:
                match = GROUPS_SEGMENT.match(raw_file.read())
                if not match:
                    raise IOError(f'{path} is not a meta file.')
                self.data = discover_grouptree(
                    io.BytesIO(match.group(1)),
                    {}
                )
        self.group_id = self._find_max_id(self.data)

    def _find_max_id(self, data):
        """
        Find the max group id.
        """
        for group_id, dict_ in data.items():
            max_value = group_id
            if 'child' in dict_:
                current_value = self._find_max_id(dict_['child'])
                max_value = current_value if current_value > max_value else max_value
        return max_value

    def _find_element(self, tree, path):
        """
        Find an element within a tree by name attribute.
        """
        name = path[:1]
        path_ = path[1:]

        # Base case
        if len(name) == 0: # Each element in the path has been consumed
            return tree

        # Recursive case
        # Given a path, find its nested dict
        name_str = name[0]
        for _, dict_ in tree.items():
            if not dict_['name'] == name_str:
                continue

            child = dict_.get('child')
            if child is None:
                if len(path_) == 0: # The elemt
                    return self._find_element(dict_, path_)
            else:
                return self._find_element(child, path_)

        raise MarkGroupNotFoundError(
            f'mark group "{name[0]}" does not exist.'
        )

    @staticmethod
    def _norm_path(path):
        """
        Normalize path.

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

    def insert(self, path, new_name, color=0, hotkey= 0, userparam=0):
        """
        Insert a mark group.

        Parameters
        ----------
        tree : dict of dict
            The MARKS_GROUP structure.
        path : str
            The mark groups that contain the target mark group. When
            a target mark group in nested inside more than one group,
            use forward slashes (`/`) between the subgroups' names.
        new_name : str
            The name of the new mark group
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

        tree = self._find_element(self.data, parent_names)
        self.group_id += 1
        tree[self.group_id] = {
                        'name': new_name,
                        'color': str(color),
                        'hotkey': str(hotkey),
                        'userparam': str(userparam),
                    }

    def update(self, path, name= None, color= None, hotkey= None, userparam= None):
        """
        Update a mark group.

        path : str
            The mark groups that contain the target mark group. When
            a target mark group in nested inside more than one group,
            use forward slashes (`/`) between the subgroups' names.
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

        tree = self._find_element(self.data, path_list)

        if not name is None:
            tree['name'] = name

        if not color is None:
            tree['color'] = color

        if not hotkey is None:
            tree['hotkey'] = hotkey

        if not userparam is None:
            tree['userparam'] = userparam

    def remove(self, path):
        """
        Remove a mark group item.

        Parameters
        ----------
        path : str
            The mark groups that contain the target mark group. When
            a target mark group in nested inside more than one group,
            use forward slashes (`/`) between the subgroups' names.
        """
        path = self._norm_path(path)
        path_list = path.split('/')

        name = path_list[-1]
        parents = path_list[:-1]

        tree = self._find_element(self.data, parents)
        group_id = None
        for group_id_, dict_ in tree.items():
            if dict_['name'] == name:
                group_id = group_id_
                break

        if group_id is None:
            raise MarkGroupNotFoundError(
                f'mark group "{name}" does not exist'
            )
        tree.pop(group_id)

class MarkGroupNotFoundError(Exception):
    """
    Class for exception.
    """
