from __future__ import print_function, absolute_import, division

from ..libs import qt, utils
from .base import Widget


class TableModelImpl(qt.QAbstractTableModel):

    def __init__(self, headings, data):
        super(TableModelImpl, self).__init__()
        self.headings = headings
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self.headings)

    def data(self, index, role):
        if role in (qt.Qt.DisplayRole, qt.Qt.EditRole,):
            return utils.text(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role):
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            return self.headings[section]
        return None


class Table(Widget):

    def __init__(self, headings):
        super(Table, self).__init__()
        self.headings = headings

        self._data = []

        self.startup()

    def startup(self):
        self._impl = qt.QTableView()
        self._impl.setModel(TableModelImpl(self.headings, self._data))

    def insert(self, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        model = self._impl.model()
        if index is None:
            index = len(self._data)
            self._data.append(data)
        else:
            self._data.insert(index, data)

        # Fake an insert event to trigger UI update.
        model.beginInsertRows(qt.QModelIndex(), index, index + 1)
        model.endInsertRows()
