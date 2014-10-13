from __future__ import print_function, absolute_import, division

from ..libs import qt
from .base import Widget


class OptionContainer(Widget):

    def __init__(self):
        super(OptionContainer, self).__init__()
        self._content = []

        self.startup()

    def startup(self):
        self._impl = qt.QTabWidget()

    def add(self, label, container):
        self._content.append((label, container,))
        container.window = self.window
        container.app = self.app

        self._impl.addTab(container._impl, label)
