#!/usr/bin/env python3
"""This script submits an answer to Advent of Code.

It defaults to the current day/year, and works out the level (part 1 or 2) from the
puzzle page unless one is given. Wrong answers are remembered in .submitted_answers.json
so the same answer is never sent twice, and "too high"/"too low" hints rule out any
answer that can't be right. AoC makes you wait longer after each wrong answer.
"""

import argparse
import json
import logging
import os
import re
from datetime import date

import requests
from bs4 import BeautifulSoup

import aoc_cookies
from get_input import request_headers

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s"
)
logger = logging.getLogger(__name__)

HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), ".submitted_answers.json"
)


def load_history():
    """Wrong answers submitted so far, keyed by "year/day/level"."""
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def detect_level(cookies, year, day):
    """The next unsolved part (1 or 2), or None if both are already solved."""
    req = requests.get(
        f"https://adventofcode.com/{year}/day/{day}",
        headers=request_headers(cookies),
        timeout=30,
    )
    req.raise_for_status()
    solved_parts = req.text.count("Your puzzle answer was")
    if solved_parts >= 2:
        return None
    return solved_parts + 1


def reason_not_to_submit(wrong_answers, answer):
    """Why the answer can't be right, judging by earlier wrong answers, or None."""
    for wrong in wrong_answers:
        if wrong["answer"] == answer:
            hint = f" ({wrong['hint']})" if wrong["hint"] else ""
            return f"{answer} was already rejected{hint}"
    if not re.fullmatch(r"-?\d+", answer):
        return None
    for wrong in wrong_answers:
        if wrong["hint"] == "too high" and int(answer) >= int(wrong["answer"]):
            return f"{answer} can't be right, {wrong['answer']} was already too high"
        if wrong["hint"] == "too low" and int(answer) <= int(wrong["answer"]):
            return f"{answer} can't be right, {wrong['answer']} was already too low"
    return None


def post_answer(cookies, year, day, level, answer):
    """Submit the answer and return (result, message).

    result is "right", "wrong", "wait", "solved" (that level is already done),
    "error" or "unknown"; message is the text of AoC's response.
    """
    req = requests.post(
        f"https://adventofcode.com/{year}/day/{day}/answer",
        headers=request_headers(cookies),
        data={"level": level, "answer": answer},  # requests URL-encodes the answer
        timeout=30,
    )
    if req.status_code != 200:
        return "error", req.text
    main_section = BeautifulSoup(req.text, "html.parser").find("main")
    message = " ".join(main_section.get_text().split()) if main_section else req.text
    if "That's the right answer" in message:
        return "right", message
    if "not the right answer" in message:
        return "wrong", message
    if "answer too recently" in message:
        return "wait", message
    if "the right level" in message:
        return "solved", message
    return "unknown", message


def main(browser, year, day, level, answer):
    """Submit an answer for a specific day of advent of code, returning the result."""
    answer = answer.strip()
    cookies = aoc_cookies.get_cookies(browser)
    if level is None:
        level = detect_level(cookies, year, day)
        if level is None:
            logger.info("Both parts of %s day %s are already solved.", year, day)
            return "solved"
        logger.info("Submitting %s for part %s", answer, level)

    history = load_history()
    key = f"{year}/{day:02}/{level}"
    wrong_answers = history.get(key, [])
    reason = reason_not_to_submit(wrong_answers, answer)
    if reason:
        logger.warning("Not submitted: %s", reason)
        return "skipped"

    result, message = post_answer(cookies, year, day, level, answer)
    match result:
        case "right":
            logger.info("RIGHT! %s", message)
        case "wrong":
            hint = re.search(r"your answer is too (high|low)", message)
            wrong_answers.append(
                {"answer": answer, "hint": f"too {hint.group(1)}" if hint else None}
            )
            history[key] = wrong_answers
            save_history(history)
            logger.warning(
                "WRONG%s. %s", f" (too {hint.group(1)})" if hint else "", message
            )
        case "wait":
            wait = re.search(r"You have (.+?) left to wait", message)
            logger.warning(
                "WAIT %s before submitting again.", wait.group(1) if wait else "a bit"
            )
        case "solved":
            logger.info("Part %s of %s day %s is already solved.", level, year, day)
        case _:
            logger.error("Unexpected response: %s", message)
    return result


if __name__ == "__main__":
    today = date.today()
    parser = argparse.ArgumentParser(
        description="This script submits an answer to Advent of Code."
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
        "-l",
        "--level",
        type=int,
        choices=(1, 2),
        help="part 1 or 2, worked out if not given",
    )
    parser.add_argument(
        "-a", "--answer", type=str, required=True, help="the answer to submit"
    )
    parser.set_defaults(browser="firefox")
    args = parser.parse_args()
    main(args.browser, args.year, args.day, args.level, args.answer)
