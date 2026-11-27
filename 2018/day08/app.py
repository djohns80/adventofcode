import os


def parse_node(numbers, index=0):
    """Read the node starting at numbers[index].

    Returns ((children, metadata), next_index), where children is a list of nodes
    in the same form and next_index is the position just after this node.
    """
    child_count = numbers[index]
    metadata_count = numbers[index + 1]
    index += 2
    children = []
    for _ in range(child_count):
        child, index = parse_node(numbers, index)
        children.append(child)
    metadata = numbers[index : index + metadata_count]
    index += metadata_count
    return (children, metadata), index


def node_value(node, metadata_as_indexes=False):
    """Return the value of a node.

    By default this is the sum of every metadata entry in the node and all of its
    descendants. With metadata_as_indexes, a node with children instead adds up
    the values of the children its metadata entries point at (1 = first child),
    skipping entries that don't refer to a child.
    """
    children, metadata = node
    if metadata_as_indexes and children:
        total = 0
        for index in metadata:
            if 1 <= index <= len(children):
                total += node_value(children[index - 1], metadata_as_indexes)
        return total
    total = sum(metadata)
    for child in children:
        total += node_value(child, metadata_as_indexes)
    return total


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    numbers = []
    for value in content.split():
        numbers.append(int(value))
    root, _ = parse_node(numbers)

    ##########
    # part 1 #
    ##########
    part_1 = node_value(root)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = node_value(root, metadata_as_indexes=True)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
