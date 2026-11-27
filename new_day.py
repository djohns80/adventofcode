#!/usr/bin/env python3
"""Start an Advent of Code day.

Creates YYYY/dayDD/app.py from the template, waits for the puzzle to unlock if run
early, saves the first example on the puzzle page as `sample`, downloads `input`, then
opens app.py in VS Code. It defaults to today and never overwrites an existing file,
so it is safe to run again.
"""

import argparse
import logging
import os
import shutil
import subprocess
import time
from datetime import UTC, date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

import aoc_cookies
from get_input import download_input, request_headers

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s"
)
logger = logging.getLogger(__name__)

REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
UNLOCK_HOUR_UTC = (
    5  # puzzles unlock at midnight US Eastern, which is 05:00 UTC in December
)
MAX_WAIT = timedelta(hours=24)  # refuse to sit waiting for days if the date is wrong

TEMPLATE = """\
import os


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()

    ##########
    # part 1 #
    ##########
    # print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # print("part 2:", part_2)


if __name__ == "__main__":
    main()
"""


def unlock_time(year, day):
    return datetime(year, 12, day, UNLOCK_HOUR_UTC, tzinfo=UTC)


def wait_until(unlock):
    """Show a countdown until the unlock time, then return."""
    if datetime.now(UTC) >= unlock:
        return
    while (remaining := unlock - datetime.now(UTC)) > timedelta(0):
        hours, rest = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(rest, 60)
        print(
            f"\rPuzzle unlocks in {hours:02}:{minutes:02}:{seconds:02} ",
            end="",
            flush=True,
        )
        time.sleep(min(remaining.total_seconds(), 1))
    print()
    time.sleep(2)  # small buffer in case our clock is slightly ahead of the server's


def fetch_puzzle_page(cookies, year, day, attempts=5):
    """The puzzle page's HTML, retrying briefly in case it has only just unlocked."""
    for _ in range(attempts):
        req = requests.get(
            f"https://adventofcode.com/{year}/day/{day}",
            headers=request_headers(cookies),
            timeout=30,
        )
        if req.status_code != 404:
            req.raise_for_status()
            return req.text
        time.sleep(5)
    raise RuntimeError(f"{year} day {day} still isn't available")


def parse_puzzle_page(html):
    """The puzzle title and the text of the first example block (or None)."""
    article = BeautifulSoup(html, "html.parser").find("article")
    if article is None:
        return None, None
    title = article.find("h2").get_text()
    first_example = article.find("pre")
    return title, first_example.get_text() if first_example else None


def write_if_missing(path, text, description):
    if os.path.exists(path):
        logger.info("%s already exists, leaving it alone: %s", description, path)
        return
    # newline="\n" keeps Unix line endings on Windows, matching .gitattributes
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)
    logger.info("Created %s: %s", description, path)


def open_in_editor(path):
    code = shutil.which("code")
    if code is None:
        logger.info("VS Code's `code` command wasn't found, open %s yourself", path)
        return
    subprocess.run([code, "--reuse-window", path], check=False)


def main(browser, year, day, open_editor):
    os.chdir(REPO_ROOT)  # get_input writes the input relative to the current directory
    unlock = unlock_time(year, day)
    if unlock - datetime.now(UTC) > MAX_WAIT:
        logger.error(
            "%s day %s doesn't unlock until %s, pass -y/-d for another day",
            year,
            day,
            unlock,
        )
        return

    folder = os.path.join(str(year), f"day{day:02}")
    os.makedirs(folder, exist_ok=True)
    app_path = os.path.join(folder, "app.py")
    write_if_missing(app_path, TEMPLATE, "app.py")

    # reading the browser's cookies can take a few seconds, so do it before the countdown
    cookies = aoc_cookies.get_cookies(browser)
    wait_until(unlock)

    sample_path = os.path.join(folder, "sample")
    html = fetch_puzzle_page(cookies, year, day)
    title, example = parse_puzzle_page(html)
    if title:
        logger.info("%s", title)
    if example is None:
        logger.warning(
            "No example block found on the puzzle page: paste the example into %s",
            sample_path,
        )
    else:
        # a guess: usually the first example is the one to test with, so check it
        write_if_missing(sample_path, example, "sample (check it's the right example)")

    if os.path.exists(os.path.join(folder, "input")):
        logger.info("input already exists, not downloading it again")
    else:
        download_input(cookies, year, day)

    if open_editor:
        open_in_editor(app_path)


if __name__ == "__main__":
    today = date.today()
    parser = argparse.ArgumentParser(
        description="Set up a day of Advent of Code and wait for it to unlock."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-f",
        "--firefox",
        action="store_const",
        dest="browser",
        const="firefox",
        help="use Firefox",
    )
    group.add_argument(
        "-c",
        "--chrome",
        action="store_const",
        dest="browser",
        const="chrome",
        help="use Chrome",
    )
    parser.add_argument(
        "-y", "--year", default=today.year, type=int, help="defaults to current year"
    )
    parser.add_argument(
        "-d", "--day", default=today.day, type=int, help="defaults to current day"
    )
    parser.add_argument(
        "--no-open",
        action="store_false",
        dest="open_editor",
        help="don't open app.py in VS Code",
    )
    parser.set_defaults(browser="firefox")
    args = parser.parse_args()
    main(args.browser, args.year, args.day, args.open_editor)
