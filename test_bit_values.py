import pytest
from bit_values import Value15Bit, Value16Bit


@pytest.mark.parametrize('value', [
    -1,
    32776
])
def test_15_bit_values_out_of_range(value):
    with pytest.raises(ValueError):
        Value15Bit(value)


def test_15_bit_happy_path():
    value = 207
    value_15_bit = Value15Bit(207)
    assert value == value_15_bit.value


@pytest.mark.parametrize('value', [
    -1,
    65536
])
def test_16_bit_values_out_of_range(value):
    with pytest.raises(ValueError):
        Value16Bit(value)


def test_16_bit_happy_path():
    value = 32776
    value_16_bit = Value16Bit(32776)
    assert value == value_16_bit.value
