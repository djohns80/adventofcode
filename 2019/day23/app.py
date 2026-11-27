import os
from collections import defaultdict, deque

COMPUTER_COUNT = 50
NAT_ADDRESS = 255  # packets sent here go to the NAT
WAKE_ADDRESS = 0  # the NAT sends its packet here when the network is idle
EMPTY_QUEUE = -1  # input given to a computer with no packets waiting
MAX_ROUNDS = 100_000  # safety limit so a broken network can't loop forever


class Intcode:
    """An Intcode computer (2019 days 2, 5, 7 and 9 rules).

    Queue values with `send`, call `run`, then read `outputs`. `run` returns when
    the program halts or when it needs an input that hasn't been queued yet, so it
    can be resumed later for interactive puzzles.
    """

    def __init__(self, program):
        # memory beyond the program reads as 0
        self.memory = defaultdict(int, enumerate(program))
        self.ip = 0
        self.relative_base = 0
        self.inputs = deque()
        self.outputs = []
        self.halted = False

    def send(self, *values):
        self.inputs.extend(values)

    def address(self, offset):
        """Memory address of the parameter at ip + offset, using its mode."""
        mode = self.memory[self.ip] // (10 ** (offset + 1)) % 10
        if mode == 0:  # position
            return self.memory[self.ip + offset]
        if mode == 1:  # immediate
            return self.ip + offset
        return self.relative_base + self.memory[self.ip + offset]  # relative

    def value(self, offset):
        return self.memory[self.address(offset)]

    def run(self):
        while True:
            opcode = self.memory[self.ip] % 100
            match opcode:
                case 1:
                    self.memory[self.address(3)] = self.value(1) + self.value(2)
                    self.ip += 4
                case 2:
                    self.memory[self.address(3)] = self.value(1) * self.value(2)
                    self.ip += 4
                case 3:
                    if not self.inputs:
                        return  # wait for more input
                    self.memory[self.address(1)] = self.inputs.popleft()
                    self.ip += 2
                case 4:
                    self.outputs.append(self.value(1))
                    self.ip += 2
                case 5:
                    self.ip = self.value(2) if self.value(1) != 0 else self.ip + 3
                case 6:
                    self.ip = self.value(2) if self.value(1) == 0 else self.ip + 3
                case 7:
                    self.memory[self.address(3)] = int(self.value(1) < self.value(2))
                    self.ip += 4
                case 8:
                    self.memory[self.address(3)] = int(self.value(1) == self.value(2))
                    self.ip += 4
                case 9:
                    self.relative_base += self.value(1)
                    self.ip += 2
                case 99:
                    self.halted = True
                    return
                case _:
                    raise ValueError(f"unknown opcode {opcode} at {self.ip}")


def boot_network(program, computer_count):
    """Start one computer per address, each told its own network address."""
    computers = []
    for network_address in range(computer_count):
        computer = Intcode(program)
        computer.send(network_address)
        computers.append(computer)
    return computers


def run_round(computers):
    """Run every computer until it waits for input; return the packets they sent.

    A computer with nothing in its queue is given -1, so input never blocks.
    Each packet is a (destination, x, y) tuple, taken from outputs in threes.
    """
    packets = []
    for computer in computers:
        if not computer.inputs:
            computer.send(EMPTY_QUEUE)
        computer.run()
        outputs = computer.outputs
        # keep any incomplete packet for the next round
        complete_length = len(outputs) - len(outputs) % 3
        for index in range(0, complete_length, 3):
            packets.append(tuple(outputs[index : index + 3]))
        computer.outputs = outputs[complete_length:]
    return packets


def run_network(program, computer_count, nat_address, max_rounds, use_nat=False):
    """Run the network and return a Y value.

    Without the NAT, return the Y of the first packet sent to nat_address.
    With the NAT, it keeps only the last packet sent to nat_address and
    delivers it to address 0 whenever the network goes idle; return the first
    Y it delivers twice in a row.
    """
    computers = boot_network(program, computer_count)
    nat_packet = None
    last_delivered_y = None
    for _ in range(max_rounds):
        packets = run_round(computers)
        for destination, x, y in packets:
            if destination == nat_address:
                if not use_nat:
                    return y
                nat_packet = (x, y)
            else:
                computers[destination].send(x, y)

        # idle: nobody sent anything and every computer is still waiting for input
        idle = not packets and all(not computer.inputs for computer in computers)
        if use_nat and idle and nat_packet is not None:
            x, y = nat_packet
            if y == last_delivered_y:
                return y
            computers[WAKE_ADDRESS].send(x, y)
            last_delivered_y = y
    raise RuntimeError(f"no answer after {max_rounds} rounds")


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    program = [int(value) for value in content.split(",")]

    ##########
    # part 1 #
    ##########
    part_1 = run_network(program, COMPUTER_COUNT, NAT_ADDRESS, MAX_ROUNDS)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = run_network(program, COMPUTER_COUNT, NAT_ADDRESS, MAX_ROUNDS, use_nat=True)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
