import os


def get_distance(box_a, box_b):
    return sum((a - b) ** 2 for a, b in zip(box_a, box_b))


def main():
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if size[px] < size[py]:
            px, py = py, px
        parent[py] = px
        size[px] += size[py]
        return True

    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    boxes = [tuple(int(c) for c in line.split(",")) for line in lines]
    distances = [
        (get_distance(boxes[i], boxes[j]), i, j)
        for i in range(len(boxes))
        for j in range(i + 1, len(boxes))
    ]
    distances.sort()

    ##########
    # part 1 #
    ##########
    parent = list(range(len(boxes)))
    size = [1] * len(boxes)

    for processed, (_, i, j) in enumerate(distances, 1):
        union(i, j)
        if processed == 1000:
            circuit_sizes = [size[i] for i in range(len(boxes)) if find(i) == i]
            circuit_sizes.sort(reverse=True)
            part_1 = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
            print("part 1:", part_1)
            break

    ##########
    # part 2 #
    ##########
    for _, i, j in distances[1000:]:
        if union(i, j):
            if size[find(i)] == len(boxes):
                print("part 2:", boxes[i][0] * boxes[j][0])
                break


if __name__ == "__main__":
    main()
