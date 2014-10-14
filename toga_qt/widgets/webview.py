from __future__ import print_function, absolute_import, division

from ..libs import qt
from .base import Widget


class WebView(Widget):

    def __init__(self, url=None):
        super(WebView, self).__init__()

        self.startup()

        self.url = url

    def startup(self):
        self._impl = qt.QWebView()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._impl.setUrl(qt.QUrl(value))
