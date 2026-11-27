import os
from collections import deque

START_LABEL = "AA"
END_LABEL = "ZZ"

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def parse_maze(lines):
    """
    Return (open_tiles, portals): the set of walkable (row, col) tiles, and a dict
    mapping each label to the list of open tiles that sit next to it.
    """
    grid = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            grid[(row, col)] = char

    open_tiles = set()
    for tile, char in grid.items():
        if char == ".":
            open_tiles.add(tile)

    portals = {}
    for (row, col), char in grid.items():
        if not char.isupper():
            continue
        # only start from the first letter of a label (the top or left one)
        right = grid.get((row, col + 1), " ")
        below = grid.get((row + 1, col), " ")
        if right.isupper():
            label = char + right
            # the open tile is either just after the label or just before it
            candidates = [(row, col + 2), (row, col - 1)]
        elif below.isupper():
            label = char + below
            candidates = [(row + 2, col), (row - 1, col)]
        else:
            continue
        for candidate in candidates:
            if candidate in open_tiles:
                portals.setdefault(label, []).append(candidate)
    return open_tiles, portals


def portal_links(portals, open_tiles):
    """
    Map each portal tile to (tile with the same label on the other side, level change).
    Outer portals lead one level out (-1), inner portals one level deeper (+1).
    """
    # outer portal tiles sit on the outside edge of the donut
    top = min(row for row, col in open_tiles)
    bottom = max(row for row, col in open_tiles)
    left = min(col for row, col in open_tiles)
    right = max(col for row, col in open_tiles)

    links = {}
    for tiles in portals.values():
        if len(tiles) != 2:
            continue
        for tile, other_tile in ((tiles[0], tiles[1]), (tiles[1], tiles[0])):
            row, col = tile
            if row in (top, bottom) or col in (left, right):
                links[tile] = (other_tile, -1)
            else:
                links[tile] = (other_tile, 1)
    return links


def shortest_path(open_tiles, links, start, end, recursive=False):
    """
    Breadth-first search where stepping through a portal also costs one step.
    With recursive=True portals change level, outer portals are walls on the
    outermost level (0), and the end only counts on level 0.
    """
    # without a depth limit the search would never end when there's no route.
    # A route has to climb back out of every level it goes down, so in practice it
    # never needs to go deeper than there are portals.
    max_level = len(links)
    distances = {(start, 0): 0}
    queue = deque([(start, 0)])
    while queue:
        tile, level = queue.popleft()
        if tile == end and level == 0:
            return distances[(tile, level)]
        row, col = tile
        next_states = []
        for d_row, d_col in DIRECTIONS:
            next_states.append(((row + d_row, col + d_col), level))
        if tile in links:
            other_tile, level_change = links[tile]
            if not recursive:
                next_states.append((other_tile, level))
            elif 0 <= level + level_change <= max_level:
                next_states.append((other_tile, level + level_change))
        for next_state in next_states:
            if next_state[0] in open_tiles and next_state not in distances:
                distances[next_state] = distances[(tile, level)] + 1
                queue.append(next_state)
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    # leading spaces matter here, so don't strip the lines
    lines = content.splitlines()
    open_tiles, portals = parse_maze(lines)
    links = portal_links(portals, open_tiles)
    start = portals[START_LABEL][0]
    end = portals[END_LABEL][0]

    ##########
    # part 1 #
    ##########
    part_1 = shortest_path(open_tiles, links, start, end)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = shortest_path(open_tiles, links, start, end, recursive=True)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
