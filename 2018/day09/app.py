import os
from collections import deque

SCORING_MULTIPLE = 23
REMOVE_COUNTER_CLOCKWISE = 7
LAST_MARBLE_MULTIPLIER = 100


def play_game(player_count, last_marble):
    """Play the marble game and return the winning Elf's score."""
    scores = [0] * player_count
    # The current marble is always kept at the right-hand end of the deque, and
    # clockwise means moving to the right (wrapping round to the left end).
    circle = deque([0])
    for marble in range(1, last_marble + 1):
        player = (marble - 1) % player_count
        if marble % SCORING_MULTIPLE == 0:
            # Bring the marble 7 counter-clockwise round to the end and take it,
            # then make the marble clockwise of it the current one.
            circle.rotate(REMOVE_COUNTER_CLOCKWISE)
            scores[player] += marble + circle.pop()
            circle.rotate(-1)
        else:
            # Step one clockwise, then add the new marble just after it.
            circle.rotate(-1)
            circle.append(marble)
    return max(scores)


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    # "459 players; last marble is worth 72103 points"
    words = content.split()
    player_count = int(words[0])
    last_marble = int(words[6])

    ##########
    # part 1 #
    ##########
    part_1 = play_game(player_count, last_marble)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = play_game(player_count, last_marble * LAST_MARBLE_MULTIPLIER)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
