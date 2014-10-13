from __future__ import print_function, absolute_import, division

from ..libs import qt
from .base import Widget


def identifier(obj):
    return str(id(obj))


class Node(object):

    def __init__(self, data):
        self.data = data


class TreeModelImpl(qt.QAbstractItemModel):

    def __init__(self, headings, data):
        super(TreeModelImpl, self).__init__()
        self.headings = headings
        self._data = data

    def data(self, index, role):
        if role in (qt.Qt.DisplayRole, qt.Qt.EditRole,):
            current_id = index.internalPointer()
            if current_id is not None:
                return self._data[current_id]['node'].data[index.column()]
        return None

    def headerData(self, section, orientation, role):
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            return self.headings[section]
        return None

    def index(self, row, column, parent_index):
        if not self.hasIndex(row, column, parent_index):
            return qt.QModelIndex()
        if not parent_index.isValid():      # Current node is at root.
            parent_id = None
        else:
            parent_id = parent_index.internalPointer()
        try:
            current_id = self._data[parent_id]['children'][row]
        except IndexError:
            return qt.QModelIndex()
        return self.createIndex(row, column, current_id)

    def parent(self, index):
        current_id = index.internalPointer()
        if not index.isValid() or current_id is None:
            return qt.QModelIndex()
        data = self._data
        parent_id = data[index.internalPointer()]['parent']
        if parent_id is None:
            row = 0
        else:
            row = data[data[parent_id]['parent']]['children'].index(parent_id)
        return self.createIndex(row, 0, parent_id)

    def rowCount(self, index):
        if not index.isValid():
            parent_id = None
        else:
            parent_id = index.internalPointer()
        children = self._data[parent_id]['children']
        if children is None:
            return 0
        return len(children)

    def columnCount(self, index):
        return len(self.headings)


class Tree(Widget):

    def __init__(self, headings):
        super(Tree, self).__init__()
        self.headings = headings

        self._tree = None
        self._columns = None

        self._data = {
            None: {
                'children': None,
            },
        }

        self.startup()

    def startup(self):
        self._impl = qt.QTreeView()
        self._model_impl = TreeModelImpl(self.headings, self._data)
        self._impl.setModel(self._model_impl)

    def insert(self, parent, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        node = Node(data)

        parent_node = self._data[parent]
        if parent_node['children'] is None:
            parent_node['children'] = []

        current_id = identifier(node)
        if index is None:
            parent_node['children'].append(current_id)
            index = len(parent_node['children']) - 1
        else:
            parent_node['children'].insert(index, current_id)

        self._data[current_id] = {
            'node': node,
            'children': None,
            'parent': parent,
        }

        if parent is None:
            parent_index = qt.QModelIndex()
        else:
            parent_index = self._model_impl.parent(
                self._model_impl.createIndex(index, 0, current_id)
            )

        # Fake an insert event to trigger UI update.
        self._model_impl.beginInsertRows(parent_index, index, index + 1)
        self._model_impl.endInsertRows()

        return current_id
