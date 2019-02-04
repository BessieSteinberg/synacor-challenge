from memory_storage import Memory

memory = Memory()

bytes_generator = memory.get_bytes_from_file('challenge.bin')

for b in bytes_generator:
    print(b)