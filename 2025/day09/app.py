import os
import math
from shapely.geometry import Polygon, box


def get_area(tile_a, tile_b):
    return math.prod(abs(a - b) + 1 for a, b in zip(tile_a, tile_b))


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    tiles = [tuple(int(c) for c in line.split(",")) for line in lines]
    areas = [
        (get_area(tiles[i], tiles[j]), tiles[i], tiles[j])
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
    ]
    areas.sort(reverse=True)

    ##########
    # part 1 #
    ##########
    print("part 1:", areas[0][0])

    ##########
    # part 2 #
    ##########
    polygon = Polygon(tiles)
    for area, tile_a, tile_b in areas:
        rect = box(*tile_a, *tile_b)
        if polygon.covers(rect):
            print("part 2:", area)
            break


if __name__ == "__main__":
    main()
