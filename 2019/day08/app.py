import os

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6
WHITE = "1"
TRANSPARENT = "2"


def split_layers(digits, width, height):
    """Split the image data into layers of width * height digits each."""
    layer_size = width * height
    layers = []
    for start in range(0, len(digits), layer_size):
        layers.append(digits[start : start + layer_size])
    return layers


def corruption_check(layers):
    """On the layer with the fewest 0 digits, multiply the counts of 1s and 2s."""
    fewest_zeros_layer = layers[0]
    for layer in layers:
        if layer.count("0") < fewest_zeros_layer.count("0"):
            fewest_zeros_layer = layer
    return fewest_zeros_layer.count("1") * fewest_zeros_layer.count("2")


def decode_image(layers):
    """Return the visible pixels: at each position, the first non-transparent one."""
    image = ""
    for position in range(len(layers[0])):
        for layer in layers:
            if layer[position] != TRANSPARENT:
                image += layer[position]
                break
    return image


def render(image, width):
    """Return the image as text rows, drawing white pixels as '#'."""
    rows = []
    # each row is a "layer" one pixel tall
    for pixels in split_layers(image, width, 1):
        row = ""
        for pixel in pixels:
            if pixel == WHITE:
                row += "#"
            else:
                row += " "
        rows.append(row)
    return rows


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    digits = lines[0]
    layers = split_layers(digits, IMAGE_WIDTH, IMAGE_HEIGHT)

    ##########
    # part 1 #
    ##########
    part_1 = corruption_check(layers)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = render(decode_image(layers), IMAGE_WIDTH)
    print("part 2:")
    for row in part_2:
        print(row)


if __name__ == "__main__":
    main()
