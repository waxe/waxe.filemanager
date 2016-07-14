import os


def _append_file(filename, directory, lis, exts=None):
    filename = filename.decode('utf-8')
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
