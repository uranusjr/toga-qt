from __future__ import print_function, absolute_import, division

from ..libs import qt
from .base import Widget


class SplitContainer(Widget):

    HORIZONTAL = False
    VERTICAL = True

    def __init__(self, direction=VERTICAL):
        super(SplitContainer, self).__init__()
        self.direction = direction
        self._content = None

        self.startup()

    def startup(self):
        self._impl = qt.QSplitter()
        self._impl.setOrientation(self._get_orientation())

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if len(content) != 2:
            raise ValueError('SplitContainer content must be a 2-tuple')
        self._content = content

        for widget in self._content:
            widget.window = self.window
            widget.app = self.app
            self._impl.addWidget(widget._impl)

    def _set_app(self, app):
        for widget in self._content:
            widget.app = self.app

    def _set_window(self, window):
        for widget in self._content:
            widget.window = self.window

    def _get_orientation(self):
        if self.direction == self.HORIZONTAL:
            return qt.Qt.Vertical
        return qt.Qt.Horizontal
