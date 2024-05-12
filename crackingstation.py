from playwright.sync_api import Playwright, sync_playwright, expect
import argparse, os
from core.browser import playwright_browser

parser = argparse.ArgumentParser(description='Hash Cracker using CrackingStation.com', usage='python3 crackstation.py --hash <hash> [hash.txt]')
parser.add_argument('--hash', help='specify hash to crack [single hash or file]', type=str, required=True)
args = parser.parse_args()
hash_text = args.hash

if hash_text and os.path.isfile(hash_text):
    with open(hash_text, 'r') as file:
        hashes_list = file.readlines()
        hash_text = ''.join(hashes_list)

with sync_playwright() as playwright:
    playwright_browser(playwright, hash_text)
