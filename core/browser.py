from playwright.sync_api import Playwright, sync_playwright, expect
from playwright_stealth import stealth_sync
from browserforge.injectors.playwright import NewContext
from browserforge.fingerprints import FingerprintGenerator
from bs4 import BeautifulSoup
from core.captcha import ffmpeg_converter, speech_to_text
import re, subprocess

def playwright_browser(playwright: Playwright, hash) -> None:
    '''
    function to crack hashes with crackstation.com
    '''
    fingerprints = FingerprintGenerator()
    fingerprint = fingerprints.generate()
    #browser = playwright.chromium.launch(headless=False, proxy={'server':'<http://proxy:port>'}, timeout=10000) # proxy option..
    browser = playwright.chromium.launch()

    context = NewContext(browser, fingerprint=fingerprint)
    page = context.new_page()
    stealth_sync(page)
    page.goto("https://crackstation.net/")
    page.get_by_role("textbox").fill(f"{hash}")
    frame = page.frames # grab frames where the captcha is stored
    try:
        audio_challenge = re.sub('a', 'c', frame[1].name, 1) # visual and audio captcha differ by a & c
    except IndexError:
        print("[-] iframe not found.. google being a buster..\n") # appears when google gets too many requests..
        return # exit if google blocks audio captcha solving

    # bypass the captcha
    print("[*] Solving captcha..", end='\r')
    page.frame_locator(f"iframe[name=\"{frame[1].name}\"]").get_by_label("I'm not a robot").click()
    page.frame_locator(f"iframe[name=\"{audio_challenge}\"]").get_by_role("button", name="Get an audio challenge").click()

    # captcha audio option pop up
    try:
        with page.expect_popup(timeout=5000) as captcha_page:
            download_link = page.frame_locator(f"iframe[name=\"{audio_challenge}\"]").get_by_role("link", name="Alternatively, download audio")
            download_url = download_link.get_attribute('href')
            print("[*] Converting to wav..")
            download = ffmpeg_converter(download_url)
            if download:
                print("[*] Converting wav to text..")
                captcha = speech_to_text('captcha.wav')
                page.frame_locator(f"iframe[name=\"{audio_challenge}\"]").get_by_label("Enter what you hear").fill(f"{captcha}")
                page.keyboard.press("Enter")
                print("[*] Captcha Solved..", end='\r')
    except:
        pass # don't know how to handle the closing of the popup..

    page.get_by_role("button", name="Crack Hashes").click()
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser') # don't even need to do this tbh..
    matches = re.findall(r'<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>', str(soup)) # results stored here
    subprocess.run(['clear'], shell=True)
    if matches:
        for match in matches: # if multiple hashes (results), loop through each result
            hash_value, type_value, result_value = match
            print(f"Hash: {hash_value.strip()}")
            print(f"Type: {type_value.strip()}")
            print(f"Result: {result_value.strip()}\n")

    context.close()
    browser.close()