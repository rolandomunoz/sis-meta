"""
Serialize GROUPS_SEGMENT. 
"""
import re
import jinja2

def _iter(data):
    pass

def serialize_groups_segment(data):
    """
    Serialize GROUPS_SEGMENT.

    Parameters
    ----------
    data : :class:`sis_meta.GroupsSegment`

    """
    for dict_ in data:
        child = dict_.get('child')
        
        # Base case
        if child is None:
            print(dict_)

        else:
        # Recursive case
            print(f'OPEN_GROUP{dict_.get("id")}')
            print(dict_)
            print(f'OPEN_SUBGROUP{dict_.get("id")}')
            serialize_groups_segment(child)
            print(f'CLOSE_GROUP{dict_.get("id")}')
