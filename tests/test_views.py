import unittest

from pyramid import testing

from .utils import BaseFolderTest

from waxe.filemanager import views
from waxe.filemanager.files import absolute_path


class TestFilesViewFunctions(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        self.view = views.FilesView(request)
        self.view.root_path = '/tmp/folder1'

    def test_path_to_relpath(self):
        res = self.view.path_to_relpath('/tmp/folder1/file.txt')
        self.assertEqual(res, 'file.txt')

    def test_remove_abspath(self):
        s = "Can't open file /tmp/folder1/file.txt"
        res = self.view.remove_abspath(s)
        self.assertEqual(res, "Can't open file file.txt")


class TestFilesView(BaseFolderTest):

    def setUp(self):
        super(TestFilesView, self).setUp()
        request = testing.DummyRequest()
        self.view = views.FilesView(request)
        self.view.root_path = self.abs_dir
        self.view.abspath = absolute_path(self.view.root_path, relpath='')

    def test_files_view(self):
        res = self.view.files_view()
        expected = [
            {'path': 'folder1', 'type': 'folder', 'name': 'folder1'},
            {'path': 'file1.txt', 'type': 'file', 'name': 'file1.txt'},
            {'path': 'file2.txt', 'type': 'file', 'name': 'file2.txt'}
        ]
        self.assertEqual(res, expected)
