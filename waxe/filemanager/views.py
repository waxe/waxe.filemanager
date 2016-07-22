import os
from pyramid.view import view_config, view_defaults
import pyramid.httpexceptions as exc

from .files import (
    get_folders_and_files,
    relative_path,
    absolute_path,
)


@view_defaults(renderer='json')
class FilesView(object):

    def __init__(self, request):
        self.request = request
        # TODO: put root_path in config
        self.root_path = '/home/lereskp/temp/waxe/client1'
        path = self.request.GET.get('path', '')
        self.abspath = absolute_path(self.root_path, path)

    def path_to_relpath(self, path):
        """Transform the given path in relative path
        """
        return relative_path(self.root_path, path)

    def remove_abspath(self, s):
        """In the error message we don't want to display the absolute path
        """
        s = s.replace(self.root_path + '/', '')
        s = s.replace(self.root_path, '')
        return s

    @view_config(route_name='files')
    def files_view(self):
        """Get the folders and the files for the given path
        """
        try:
            folders, filenames = get_folders_and_files(self.abspath)
        except IOError, e:
            raise exc.HTTPNotFound(self.remove_abspath(str(e)))

        lis = []

        for folder in folders:
            lis += [{
                'name': os.path.basename(folder),
                'type': 'folder',
                'path': self.path_to_relpath(folder),
            }]
        for filename in filenames:
            lis += [{
                'name': os.path.basename(filename),
                'type': 'file',
                'path': self.path_to_relpath(filename),
            }]
        return lis


def includeme(config):
    config.add_route('files', '/api/0/files')
    config.scan(__name__)
