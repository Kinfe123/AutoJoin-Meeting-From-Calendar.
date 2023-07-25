from playwright.sync_api import Playwright, sync_playwright, expect
from threading import Event
import time
import os 
from dotenv import load_dotenv
load_dotenv()

def nuke(acc,pas,meet_url):
    def run(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        context.grant_permissions(permissions=['microphone','camera'])
        page = context.new_page()
        page.goto("https://accounts.google.com/ServiceLogin")
        page.locator("[aria-label=\"email address or phone number\"]").click()
        page.locator("[aria-label=\"email address or phone number\"]").fill(acc)
        with page.expect_navigation():
            page.locator("[aria-label=\"email address or phone number\"]").press("Enter")
        page.locator("[aria-label=\"Enter your password\"]").fill(pas)
        with page.expect_navigation():
            page.locator("[aria-label=\"Enter your password\"]").press("Enter")
        page.goto(meet_url)
        page.locator("[aria-label=\mute the microphone or turn off the microphone \\(Ctrl \\+ D\\)\"]").click()
        page.locator("[aria-label=\disable the camera or turn off the camera \\(Ctrl \\+ E\\)\"]").click()
        page.locator("button:has-text(\"Join now\")").click()
        Event().wait()

    with sync_playwright() as playwright:
        run(playwright)

if __name__ == '__main__':
 
    acc = os.getenv('EMAIL_ID')
    pas = os.getenv("PASSWORD")
    #----------------------------
    if acc == "" or pas =="":
        print("Nohing provided yet")
        exit(0)
    
    # meet_url = ""  - The meeting url get get here

    nuke(acc,pas,meet_url)