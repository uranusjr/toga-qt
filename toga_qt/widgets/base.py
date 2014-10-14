from __future__ import print_function, absolute_import, division

from toga_cassowary.widget import Widget as CassowaryWidget


class SizeHintMixin(object):

    @property
    def _width_hint(self):
        return (self._impl.minimumSizeHint().width(),
                self._impl.sizeHint().width())

    @property
    def _height_hint(self):
        return (self._impl.minimumSizeHint().height(),
                self._impl.sizeHint().height())


class Widget(SizeHintMixin, CassowaryWidget):
    pass
