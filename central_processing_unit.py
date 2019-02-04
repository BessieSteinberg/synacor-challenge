from memory_storage import Memory, Registers, Stack


class ProgramTerminated(Exception):
    pass


class NoCommandError(Exception):
    pass


class CentralProcessingUnit(object):
    """ Models the CPU """

    MAX_VALUE = 32768

    def __init__(self, capture_terminal_log=False):
        # Initialize all the memory
        self.memory = Memory()
        self.registers = Registers()
        self.stack = Stack()

        self.program_pointer = 0

        # Just for debugging
        self.capture_terminal_log = capture_terminal_log
        self.terminal_log = ''

    def get_value(self, a):
        """
        'a' represents a register address or a literal value
        attempt to use 'a' as a register address and if that fails return the
        literal value
        """
        try:
            return self.registers.read_from(a).value
        except (AttributeError, IndexError):
            return a

    def halt(self):
        """ stop execution and terminate the program """
        raise ProgramTerminated()

    def out(self):
        """
        out: 19 a
        write the character represented by ascii code <a> to the terminal
        if there is no value at that address, do nothing
        """
        a = next(self.current_program)
        value = self.get_value(a)
        ascii_char = str(chr(value))

        if self.capture_terminal_log:
            self.terminal_log += ascii_char

        print(ascii_char, end="")

    def noop(self):
        """ no operation """
        pass

    def add(self):
        """
        add: 9 a b c
        assign into <a> the sum of <b> and <c> (modulo MAX_VALUE)
        """
        reg_a = next(self.current_program)
        b = self.get_value(next(self.current_program))
        c = self.get_value(next(self.current_program))

        result = (b + c) % self.MAX_VALUE
        self.registers.write_to(address_or_register=reg_a, value=result)

    def jmp(self):
        """
        jmp: 6 a
        jump to <a>
        """
        a = self.get_value(next(self.current_program))
        self.program_pointer = a

    # maps the opcode # to the associated function
    opcodes = {
        0: halt,
        6: jmp,
        9: add,
        19: out,
        21: noop,
    }

    def execute_command(self, opcode):
        """
        excecute the command defined by 'opcode'
        if there is no command for that opcode raises a NoCommandError
        """
        try:
            self.opcodes[opcode](self)
        except KeyError:
            raise NoCommandError(f"No command for opcode [{opcode}]")

    def get_current_program_value(self):
        """ Returns the value currently pointed to in the program then increases the pointer """
        while True:
            value = self.memory.read_from(self.program_pointer)
            if value:
                self.program_pointer += 1
                yield value.value
            else:
                break

    def run_program(self, program, from_file=False):
        """ runs the program which is models as an iterable of numbers """

        self.program_pointer = 0
        self.memory.load_program(program, from_file)
        self.current_program = self.get_current_program_value()

        while True:
            try:
                opcode = next(self.current_program)
                self.execute_command(opcode)
            except StopIteration:
                break
