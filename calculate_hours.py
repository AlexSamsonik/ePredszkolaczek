"""There is main module to calculate actual the actual number of hours children are in kindergarten."""

import logging
from calendar import monthrange
from datetime import date
from os import environ

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Playwright

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
    logger.info(f"Goto url: {environ["URL"]}.")
    page.goto(environ["URL"])
    logger.info("Input email: *** .")
    page.locator("xpath=//*[@type='email']").fill(environ["EMAIL"])
    logger.info("Input password: *** .")
    page.locator("xpath=//*[@type='password']").fill(environ["PASSWORD"])
    logger.info("Click 'Submit' button.")
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
    pages_in_table = int(pagination.replace("»", "")[-1:])
    logger.info(f"Found '{pages_in_table}' pages in 'Obecności' table.")

    presents = []
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


def get_first_and_last_day_of_month(month: str | int | None = None):
    """Calculate the first and last day of the specified month or the current month if no month is specified.

    :param month: Optional; an integer (1-12) or a string representing the month. If not specified, the current month is used.
    :return: A tuple containing two strings, the first and last day of the specified or current month in 'YYYY-MM-DD' format.
    """
    today = date.today()
    year = today.year

    if not month:
        month = today.month
    elif isinstance(month, str):
        try:
            month = int(month)
        except ValueError:
            raise ValueError("Month must be a number between 1 and 12")

    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12")

    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    return first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d")


def main():
    """The main function to execute script."""
    load_dotenv()
    first_day, last_day = get_first_and_last_day_of_month()
    with sync_playwright() as playwright:
        presents = run(playwright, first_day, last_day)
    print(presents)


if __name__ == "__main__":
    main()
