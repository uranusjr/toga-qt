from __future__ import print_function, absolute_import, division

from toga import constants
from ..libs import qt
from ..libs.constants import get_alignment
from .base import Widget


class Label(Widget):

    def __init__(self, text=None, alignment=constants.LEFT_ALIGNED):
        super(Label, self).__init__()
        self.text = text

        self.startup()

        self.alignment = alignment

    def startup(self):
        self._impl = qt.QLabel(self.text)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._impl.setAlignment(get_alignment(value))
