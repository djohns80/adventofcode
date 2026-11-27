import os


def decompressed_length(text, recursive=False):
    # count the length without building the decompressed string
    length = 0
    position = 0
    while position < len(text):
        if text[position] == "(":
            marker_end = text.index(")", position)
            marker = text[position + 1 : marker_end]
            count, repeats = marker.split("x")
            count = int(count)
            repeats = int(repeats)
            data_start = marker_end + 1
            if recursive:
                # markers inside the data section are expanded too
                data = text[data_start : data_start + count]
                length += decompressed_length(data, recursive=True) * repeats
            else:
                # the data section is not scanned for markers
                length += count * repeats
            position = data_start + count
        else:
            length += 1
            position += 1
    return length


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    # whitespace is ignored
    compressed = "".join(content.split())

    ##########
    # part 1 #
    ##########
    part_1 = decompressed_length(compressed)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = decompressed_length(compressed, recursive=True)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
