from __future__ import print_function, absolute_import, division

from ..libs import qt
from .base import Widget


class ButtonImpl(qt.QPushButton):

    def __init__(self, _interface, *args, **kwargs):
        super(ButtonImpl, self).__init__(*args, **kwargs)
        self._interface = _interface
        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        self._interface.on_press(self._interface)


class Button(Widget):

    def __init__(self, label, on_press=None):
        super(Button, self).__init__()
        self.label = label
        self.on_press = on_press

        self._expand_vertical = False

        self.startup()

    def startup(self):
        self._impl = ButtonImpl(self, self.label)
