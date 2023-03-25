"""
Handle annotation files (.meta).
"""
class Meta:
    """
    Class for handling guide marks.
    """
    def __init__(self):
        self.data = []

    def __iter__(self):
        return iter(self.data)

    def insert_guide_mark(self, position, length = 0, text = '', group_id = 6):
        """
        Insert a guide mark.
        """
        guide_mark = GuideMark(position, length, text, group_id, 'gaaa')
        self.data.append(guide_mark)

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
