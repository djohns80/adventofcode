import os
import math
from collections import deque, defaultdict


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))

    def parse_data():
        data = {}
        for line in lines:
            module, outputs = line.split(" -> ")
            module_type = "broadcast"
            if module != "broadcaster":
                module_type = module[0]
                module = module[1:]
            data[module] = {
                "type": module_type,
                "outputs": outputs.split(", "),
                "state": None if module_type != "%" else "off",
                "last_inputs": {},
            }
        conjunction_inputs = {
            ck: [ok for ok, ov in data.items() if ck in ov["outputs"]]
            for ck, cv in data.items()
            if cv["type"] == "&"
        }
        for c, inputs in conjunction_inputs.items():
            data[c]["last_inputs"] = {i: "low" for i in inputs}
        return data

    ##########
    # part 1 #
    ##########
    modules = parse_data()
    counts = defaultdict(int)
    for _ in range(1000):
        counts["low"] += 1
        pulses = deque([("button", "low", "broadcaster")])
        while pulses:
            source, pulse, module_name = pulses.popleft()
            if module_name in modules:
                module = modules[module_name]
                match module["type"]:
                    case "%":
                        if pulse == "high":
                            pass
                        elif pulse == "low":
                            module["state"] = (
                                "on" if module["state"] == "off" else "off"
                            )
                            new_pulse = "high" if module["state"] == "on" else "low"
                            for o in module["outputs"]:
                                counts[new_pulse] += 1
                                pulses.append((module_name, new_pulse, o))
                    case "&":
                        module["last_inputs"][source] = pulse
                        new_pulse = (
                            "low"
                            if all(v == "high" for v in module["last_inputs"].values())
                            else "high"
                        )
                        for o in module["outputs"]:
                            counts[new_pulse] += 1
                            pulses.append((module_name, new_pulse, o))
                    case "broadcast":
                        for o in module["outputs"]:
                            counts[pulse] += 1
                            pulses.append((module_name, pulse, o))
    print(math.prod(counts.values()))

    ##########
    # part 2 #
    ##########
    modules = parse_data()
    rx_source = [name for name, m in modules.items() if "rx" in m["outputs"]][0]
    rx_dependants = {
        name: 0 for name, m in modules.items() if rx_source in m["outputs"]
    }
    n = 0
    while any([v == 0 for v in rx_dependants.values()]):
        n += 1
        pulses = deque([("button", "low", "broadcaster")])
        while pulses:
            source, pulse, module_name = pulses.popleft()
            if module_name in modules:
                module = modules[module_name]
                match module["type"]:
                    case "%":
                        if pulse == "high":
                            pass
                        elif pulse == "low":
                            module["state"] = (
                                "on" if module["state"] == "off" else "off"
                            )
                            new_pulse = "high" if module["state"] == "on" else "low"
                            for o in module["outputs"]:
                                pulses.append((module_name, new_pulse, o))
                    case "&":
                        module["last_inputs"][source] = pulse
                        new_pulse = (
                            "low"
                            if all(v == "high" for v in module["last_inputs"].values())
                            else "high"
                        )
                        if new_pulse == "high" and module_name in [
                            k for k, v in rx_dependants.items() if v == 0
                        ]:
                            rx_dependants[module_name] = n
                        for o in module["outputs"]:
                            pulses.append((module_name, new_pulse, o))
                    case "broadcast":
                        for o in module["outputs"]:
                            pulses.append((module_name, pulse, o))
    print(math.lcm(*rx_dependants.values()))


if __name__ == "__main__":
    main()
