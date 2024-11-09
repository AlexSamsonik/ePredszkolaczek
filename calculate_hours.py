"""There is main module to calculate actual the actual number of hours children are in kindergarten."""

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


if __name__ == "__main__":
    load_dotenv()
    with sync_playwright() as playwright:
        presents = run(playwright, "2024-10-01", "2024-10-30")
    print(presents)
