# -*- coding: utf-8 -*-

import os
import shutil

import unittest

import tempfile

from waxe.filemanager.files import (
    _append_file,
    get_folders_and_files,
    relative_path,
    absolute_path,
)


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.abs_dir = tempfile.mkdtemp()
        open(os.path.join(self.abs_dir, 'file1.txt'), 'w').write('file1')
        open(os.path.join(self.abs_dir, 'file2.txt'), 'w').write('file2')
        self.folder1 = os.path.join(self.abs_dir, 'folder1')
        os.mkdir(self.folder1)
        self.folder1_file1 = os.path.join(self.folder1, 'folder1_file1.txt')
        open(self.folder1_file1, 'w').write('folder1_file1')

    def tearDown(self):
        shutil.rmtree(self.abs_dir)

    def test_relative_path(self):
        try:
            relpath = relative_path(self.abs_dir, '.')
            assert 0
        except IOError, e:
            self.assertEqual(str(e), ". doesn't exist")

        try:
            relpath = relative_path(self.abs_dir, 'test')
            assert 0
        except IOError, e:
            self.assertEqual(str(e), "test doesn't exist")

        relpath = relative_path(self.abs_dir, self.abs_dir)
        self.assertEqual(relpath, '.')

        relpath = relative_path(self.abs_dir, self.folder1)
        self.assertEqual(relpath, 'folder1')

        relpath = relative_path(self.abs_dir, self.folder1_file1)
        self.assertEqual(relpath, 'folder1/folder1_file1.txt')

        try:
            relpath = relative_path(self.abs_dir,
                                    '/folder1/folder1_file1.txt')
            assert 0
        except IOError, e:
            pass

    def test_absolute_path(self):
        relpath = 'folder1'
        abspath = absolute_path(self.abs_dir, relpath)
        self.assertEqual(abspath, self.folder1)

        relpath = ''
        abspath = absolute_path(self.abs_dir, relpath)
        self.assertEqual(abspath, self.abs_dir)

        relpath = 'folder1/folder1_file1.txt'
        abspath = absolute_path(self.abs_dir, relpath)
        self.assertEqual(abspath, self.folder1_file1)

        relpath = '/folder1/folder1_file1.txt'
        try:
            absolute_path(self.abs_dir, relpath)
            assert 0
        except IOError, e:
            self.assertEqual(str(e), "%s doesn't exist" % relpath)

        relpath = '../folder1/folder1_file1.txt'
        try:
            absolute_path(self.abs_dir, relpath)
            assert 0
        except IOError, e:
            self.assertEqual(str(e), "%s doesn't exist" % relpath)

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

        lis = []
        filename = u'filé.txt'
        _append_file(filename, directory, lis, exts)
        self.assertEqual(lis, [u'dir/filé.txt'])

    def test_get_folders_and_files(self):
        try:
            get_folders_and_files('/unexisting')
            assert(False)
        except IOError, e:
            self.assertEqual(str(e), "Directory /unexisting doesn't exist")
        folders, files = get_folders_and_files(self.abs_dir)
        self.assertEqual(len(folders), 1)
        self.assertEqual(len(files), 2)
