from __future__ import print_function, absolute_import, division

import sys

from .libs import qt
from .widgets.icon import Icon, TIBERIUS_ICON
from .window import Window


class App(object):
    """Main application object.

    Corresponds to a QApplication.
    """

    def __init__(self, name, app_id, icon=None, startup=None):
        self._impl = qt.QApplication(sys.argv)

        # Set the icon for the app
        Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)
        self.icon = Icon.app_icon

        self._startup_method = startup

    def _startup(self, data=None):
        self.main_window = Window()
        menu_bar = qt.QMenuBar()

        # App menu
        app_menu = menu_bar.addMenu('Application')
        app_menu.addAction('About')
        app_menu.addAction('Preferences')
        app_menu.addSeparator()

        action = app_menu.addAction('Quit')
        action.triggered.connect(self._quit)
        action.shortcut = qt.QKeySequence('Ctrl+S')

        self.app_menu = app_menu

        # Help
        submenu = menu_bar.addMenu('Help')
        submenu.addAction('Help')

        self.main_window._impl.setMenuBar(menu_bar)

        self.startup()

        self.main_window.show()

    def _quit(self):
        self._impl.quit()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def main_loop(self):
        # Stimulate the build of the app
        self._startup()
        self._impl.exec_()
