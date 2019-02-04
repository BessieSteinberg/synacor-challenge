class ValueXBit(object):
    """ Generic class used to define a value stored in X bits """

    def __init__(self, num_bits, value, from_bytes=False):
        self.min = 0
        self.max = 2 ** num_bits - 1

        if from_bytes:
            self.value = int.from_bytes(value, 'little')
        else:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value < self.min:
            raise ValueError(f"Value cannot be below {self.min}")

        if value > self.max:
            raise ValueError(f"Value cannot be above {self.max}")

        self._value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value


class Value15Bit(ValueXBit):
    """ Class used to define values stored in 15 bits """

    def __init__(self, value, from_bytes=False):
        super(Value15Bit, self).__init__(15, value, from_bytes)


class Value16Bit(ValueXBit):
    """ Class used to define values stored in 16 bits """

    def __init__(self, value, from_bytes=False):
        super(Value16Bit, self).__init__(16, value, from_bytes)


