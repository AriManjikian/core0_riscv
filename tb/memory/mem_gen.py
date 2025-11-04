import random


def generate_random_mem_file(filename="mem.hex", words=64):
    mem_list = [random.getrandbits(32) for _ in range(words)]
    with open(filename, "w") as f:
        for word in mem_list:
            f.write(f"{word:08X}\n")
    return mem_list
