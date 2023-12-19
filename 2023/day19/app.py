import os
import re
import math
from collections import deque


def parse_rule(text):
    return re.match(
        r"(?:(?P<rating>[xmas])(?P<operator>[<>])(?P<value>\d+):)?(?P<result>[a-z]+|A|R)",
        text,
    ).groupdict()


def evalute_rule(part, rule):
    if not rule["rating"]:
        return rule["result"]
    if eval(f'{part[rule["rating"]]} {rule["operator"]} {rule["value"]}'):
        return rule["result"]
    return None


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    data = file.read().split("\n\n")
    workflows = {
        m.groupdict()["id"]: [parse_rule(r) for r in m.groupdict()["rules"].split(",")]
        for m in re.finditer(r"(?P<id>[a-z]+){(?P<rules>[^}]+)}", data[0])
    }
    parts = [
        dict(r.split("=") for r in line[1:-1].split(","))
        for line in data[1].splitlines()
    ]

    def evalute_workflow(part, workflow):
        for r in workflows[workflow]:
            result = evalute_rule(part, r)
            if result:
                return result

    ##########
    # part 1 #
    ##########
    accepted = []
    rejected = []
    for p in parts:
        workflow = "in"
        while workflow not in ["A", "R"]:
            workflow = evalute_workflow(p, workflow)
        if workflow == "A":
            accepted.append(p)
        elif workflow == "R":
            rejected.append(p)
    print(sum(sum(map(int, a.values())) for a in accepted))

    ##########
    # part 2 #
    ##########
    workflow_ranges = deque(
        [
            (
                {
                    "x": (1, 4000),
                    "m": (1, 4000),
                    "a": (1, 4000),
                    "s": (1, 4000),
                },
                "in",
            )
        ]
    )
    accepted_ranges = []
    rejected_ranges = []
    while workflow_ranges:
        rng, rule_name = workflow_ranges.pop()
        for rule in workflows[rule_name]:
            if rng:
                if rule["rating"]:
                    rng_L = {
                        **rng.copy(),
                        rule["rating"]: (
                            rng[rule["rating"]][0],
                            int(rule["value"]) - (1 if rule["operator"] == "<" else 0),
                        ),
                    }
                    rng_H = {
                        **rng.copy(),
                        rule["rating"]: (
                            int(rule["value"]) + (1 if rule["operator"] == ">" else 0),
                            rng[rule["rating"]][-1],
                        ),
                    }
                    if rule["operator"] == "<":
                        if rule["result"] == "A":
                            accepted_ranges.append(rng_L)
                        elif rule["result"] == "R":
                            rejected_ranges.append(rng_L)
                        else:
                            workflow_ranges.append((rng_L, rule["result"]))
                        rng = rng_H
                    elif rule["operator"] == ">":
                        if rule["result"] == "A":
                            accepted_ranges.append(rng_H)
                        elif rule["result"] == "R":
                            rejected_ranges.append(rng_H)
                        else:
                            workflow_ranges.append((rng_H, rule["result"]))
                        rng = rng_L
                else:
                    if rule["result"] == "A":
                        accepted_ranges.append(rng)
                    elif rule["result"] != "R":
                        workflow_ranges.append((rng, rule["result"]))
                    else:
                        rejected_ranges.append(rng)
                    rng = None
    print(sum(math.prod(v[1] - v[0] + 1 for v in a.values()) for a in accepted_ranges))


if __name__ == "__main__":
    main()
