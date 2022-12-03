#!/usr/bin/env python3
""" This script downloads a specified advent of code input file.
    It defaults to the current day/year but parameters can be used to define a specific day or year (or both). """

import argparse
import base64
import json
import logging
import os
import sqlite3
from datetime import date

import requests
from win32 import win32crypt
from Cryptodome.Cipher import AES

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')

def get_cookies(browser: str):
    """ Get the advent of code cookies from specified browser """
    if browser == 'firefox':
        return get_cookies_firefox()
    elif browser == 'chrome':
        return get_cookies_chrome()
    else:
        return []

def get_cookies_firefox():
    """ Get the advent of code cookies from Firefox """
    profiles_dir = os.path.join(os.path.expanduser('~'), 'AppData/Roaming/Mozilla/Firefox/Profiles')
    db_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(profiles_dir) for f in filenames if f == 'cookies.sqlite']
    for db_file in db_files:
        logging.info('Reading sqlite db from: %s...', db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        try:
            rows = cursor.execute('SELECT name, value FROM moz_cookies WHERE host = ".adventofcode.com"').fetchall()
            logging.info('Cookies found...')
            return rows
        except sqlite3.OperationalError:
            logging.warning('Cookies not found...')
    return []

def get_cookies_chrome():
    """ Get the advent of code cookies from Google Chrome """
    user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData/Local/Google/Chrome/User Data')
    encrypted_key = None
    with open(os.path.join(user_data_dir, 'Local State'), 'r', encoding='utf-8') as file:
        encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key)
    encrypted_key = encrypted_key[5:]
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    db_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.path.join(user_data_dir, 'Default/Network')) for f in filenames if f == 'Cookies']
    if len(db_files) > 0:
        db_file = db_files[0]
        logging.info('Reading sqlite db from: %s...', db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        try:
            rows = cursor.execute('SELECT name, encrypted_value FROM cookies WHERE host_key = ".adventofcode.com"').fetchall()
            logging.info('Cookies found...')
            decrypted_rows = []
            for name, encrypted_value in rows:
                cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=encrypted_value[3:3+12])
                decrypted_value = cipher.decrypt_and_verify(encrypted_value[3+12:-16], encrypted_value[-16:])
                decrypted_rows.append((name, decrypted_value.decode('utf-8')))
            return decrypted_rows
        except sqlite3.OperationalError:
            logging.warning('Cookies not found...')
    return []

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

def main(params: argparse.Namespace):
    """ Download the inout for a specific day of advent of code """
    cookies = get_cookies(params.browser)
    download_input(cookies, params.year, params.day)

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
    main(args)
