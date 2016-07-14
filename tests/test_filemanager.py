import os
import shutil

import unittest

import tempfile

from waxe.filemanager.files import (
    _append_file,
    get_folders_and_files,
)


def create_files():
    abs_dir = tempfile.mkdtemp()
    open(os.path.join(abs_dir, 'file1.txt'), 'w').write('file1')
    open(os.path.join(abs_dir, 'file2.txt'), 'w').write('file2')
    folder1 = os.path.join(abs_dir, 'folder1')
    os.mkdir(folder1)
    open(os.path.join(folder1, 'folder1_file1.txt'), 'w').write(
        'folder1_file1')
    return abs_dir


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.abs_dir = create_files()

    def tearDown(self):
        shutil.rmtree(self.abs_dir)

    def test__append_file(self):
        directory = 'dir'
        filename = 'file.txt'
        lis = []
        exts = None
        _append_file(filename, directory, lis, exts)
        self.assertEqual(lis, ['dir/file.txt'])

        lis = []
        exts = ['.xml']
        _append_file(filename, directory, lis, exts)
        self.assertEqual(lis, [])

        exts = ['.txt']
        _append_file(filename, directory, lis, exts)
        self.assertEqual(lis, ['dir/file.txt'])

        lis = []
        filename = '.file.txt'
        _append_file(filename, directory, lis, exts)
        self.assertEqual(lis, [])

    def test_get_folders_and_files(self):
        try:
            get_folders_and_files('/unexisting')
            assert(False)
        except IOError, e:
            self.assertEqual(str(e), "Directory /unexisting doesn't exist")
        folders, files = get_folders_and_files(self.abs_dir)
        self.assertEqual(len(folders), 1)
        self.assertEqual(len(files), 2)
