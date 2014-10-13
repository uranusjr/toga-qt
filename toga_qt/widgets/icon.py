from __future__ import print_function, absolute_import, division

import os

import toga

from ..libs import qt


class Icon(object):

    app_icon = None

    def __init__(self, path, system=False):
        self.path = path
        self.system = system
        if self.system:
            filename = os.path.join(
                os.path.dirname(toga.__file__), 'resources', self.path,
            )
        else:
            filename = self.path
        self._impl = qt.QIcon(filename)

    @staticmethod
    def load(path_or_icon, default=None):
        while callable(default):
            default = default()
        while callable(path_or_icon):
            path_or_icon = path_or_icon()

        if path_or_icon:
            if isinstance(path_or_icon, Icon):
                obj = path_or_icon
            else:
                obj = Icon(path_or_icon)
        elif default:
            obj = default
        else:
            raise ValueError('Need to specify icon path or default icon')
        return obj


# Qt can't load pixmaps before the application is created, so we need to delay
# initialization.
TIBERIUS_ICON = lambda: Icon('tiberius-32.png', system=True)
