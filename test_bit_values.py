import pytest
from bit_values import Value15Bit, Value16Bit
from random import randint


@pytest.mark.parametrize('value', [
    -1,
    32776
])
def test_15_bit_values_out_of_range(value):
    with pytest.raises(ValueError):
        Value15Bit(value)


def test_15_bit_values_out_of_range_from_bytes():
    value_in_bytes = (32776).to_bytes(length=4, byteorder='little')
    with pytest.raises(ValueError):
        Value15Bit(value_in_bytes)


def test_15_bit_happy_path():
    value = randint(0, 32767)
    value_15_bit = Value15Bit(value)
    assert value == value_15_bit.value

    value = randint(0, 32767)
    value_in_bytes = value.to_bytes(length=4, byteorder='little')
    value_15_bit = Value15Bit(value_in_bytes)
    assert value == value_15_bit.value


@pytest.mark.parametrize('value', [
    -1,
    65536
])
def test_16_bit_values_out_of_range(value):
    with pytest.raises(ValueError):
        Value16Bit(value)


def test_16_bit_happy_path():
    value = randint(0, 65535)
    value_16_bit = Value16Bit(value)
    assert value == value_16_bit.value

    value = randint(0, 65535)
    value_in_bytes = value.to_bytes(length=4, byteorder='little')
    value_16_bit = Value16Bit(value_in_bytes)
    assert value == value_16_bit.value

