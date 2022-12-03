#!/usr/bin/env python3
""" This script downloads a specified advent of code input file.
    It defaults to the current day/year but parameters can be used to define a specific day or year (or both). """

import argparse
import logging
import os
from datetime import date

import requests

import aoc_cookies

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')

def download_input(cookies: list, year: int, day: int):
    """ download the input file """
    if not cookies:
        logging.warning('No Cookies found. Will attempt request without cookies...')
    headers = {'Cookie': '; '.join([f'{c[0]}={c[1]}' for c in cookies])}
    req = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', headers=headers, timeout=30)
    if req.status_code != 200:
        logging.error('Unable to download input... %s', req.content.decode('utf-8'))
        return
    input_file = f'./{year}/day{day:02}/input'
    os.makedirs(os.path.dirname(input_file), exist_ok=True)
    logging.info('Writing file to: %s...', input_file)
    open(input_file, 'wb').write(req.content)
    return input_file

def main(browser: str, year:int , day: int):
    """ Download the inout for a specific day of advent of code """
    cookies = aoc_cookies.get_cookies(browser)
    download_input(cookies, year, day)

if __name__ == '__main__':
    today = date.today()
    parser = argparse.ArgumentParser(description='This script downloads the puzzle input for Advent of Code.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--firefox', action='store_const', dest='browser', const='firefox', help='use Firefox')
    group.add_argument('-c', '--chrome', action='store_const', dest='browser', const='chrome', help='use Chrome')
    parser.add_argument('-y', '--year', default=today.year, type=int, help='defaults to current year')
    parser.add_argument('-d', '--day', default=today.day, type=int, help='defaults to current day')
    parser.set_defaults(browser='firefox')
    args = parser.parse_args()
    for arg, value in sorted(vars(args).items()):
        logging.info('Argument %s: %r', arg, value)
    main(args.browser, args.year, args.day)
