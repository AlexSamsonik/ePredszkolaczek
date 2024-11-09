"""There is main module to calculate actual the actual number of hours children are in kindergarten."""

from calendar import monthrange
from datetime import date
from os import environ

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Playwright


def run(playwright: Playwright, date_from: str, date_to: str):
    """Running Playwright and return list with all presented information for specify date range.

    :param playwright: Playwright instance.
    :param date_from: Start search date. Date format must be 'YYYY-MM-DD'.
    :param date_to: End search date. Date format must be 'YYYY-MM-DD'.
    :return:
    """
    browser = playwright.firefox.launch()
    page = browser.new_page()

    # Login to the kindergarten application
    page.goto(environ["URL"])
    page.locator("xpath=//*[@type='email']").fill(environ["EMAIL"])
    page.locator("xpath=//*[@type='password']").fill(environ["PASSWORD"])
    page.locator("xpath=//*[@type='submit']").click()
    page.wait_for_load_state()

    # Input search dates
    page.get_by_placeholder("Data od").fill(date_from)
    page.get_by_placeholder("Data do").fill(date_to)
    page.locator("xpath=//*[@type='submit']").click()
    page.wait_for_load_state()

    # Count page in table
    pagination = page.locator("xpath=//ul[@class='pagination']").text_content()
    pages_in_table = int(pagination.replace("»", "")[-1:])

    presents = []
    for i in range(pages_in_table):
        rows = page.locator("//table[@class='table table-bordered']/tbody/tr/td")
        for j in range(rows.count()):
            presents.append(rows.nth(j).text_content().strip())
        if i != pages_in_table - 1:
            page.locator("xpath=//li[@class='PagedList-skipToNext']/a[@rel='next']").click()
        page.wait_for_load_state()

    browser.close()
    return presents


def get_first_and_last_day_of_current_month() -> tuple:
    """Calculate the first and last day of the current month.

    :return: A tuple containing two strings, the first and last day of the current month in 'YYYY-MM-DD' format.
    """
    today = date.today()
    first_day = date(today.year, today.month, 1)
    last_day = date(today.year, today.month, monthrange(today.year, today.month)[1])
    return first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d")


def main():
    """The main function to execute script."""
    load_dotenv()
    first_day, last_day = get_first_and_last_day_of_current_month()
    with sync_playwright() as playwright:
        presents = run(playwright, first_day, last_day)
    print(presents)


if __name__ == "__main__":
    main()
