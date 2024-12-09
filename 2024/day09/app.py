import os
from collections import deque


def get_checksum(disk_map):
    pos = 0
    checksum = 0
    for file_id, count in disk_map:
        for n in range(count):
            if file_id is not None:
                checksum += file_id * (pos + n)
        pos += count
    return checksum


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read().strip()
    sizes = [int(c) for c in content]

    ##########
    # part 1 #
    ##########
    block_que = deque(
        (int(i / 2) if i % 2 == 0 else None, size) for i, size in enumerate(sizes)
    )
    disk_map = []
    while block_que:
        block_section = block_que.popleft()
        if block_section[0] is not None:
            disk_map.append(block_section)
        else:
            gap_size = block_section[1]
            while gap_size > 0:
                end_section = block_que.pop()
                if end_section[0] is None:
                    end_section = block_que.pop()
                if gap_size >= end_section[1]:
                    disk_map.append(end_section)
                else:
                    disk_map.append((end_section[0], gap_size))
                    block_que.append((end_section[0], end_section[1] - gap_size))
                gap_size -= end_section[1]
    print(get_checksum(disk_map))

    ##########
    # part 2 #
    ##########
    disk_map = [
        [int(i / 2) if i % 2 == 0 else None, size] for i, size in enumerate(sizes)
    ]
    for file in reversed([p for p in disk_map if p[0] is not None]):
        file_idx = disk_map.index(file)
        matched_gaps = [
            (n_p, p)
            for n_p, p in enumerate(disk_map)
            if p[0] is None and p[1] >= file[1]
        ]
        if len(matched_gaps) > 0:
            matched_index, matched_gap = matched_gaps[0]
            if matched_index < file_idx:
                disk_map[file_idx] = [None, file[1]]
                if matched_gap[1] == file[1]:
                    swap_list = [file]
                else:
                    swap_list = [file, [None, matched_gap[1] - file[1]]]
                disk_map = [
                    *disk_map[:matched_index],
                    *swap_list,
                    *disk_map[matched_index + 1 :],
                ]
    print(get_checksum(disk_map))


if __name__ == "__main__":
    main()
