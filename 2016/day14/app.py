import binascii
import hashlib
import os
from functools import cache

KEYS_NEEDED = 64
LOOKAHEAD = 1000
STRETCH_COUNT = 2016


@cache
def md5_hash(salt, index, stretch_count):
    # hash once, then re-hash the hex digest stretch_count more times.
    # The data stays as bytes between rounds so it isn't re-encoded each time.
    data = f"{salt}{index}".encode()
    for _ in range(stretch_count + 1):
        data = binascii.hexlify(hashlib.md5(data).digest())
    return data.decode()


def first_triple(text):
    # return the character of the first run of three, or None
    for i in range(len(text) - 2):
        if text[i] == text[i + 1] == text[i + 2]:
            return text[i]
    return None


def is_key(salt, index, stretch_count):
    character = first_triple(md5_hash(salt, index, stretch_count))
    if character is None:
        return False
    five_in_a_row = character * 5
    for next_index in range(index + 1, index + 1 + LOOKAHEAD):
        if five_in_a_row in md5_hash(salt, next_index, stretch_count):
            return True
    return False


def find_key_index(salt, keys_needed, stretch_count=0):
    keys_found = 0
    index = 0
    while True:
        if is_key(salt, index, stretch_count):
            keys_found += 1
            if keys_found == keys_needed:
                return index
        index += 1


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    salt = content.strip()

    ##########
    # part 1 #
    ##########
    part_1 = find_key_index(salt, KEYS_NEEDED)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = find_key_index(salt, KEYS_NEEDED, STRETCH_COUNT)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
