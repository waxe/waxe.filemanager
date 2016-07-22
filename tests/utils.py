# -*- coding: utf-8 -*-

import os
import shutil

import unittest

import tempfile


class BaseFolderTest(unittest.TestCase):
    """Create the following tree:

        -/tmp/dir
        |- file1.txt
        |- file2.txt
        |- folder1
         |- folder1_file1.txt
    """

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
