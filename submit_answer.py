#!/usr/bin/env python3
""" This script submits a specified answer to advent of code.
    It defaults to the current day/year but parameters can be used to define a specific day or year (or both). """

import argparse
import logging
from datetime import date

import requests
from bs4 import BeautifulSoup

import aoc_cookies

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')

def post_answer(cookies: list, year: int, day: int, level: int, answer: str):
    """ submit the answer """
    if not cookies:
        logging.warning('No Cookies found. Will attempt request without cookies...')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '; '.join([f'{c[0]}={c[1]}' for c in cookies])
    }
    req = requests.post(f'https://adventofcode.com/{year}/day/{day}/answer', headers=headers, data=f'level={level}&answer={answer}', timeout=30)
    if req.status_code != 200:
        logging.error('Unable to submit answer... %s', req.content.decode('utf-8'))
        return
    soup = BeautifulSoup(req.content.decode('utf-8').replace('\n','').split('<main>')[1].split('</main>')[0], features='html.parser')
    logging.info('****************************** RESPONSE ******************************')
    logging.info(soup.get_text())

def main(browser: str, year: int, day: int, level:int, answer: str):
    """ Download the inout for a specific day of advent of code """
    cookies = aoc_cookies.get_cookies(browser)
    post_answer(cookies, year, day, level, answer)

if __name__ == '__main__':
    today = date.today()
    parser = argparse.ArgumentParser(description='This script submits an answer to Advent of Code.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--firefox', action='store_const', dest='browser', const='firefox', help='use Firefox')
    group.add_argument('-c', '--chrome', action='store_const', dest='browser', const='chrome', help='use Chrome')
    parser.add_argument('-y', '--year', default=today.year, type=int, help='defaults to current year')
    parser.add_argument('-d', '--day', default=today.day, type=int, help='defaults to current day')
    parser.add_argument('-l', '--level', default=1, type=int, help='answer level defaults to 1')
    parser.add_argument('-a', '--answer', type=str, help='the answer to submit')
    parser.set_defaults(browser='firefox')
    args = parser.parse_args()
    for arg, value in sorted(vars(args).items()):
        logging.info('Argument %s: %r', arg, value)
    main(args.browser, args.year, args.day, args.level, args.answer)
