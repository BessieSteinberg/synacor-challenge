from random import randint, choice


def get_random_memory_address(start_buffer=0, end_buffer=0):
    """ return random valid memory address 0...32767 """
    return randint(0 + start_buffer, 32767 + end_buffer)


def get_random_char_ASCII_value():
    """ return ASCII value of random char between a-z and A-Z """
    return choice([randint(97, 122), randint(65, 90)])


class TestPrograms(object):
    """ Set of small programs for testing """

    @staticmethod
    def print_rand_char():
        c = randint(97, 122)
        return [19, c]
