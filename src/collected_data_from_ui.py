"""There is module to provide functions to collecting data from UI."""

import logging
from os import environ

from playwright.sync_api import Playwright

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", level=logging.INFO)


def run(playwright: Playwright, date_from: str, date_to: str):
    """Running Playwright and return list with all presented information for specify date range.

    :param playwright: Playwright instance.
    :param date_from: Start search date. Date format must be 'YYYY-MM-DD'.
    :param date_to: End search date. Date format must be 'YYYY-MM-DD'.
    :return:
    """
    logger.info("Playwright launch.")
    browser = playwright.firefox.launch()
    page = browser.new_page()

    # Login to the kindergarten application
    logger.info(f"Goto url: {environ['URL']}.")
    page.goto(environ["URL"])
    logger.info("Input 'Nazwa uzytkownika': *** .")
    page.locator("xpath=//*[@id='Username']").fill(environ["USER_NAME"])
    logger.info("Input 'Haslo': *** .")
    page.locator("xpath=//*[@id='Password']").fill(environ["PASSWORD"])
    logger.info("Click 'Zaloguj sie' button.")
    page.locator("xpath=//*[@type='submit']").click()
    page.wait_for_load_state()

    # Input search dates
    logger.info(f"Input 'Data od' equals '{date_from}'.")
    page.get_by_placeholder("Data od").fill(date_from)
    logger.info(f"Input 'Data do' equals '{date_to}'.")
    page.get_by_placeholder("Data do").fill(date_to)
    logger.info("Click 'Szukaj' button.")
    page.locator("xpath=//*[@type='submit']").click()
    page.wait_for_load_state()

    # Count page in table
    pagination = page.locator("xpath=//ul[@class='pagination']").text_content()
    try:
        pages_in_table = int(pagination.replace("»", "")[-1:])
        logger.info(f"Found '{pages_in_table}' pages in 'Obecności' table.")
    except ValueError:
        pages_in_table = 0
        logger.info(f"Found '{pages_in_table}' pages in 'Obecności' table.")

    presents = []
    if pages_in_table:
        logger.info("Start collect information about actual presenting children in kindergarten.")
        for i in range(pages_in_table):
            rows = page.locator("//table[@class='table table-bordered']/tbody/tr/td")
            for j in range(rows.count()):
                presents.append(rows.nth(j).text_content().strip())
            if i != pages_in_table - 1:
                logger.info("Click '»' button.")
                page.locator("xpath=//li[@class='PagedList-skipToNext']/a[@rel='next']").click()
            page.wait_for_load_state()

    browser.close()
    return presents
