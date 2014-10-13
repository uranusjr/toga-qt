from __future__ import print_function, absolute_import, division

from ..libs import qt
from .base import Widget


class ScrollContainer(Widget):

    def __init__(self, horizontal=True, vertical=True):
        super(ScrollContainer, self).__init__()
        self.horizontal = horizontal
        self.vertical = vertical
        self._content = None

        self.startup()

    def startup(self):
        self._impl = qt.QScrollArea()
        self._impl.setHorizontalScrollBarPolicy(self._policy(self.horizontal))
        self._impl.setVerticalScrollBarPolicy(self._policy(self.vertical))

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self.window
        self._content.app = self.app
        self._impl.setWidget(widget._impl)

    def _set_app(self, app):
        if self._content:
            self._content.app = self.app

    def _set_window(self, window):
        if self._content:
            self._content.window = self.window

    def _policy(self, value):
        if value:
            return qt.Qt.ScrollBarAsNeeded
        return qt.Qt.ScrollBarAlwaysOff
