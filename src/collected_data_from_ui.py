"""There is module to provide functions to collecting data from UI."""

import logging
from os import environ
from time import sleep
from playwright.sync_api import Playwright

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", level=logging.INFO)


def run(playwright: Playwright) -> list:
    """Running Playwright, log in to web application and return list with cookies.

    :param playwright: Playwright instance.
    :return: List of cookies.
    """
    logger.info("Playwright launch.")
    browser = playwright.firefox.launch(headless=False)  # launch(headless=False) for debugging
    page = browser.new_page()

    # Login to the kindergarten application
    start_url = environ["BASE_URL"] + environ["START_URL"]
    logger.info("Goto url: %s.", start_url)
    page.goto(start_url)
    logger.info("Input 'Nazwa uzytkownika': *** .")
    page.locator("xpath=//*[@id='Username']").fill(environ["USER_NAME"])
    logger.info("Input 'Haslo': *** .")
    page.locator("xpath=//*[@id='Password']").fill(environ["PASSWORD"])
    logger.info("Click 'Zaloguj sie' button.")
    page.locator("xpath=//*[@type='submit']").click()
    page.wait_for_load_state()

    sleep(5)  # Need to wait, but don't know what events need to waiting, so just use sleep 5 seconds
    cookies = page.context.cookies()
    logger.info("Cookies were obtained from the UI.")

    browser.close()
    logger.info("Browser has been closed.")
    return cookies
