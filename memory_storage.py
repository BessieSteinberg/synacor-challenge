from bit_values import Value16Bit, Value15Bit
from collections import deque


class RandomAccessMemory(object):
    """
    Models RAM allows you to write and read from addressed memory
    Assumes 16-bit values
    """

    def __init__(self):
        self._memory = {}

    def write_to(self, address, value):
        """ writes 'value' to memory 'address' if both are valid """
        try:
            value = Value16Bit(value)
        except ValueError:
            raise IndexError(f"Value [{value}] is out of range!")

        self._memory[address] = value

    def read_from(self, address):
        """
        Returns value stored in 'address'
        if  there is no value for 'address' return None
        """
        try:
            return self._memory[address]
        except KeyError:
            return None


class Memory(RandomAccessMemory):
    """ A type of RAM with a 15-bit memory space """

    def write_to(self, address, value):
        """ checks if address is in possible range and then tries to write 'value' to memory 'address'"""
        try:
            address = Value15Bit(address)
        except ValueError:
            raise IndexError(f"Address [{address}] is out of range!")

        super(Memory, self).write_to(address, value)

    def read_from(self, address):
        """
        Returns value stored in 'address'
        if 'address' is out of acceptable range throws an error
        if 'address' is in acceptable range but there is no value for it, return None
        """
        try:
            address = Value15Bit(address)
        except ValueError:
            raise IndexError(f"Address [{address}] is out of range!")

        return super(Memory, self).read_from(address)


class Registers(RandomAccessMemory):
    """
    Models the eight registers
    There are 7 registers (0...7) addressed as (32768..32775)
    """
    MIN_ADDRESS = 32768
    MAX_ADDRESS = 32775

    def get_register_num(self, address_or_register):
        """
        get the register number from the address
        if address_or_register is between 0-7: it is a register return that value
        if address_or_register is between 32768-32775: it is an address, return the corresponding register
        if it is any other number throw a ValueError
        """
        if address_or_register >= 0 and address_or_register <= 7:
            return address_or_register

        # Address must be in the range 32768..32775 of valid register addresses
        if address_or_register < self.MIN_ADDRESS or address_or_register > self.MAX_ADDRESS:
            raise ValueError(f"Address or register number [{address_or_register}] is invalid!")

        # find the corresponding register num
        return address_or_register - self.MIN_ADDRESS

    def write_to(self, address_or_register, value):
        """
        Writes 'value' to the register that maps to that 'address_or_register'
        """
        try:
            register_num = self.get_register_num(address_or_register)
        except ValueError:
            raise IndexError(f"Address or register [{address_or_register}] is out of range")

        super(Registers, self).write_to(register_num, value)

    def read_from(self, address_or_register):
        """
        Returns value stored at 'address_or_register'
        If both address and register_num are defined will default to using 'address
        """
        try:
            register_num = self.get_register_num(address_or_register)
        except ValueError:
            raise IndexError(f"Address or register [{address_or_register}] is out of range")

        return super(Registers, self).read_from(register_num)


class Stack(object):
    """ Models 16 bit values stored in stack memory """

    def __init__(self):
        self._stack = deque()

    def push(self, value):
        """ Pushes 'value' onto the stack if it is in acceptable range """
        self._stack.append(Value16Bit(value))

    def pop(self):
        """ Removes and returns the top value of the stack, if stack is empty return None """
        try:
            return self._stack.pop()
        except IndexError:
            return None

