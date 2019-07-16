class CollapsedItem:
    pass

class CollapsedPrimitive(CollapsedItem):

    def __init__(self, value):

        if value is None:
            self.type = "none"
        elif isinstance(value, int):
            self.type = "int"
        elif isinstance(value, float):
            self.type = "float"
        elif isinstance(value, str):
            self.type = "str"
        else:
            assert False

        self.value_str = str(value)

    def __str__(self):
        return self.value_str

    def __eq__(self, other):

        if not isinstance(other, CollapsedPrimitive):
            return False

        return self.type == other.type

class CollapsedEmptyArray(CollapsedItem):

    def __init__(self, shape=[0]):
        self.shape = shape

    def add_dimension(self, new_dim_size):
        new_shape = [new_dim_size] + self.shape
        return CollapsedEmptyArray(new_shape)

    def __str__(self):
        if self.shape == [0]:
            return "[]"
        else:
            shape_str = ",".join(str(d) for d in self.shape)
            return "[empty (%s)]" % shape_str

    def __eq__(self, other):

        if not isinstance(other, CollapsedEmptyArray):
            return False

        return self.shape == other.shape

class CollapsedArray(CollapsedItem):

    def __init__(self, data_type, shape):

        self.data_type = data_type
        self.shape = shape

    def add_dimension(self, new_dim_size):
        new_shape = [new_dim_size] + self.shape
        return CollapsedArray(self.data_type, new_shape)

    def __str__(self):
        shape_str = ",".join(str(d) for d in self.shape)
        return "[%s (%s)]" % (self.data_type, shape_str)

    def __eq__(self, other):

        if not isinstance(other, CollapsedArray):
            return False

        return (self.data_type == other.data_type) and \
               (self.shape == other.shape)
