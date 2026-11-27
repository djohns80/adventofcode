import os

BASE_PATTERN = (0, 1, 0, -1)
PHASES = 100
MESSAGE_LENGTH = 8
SIGNAL_REPEATS = 10000
OFFSET_DIGITS = 7


def run_phase(signal):
    """Return the output list of one FFT phase."""
    length = len(signal)
    # prefix_sums[i] is the sum of signal[:i], so any run of digits sums in O(1)
    prefix_sums = [0]
    for digit in signal:
        prefix_sums.append(prefix_sums[-1] + digit)

    output = []
    for position in range(length):
        repeat = position + 1
        # The pattern is blocks of `repeat` copies of each base value. With the
        # first value skipped, block k covers indexes k * repeat - 1 onwards.
        total = 0
        block = 0
        block_start = -1
        while block_start < length:
            multiplier = BASE_PATTERN[block % len(BASE_PATTERN)]
            if multiplier != 0:
                start = max(block_start, 0)
                end = min(block_start + repeat, length)
                total += multiplier * (prefix_sums[end] - prefix_sums[start])
            block += 1
            block_start += repeat
        output.append(abs(total) % 10)
    return output


def run_second_half_phase(digits):
    """Return one FFT phase for digits taken from the second half of a signal.

    For output position i, the pattern is 0 before i and then 1 for the next
    i + 1 digits. In the second half that run of 1s reaches past the end, so
    each output digit is just the sum of the input digits from i to the end.
    Working backwards from the end turns that into one running sum.
    """
    output = [0] * len(digits)
    running_sum = 0
    for index in range(len(digits) - 1, -1, -1):
        running_sum += digits[index]
        output[index] = running_sum % 10
    return output


def run_fft(signal, phases, offset=0):
    """Return the final output list, from offset onwards, after the given phases."""
    if offset < len(signal) // 2:
        for _ in range(phases):
            signal = run_phase(signal)
        return signal[offset:]

    # Digits in the second half only depend on digits after them, so the
    # digits before the offset never need to be calculated.
    digits = signal[offset:]
    for _ in range(phases):
        digits = run_second_half_phase(digits)
    return digits


def digits_to_text(digits):
    text = ""
    for digit in digits:
        text += str(digit)
    return text


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    signal = []
    for char in lines[0]:
        signal.append(int(char))

    ##########
    # part 1 #
    ##########
    output = run_fft(signal, PHASES)
    part_1 = digits_to_text(output[:MESSAGE_LENGTH])
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    real_signal = signal * SIGNAL_REPEATS
    offset = int(digits_to_text(signal[:OFFSET_DIGITS]))
    output = run_fft(real_signal, PHASES, offset)
    part_2 = digits_to_text(output[:MESSAGE_LENGTH])
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
