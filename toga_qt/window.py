from __future__ import print_function, absolute_import, division

from .libs import qt
from .command import SEPARATOR, SPACER, EXPANDING_SPACER


class ToolbarImpl(qt.QToolBar):

    def __init__(self, _interface, *args, **kwargs):
        super(ToolbarImpl, self).__init__(*args, **kwargs)
        self._interface = _interface
        self.actionTriggered.connect(self._on_action_triggered)

    def _on_action_triggered(self, item_impl):
        toolbar_item = self._interface._action_lookup[item_impl]
        toolbar_item.action(toolbar_item)


class Window(object):
    """GUI Window object.

    Toga windows can always have a toolbar and/or menu, so this corresponds to
    QMainWindow, possibly containing a QWidget if it has content.
    """

    def __init__(self, title=None, position=(100, 100), size=(640, 480),
                 toolbar=None):
        self._app = None
        self._container = None
        self._size = size
        self._toolbar_impl = None
        self._action_lookup = {}

        self.title = title
        self.position = position

        self.startup()

        self.toolbar = toolbar

    def startup(self):
        self._impl = qt.QMainWindow()
        self._impl.resize(*self._size)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")
        self._app = app
        self._impl.setMenuBar(app.menu_bar)

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, value):
        self._toolbar = value
        self._action_lookup = {}
        if self._toolbar:
            impl = ToolbarImpl(self)
            impl.setToolButtonStyle(qt.Qt.ToolButtonTextUnderIcon)

            for toolbar_item in self._toolbar:
                if toolbar_item == SEPARATOR:
                    item_impl = impl.addSeparator()
                elif toolbar_item == SPACER:
                    item_impl = impl.addAction(qt.QWidget())
                elif toolbar_item == EXPANDING_SPACER:
                    item_impl = qt.QWidget()
                    item_impl.setHorizontalSizePolicy(
                        qt.QSizePolicy.Expending, qt.QSizePolicy.Preferred
                    )
                    impl.addAction(item_impl)
                else:
                    item_impl = impl.addAction(
                        toolbar_item.icon._impl, toolbar_item.label
                    )
                    item_impl.setToolTip(toolbar_item.tooltip)
                self._action_lookup[item_impl] = toolbar_item

            self._impl.addToolBar(impl)
            self._toolbar_impl = impl

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self
        self._content.app = self.app

        self._impl.setCentralWidget(widget._impl)

    def show(self):
        self._impl.show()
