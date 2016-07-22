import os


def relative_path(root_path, path):
    """Make a relative path

    :param path: the path we want to transform as relative
    :type path: str
    :param root_path: the root path
    :type root_path: str

    ;return: the relative path from given path according to root_path
    :rtype: str
    ..note:: The path should be in root_path. If it's not the case it raises
    and IOError exception.
    """
    path = os.path.normpath(path)
    root_path = os.path.normpath(root_path)
    relpath = os.path.relpath(path, root_path)
    abspath = os.path.normpath(os.path.join(root_path, relpath))
    if not abspath.startswith(root_path):
        # Forbidden path
        raise IOError("%s doesn't exist" % path)
    return relpath


def absolute_path(root_path, relpath):
    """Make an absolute relpath

    :param relpath: the relative path we want to transform as absolute
    :type relpath: str
    :param root_path: the root path
    :type root_path: str

    ;return: the absolute path from given relpath according to root_path
    :rtype: str
    """
    relpath = os.path.normpath(relpath)
    root_path = os.path.normpath(root_path)
    abspath = os.path.normpath(os.path.join(root_path, relpath))
    if not abspath.startswith(root_path):
        # Forbidden path
        raise IOError("%s doesn't exist" % relpath)
    return abspath


def _append_file(filename, directory, lis, exts=None):
    if filename.startswith('.'):
        return
    if exts:
        _, ext = os.path.splitext(filename)
        if ext not in exts:
            return
    lis.append(os.path.join(directory, filename))


def get_folders_and_files(abspath, exts=None):
    """Get all the folders and files in the given abspath

    ..note:: this is not recursive
    """
    if not os.path.isdir(abspath):
        raise IOError("Directory %s doesn't exist" % abspath)

    folders = []
    files = []

    for dirpath, dirnames, filenames in os.walk(abspath):
        dirnames.sort()
        filenames.sort()

        for d in dirnames:
            _append_file(d, dirpath, folders)

        for f in filenames:
            _append_file(f, dirpath, files, exts)

        return folders, files
