class Node(object):

    def __init__(self, value, coordinates=None, parent=None, children=None):
        self._value = value
        if coordinates is None:
            self._coordinates = []
        self.coordinates = coordinates
        self._parent = parent
        if parent is not None:
            parent.add_children(self)
        if children is None:
            children = []
        self._children = children

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return self._children

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return len(self._children) == 0

    def add_child(self, node):
        self._children.append(node)

    def __str__(self):
        return str(self._coordinates)


class Tree(object):

    def __init__(self, root=None):
        self._root = root

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, node):
        self._root = node

    def is_empty(self):
        return self._root is None

    def depth(self, node):
        parent = node.parent
        if parent is None:
            return 0

        return 1 + self.depth(parent)
 