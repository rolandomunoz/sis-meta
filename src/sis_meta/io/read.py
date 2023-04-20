
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
