import pytest
from memory_storage import Memory, Registers, Stack
from random import randint


def test_memory_read_from():
    """ test the read_from method """
    memory = Memory()

    # A value written to memory should be returned
    address = randint(0, 32767)
    value = randint(0, 65535)
    memory.write_to(address, value)
    assert value == memory.read_from(address).value

    # Attempting to access memory out of range should return an Index Error
    with pytest.raises(IndexError):
        memory.read_from(32768)

    with pytest.raises(IndexError):
        memory.read_from(-1)

    # If there is no data at the requested address read_from should return None
    empty_address = address + 1 % 32767
    assert memory.read_from(empty_address) is None


def test_memory_write_to_happy_path():
    """ test the write_to method """
    memory = Memory()

    # A value written to memory should be returned
    address = randint(0, 32767)
    value = randint(0, 65535)
    memory.write_to(address, value)
    assert value == memory.read_from(address).value


def test_memory_write_to_out_of_range():
    """ test that if the address and/or the value is out of range appropriate errors are thrown """
    memory = Memory()

    # An address < 0 should throw an IndexError
    with pytest.raises(IndexError):
        memory.write_to(-2, 5)

    # An address > 32767 should throw an IndexError
    with pytest.raises(IndexError):
        memory.write_to(60000, 5)

    address = randint(0, 32767)

    # A value < 0 should throw an Index Error
    with pytest.raises(IndexError):
        memory.write_to(address, -5)

    # A value > 65535 should throw an Index Error
    with pytest.raises(IndexError):
        memory.write_to(address, 655358)


def test_registers_read_from():
    """ test the registers read_from method """
    registers = Registers()

    # write to address 32769 / register 1, make sure you read the same value
    # when fetching it as address 32769 or register_num 1
    address = 32769
    reg_num = 1
    value = randint(0, 65535)
    registers.write_to(address, value)
    assert value == registers.read_from(address).value
    assert value == registers.read_from(reg_num).value

    # write to address 32775 / register 7, make sure you read the same value
    # when fetching it as address 32775 or register_num 7
    address = 32775
    reg_num = 7
    value = randint(0, 65535)
    registers.write_to(reg_num, value)
    assert value == registers.read_from(address).value
    assert value == registers.read_from(reg_num).value

    # when reading from a location that has no data it should return None
    address = 32768
    reg_num = 5
    assert registers.read_from(address) is None
    assert registers.read_from(reg_num) is None


def test_registers_out_of_range():
    """
    Test that an IndexError is thrown when we attempt to query an invalid register
    Valid Ranges:
        0-7: the register numbers
        32768-32775: the register addresses
    """
    registers = Registers()

    with pytest.raises(IndexError):
        registers.read_from(-8)

    with pytest.raises(IndexError):
        registers.read_from(8)

    with pytest.raises(IndexError):
        registers.read_from(60000)


def test_registers_write_to():
    """
    Test the write to method for Registers
    """
    registers = Registers()

    # Assert that you can write to a reg and get the same value out
    value = randint(0, 65535)
    reg_num = randint(0,7)
    registers.write_to(reg_num, value)

    value = randint(0, 65535)
    address = randint(32768, 32775)
    registers.write_to(address, value)

    # Assert you cannot write to an address/register < 0
    with pytest.raises(IndexError):
        registers.write_to(-1, value)

    # Assert you cannot write to an address/register between 8-32767
    with pytest.raises(IndexError):
        registers.write_to(9, value)

    # Assert you cannot write to an address/register > 32775
    with pytest.raises(IndexError):
        registers.write_to(90000, value)


def test_stack():
    """ Tests the stack memory model """
    stack = Stack()

    # Assert that an empty stack returns None
    assert stack.pop() is None

    # Assert that values pushed onto a stack are popped in reverse order
    values = [randint(0, 65535) in range(5)]
    for value in values:
        stack.push(value)

    for value in values[::-1]:
        assert value == stack.pop().value

    # Assert stack is empty now
    assert stack.pop() is None

    # Assert pushing onto stack with out of range values fails with ValueError
    with pytest.raises(ValueError):
        stack.push(-9)

    with pytest.raises(ValueError):
        stack.push(70000)
