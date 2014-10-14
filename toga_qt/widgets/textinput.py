from __future__ import print_function, absolute_import, division

from ..libs import qt
from .base import Widget


class TextInput(Widget):

    def __init__(self, initial=None, placeholder=None, readonly=False):
        super(TextInput, self).__init__()

        self.startup()

        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial

    def startup(self):
        self._impl = qt.QLineEdit()

    @property
    def readonly(self):
        return self._impl.isReadOnly()

    @readonly.setter
    def readonly(self, value):
        self._impl.setReadOnly(value)

    @property
    def placeholder(self):
        return self._impl.placeholderText()

    @placeholder.setter
    def placeholder(self, value):
        if value is None:
            value = ''
        self._impl.setPlaceholderText(value)

    @property
    def value(self):
        return self._impl.text()

    @value.setter
    def value(self, value):
        if value is None:
            value = ''
        self._impl.setText(value)
