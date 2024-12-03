import os


def main():
    ##########
    # part 1 #
    ##########
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.splitlines()]
    reports = [list(map(int, line.split())) for line in lines]
    checks = [
        [report[pair] - report[pair + 1] for pair in range(len(report) - 1)]
        for report in reports
    ]
    safe = [
        all([abs(c) in range(1, 4) for c in check])
        and (all([c > 0 for c in check]) or all([c < 0 for c in check]))
        for check in checks
    ]
    print(sum(safe))

    ##########
    # part 2 #
    ##########
    safe_reports = 0
    for report in reports:
        safe = False
        checks = [report[pair] - report[pair + 1] for pair in range(len(report) - 1)]
        safe = all([abs(c) in range(1, 4) for c in checks]) and (
            all([c > 0 for c in checks]) or all([c < 0 for c in checks])
        )
        if safe:
            safe_reports += 1
        n = 0
        while not safe and n < len(report):
            sub_report = report[:n] + report[n + 1 :]
            checks = [
                sub_report[pair] - sub_report[pair + 1]
                for pair in range(len(sub_report) - 1)
            ]
            safe = all([abs(c) in range(1, 4) for c in checks]) and (
                all([c > 0 for c in checks]) or all([c < 0 for c in checks])
            )
            if safe:
                safe_reports += 1
            n += 1
    print(safe_reports)


if __name__ == "__main__":
    main()
