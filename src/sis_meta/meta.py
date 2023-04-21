"""
Handle annotation files (.meta).
"""
from sis_meta.groups_segment import GroupsSegment
from sis_meta.io._serialize_marks_groups_data import serialize_marks_groups_data

class Meta:
    """
    Class for handling guide marks.
    """
    def __init__(self):
        self.data = []
        self._groups_segment = GroupsSegment()

    def __iter__(self):
        return iter(self.data)

    def _sort(self):
        self.data = sorted(self.data, key=lambda x: x.position)

    def manage_groups_segment(self):
        """
        Manage GROUPS_SEGMENT.
        """
        return self._groups_segment

    def insert_guide_mark(self, group_name, position, length = 0, text = ''):
        """
        Insert a guide mark.
        """
        mark_group_id = self._groups_segment.get_id(group_name)
        mark_group_name = group_name.split('/')[-1]
        guide_mark = GuideMark(
            position, length, text, mark_group_id, mark_group_name
        )
        self.data.append(guide_mark)
        self._sort()

    def write(self, path):
        """
        Write a meta file.
        """
        content = serialize_marks_groups_data(self)
        with open(path, 'wb') as meta_file:
            meta_file.write(content)

class GuideMark:
    """
    A guide mark.
    """
    def __init__(self, position, length, text, group_id, group_name):
        self.position = position
        self.length = length
        self.text = text
        self.group_id = group_id
        self.group_name = group_name

    def __repr__(self):
        dict_ = {
            'position': round(self.position, 2),
            'length': round(self.length, 2),
            'text': self.text,
            'group_id': self.group_id,
            'group_name': self.group_name,
        }
        return dict_.__repr__()

    def is_interval(self):
        """
        Check if the guide mark is an interval.

        Returns
        -------
        bool : True or False
            `True` if the length is greater than 0. Otherwise, it returns `False`.
        """
        return self.length != 0

    def is_point(self):
        """
        Check if the guide mark is a point.

        Returns
        -------
        bool : True or False
            `True` if the length is greater than 0. Otherwise, it returns `False`.
        """
        return self.length == 0
