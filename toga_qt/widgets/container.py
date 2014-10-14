from __future__ import print_function, absolute_import, division

from toga_cassowary.widget import Container as CassowaryContainer

from ..libs import qt
from .base import SizeHintMixin


class QContainer(qt.QWidget):
    """QWidget subclass for cassowary container _impl compatibility.
    """
    def __init__(self, layout_manager):
        super(QContainer, self).__init__()
        self.layout_manager = layout_manager
        self.setSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Fixed)

    def sizeHint(self):
        w = self.layout_manager.bounding_box.width.value
        h = self.layout_manager.bounding_box.height.value
        return qt.QSize(w, h)

    def minimumSizeHint(self):
        w = self.layout_manager.bounding_box.width.value
        h = self.layout_manager.bounding_box.height.value
        return qt.QSize(w, h)

    def resizeEvent(self, e):
        self._layout(self.width(), self.height())

    def showEvent(self, e):
        # Need to layout once when the widget appears.
        self._layout(self.width(), self.height())

    def add(self, widget):
        widget.setParent(self)

    def _layout(self, w, h):
        with self.layout_manager.layout(w, h):
            for widget in self.layout_manager.children:
                if widget._impl.isVisible():
                    min_width, preferred_width = widget._width_hint
                    min_height, preferred_height = widget._height_hint

                    box = widget._bounding_box
                    x_pos = box.x.value
                    if widget._expand_horizontal:
                        width = widget._bounding_box.width.value
                    else:
                        x_pos += (box.width.value - preferred_width) / 2.0
                        width = preferred_width

                    y_pos = box.y.value
                    if widget._expand_vertical:
                        height = box.height.value
                    else:
                        y_pos += ((box.height.value - preferred_height) / 2.0)
                        height = preferred_height

                    widget._impl.setGeometry(x_pos, y_pos, width, height)


class Container(SizeHintMixin, CassowaryContainer):
    """Container object.

    Corresponds to a QWidget. For consistency, we use Cassowary to layout the
    whole thing, instead of using Qt's box layout system.
    """
    def _create_container(self):
        return QContainer(self._layout_manager)
