import os
from dataclasses import dataclass

# (dx, dy) for each cart symbol; y grows downwards
CART_DIRECTIONS = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
# the straight track hidden underneath each cart symbol
TRACK_UNDER_CART = {"^": "|", "v": "|", "<": "-", ">": "-"}
# what a cart does at successive intersections, repeating forever
INTERSECTION_CHOICES = ("left", "straight", "right")


@dataclass
class Cart:
    x: int
    y: int
    dx: int
    dy: int
    intersections_passed: int = 0
    crashed: bool = False


def parse_tracks(lines):
    """Split the map into the bare track grid and the carts sitting on it."""
    track = []
    carts = []
    for y, line in enumerate(lines):
        row = []
        for x, char in enumerate(line):
            if char in CART_DIRECTIONS:
                dx, dy = CART_DIRECTIONS[char]
                carts.append(Cart(x, y, dx, dy))
                row.append(TRACK_UNDER_CART[char])
            else:
                row.append(char)
        track.append(row)
    return track, carts


def move_cart(cart, track):
    """Move one cart a single step, then turn it according to the track it lands on."""
    cart.x += cart.dx
    cart.y += cart.dy
    piece = track[cart.y][cart.x]
    if piece == "/":
        cart.dx, cart.dy = -cart.dy, -cart.dx
    elif piece == "\\":
        cart.dx, cart.dy = cart.dy, cart.dx
    elif piece == "+":
        choice = INTERSECTION_CHOICES[
            cart.intersections_passed % len(INTERSECTION_CHOICES)
        ]
        if choice == "left":
            cart.dx, cart.dy = cart.dy, -cart.dx
        elif choice == "right":
            cart.dx, cart.dy = -cart.dy, cart.dx
        cart.intersections_passed += 1


def tick(track, carts):
    """
    Move every cart that hasn't crashed one step, in reading order.
    Carts that collide are marked as crashed straight away, so a collision can
    happen part way through a tick. Returns crash locations in the order they happened.
    """
    crashes = []
    for cart in sorted(carts, key=lambda c: (c.y, c.x)):
        if cart.crashed:
            continue
        move_cart(cart, track)
        for other in carts:
            if other is cart or other.crashed:
                continue
            if other.x == cart.x and other.y == cart.y:
                cart.crashed = True
                other.crashed = True
                crashes.append((cart.x, cart.y))
                break
    return crashes


def run_carts(track, carts, until_last_cart=False):
    """
    Tick until the first crash and return its location. With until_last_cart,
    crashed carts are removed instead and this returns the last cart's location
    at the end of the first tick where it is the only cart left.
    """
    while True:
        crashes = tick(track, carts)
        if not until_last_cart:
            if crashes:
                return crashes[0]
            continue
        remaining = []
        for cart in carts:
            if not cart.crashed:
                remaining.append(cart)
        if len(remaining) == 1:
            return remaining[0].x, remaining[0].y


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    track, carts = parse_tracks(lines)

    ##########
    # part 1 #
    ##########
    crash_x, crash_y = run_carts(track, carts)
    part_1 = f"{crash_x},{crash_y}"
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # part 1 moved the carts, so start again from the original map
    track, carts = parse_tracks(lines)
    last_x, last_y = run_carts(track, carts, until_last_cart=True)
    part_2 = f"{last_x},{last_y}"
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
