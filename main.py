from central_processing_unit import CentralProcessingUnit

cpu = CentralProcessingUnit(capture_terminal_log=True)

# TODO: do the same thing w/ reading from memory
# TODO: test that nothing is printed when there is no value there

# Write ascii value of 'a' to the 2nd register
# and value of 'b' to memory address 9
cpu.registers.write_to(2, 97)
cpu.memory.write_to(9, 98)

# This program says print out the value in the 2nd register
# then print out the value in the 9th memory address
program = [19, 32770, 19, 9]

cpu.run_program(program)