#!/usr/bin/env python3

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def turn_left(direction):
    if direction == UP:
        return LEFT
    elif direction == LEFT:
        return DOWN
    elif direction == DOWN:
        return RIGHT
    elif direction == RIGHT:
        return UP
    else:
        raise ValueError(f"Invalid direction {direction}")


def turn_right(direction):
    if direction == UP:
        return RIGHT
    elif direction == RIGHT:
        return DOWN
    elif direction == DOWN:
        return LEFT
    elif direction == LEFT:
        return UP
    else:
        raise ValueError(f"Invalid direction {direction}")


def reverse(direction):
    if direction == UP:
        return DOWN
    elif direction == RIGHT:
        return LEFT
    elif direction == DOWN:
        return UP
    elif direction == LEFT:
        return RIGHT
    else:
        raise ValueError(f"Invalid direction {direction}")


def char_to_direc(char):
    if char == "^":
        return UP
    elif char == ">":
        return RIGHT
    elif char == "<":
        return LEFT
    elif char == "v":
        return DOWN
    else:
        raise ValueError(f"Invalid character {char}")
