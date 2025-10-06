"""There is module to provide functions to collecting data from UI."""

import logging
from os import environ
from time import sleep
from playwright.sync_api import Playwright

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", level=logging.INFO)

children_ids = [environ["WA_ID"], environ["WE_ID"]]


def select_element(locator, option, page) -> None:
    """Select option in selector and waiting couple of seconds.

    :param locator: Locator for selector element.
    :param option: Option for selector.
    :param page: Page object.
    :return: None
    """
    page.locator(locator).select_option(option)
    sleep(int(environ["WAITING_AFTER_SELECT"]))  # page.wait_for_load_state() is to fast, need to waiting 3 seconds.


def run(playwright: Playwright, month: str, year: str) -> dict:
    """Running Playwright and return list with all presented information for specify date range.

    :param playwright: Playwright instance.
    :param month: Number of month from 1 to 12. If not specified, the current month is used.
    :param year: The year for which the calculation is to be made. If not specified, the current year is used.

    :return: Dictionary with list of dictionary with start_time and end_time.
    """
    logger.info("Playwright launch.")
    browser = playwright.firefox.launch()  # launch(headless=False) for debugging
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

    logger.info("Open 'Obecnosci' page.")
    page.locator("xpath=//*[@id='btn_3']/button").click()

    presents = {}
    logger.info("Start collect information about actual presenting children in kindergarten.")
    for child_id in children_ids:
        presents.update({child_id: []})

        logger.info("Wybierz dziecko.")
        select_element(locator="xpath=//*[@id='MasterComboDziecko']", option=child_id, page=page)

        logger.info("Wybierz Miesiac.")
        select_element(locator="xpath=//*[@id='comboMiesiac']", option=month, page=page)

        logger.info("Wybierz Rok.")
        select_element(locator="xpath=//*[@id='comboRok']", option=year, page=page)

        rows = page.locator("xpath=//*[@id='table_obecnosci']/tbody/tr/td")
        for j in range(rows.count()):
            logger.info("%s. Collecting...", j + 1)
            if len(rows.nth(j).text_content()) in [11, 12]:
                start_time = rows.nth(j).locator("xpath=/div[@class='overlay']/div[@class='wejscie']").text_content()
                end_time = rows.nth(j).locator("xpath=/div[@class='overlay']/div[@class='wyjscie']").text_content()
                presents[child_id].append({"start_time": start_time, "end_time": end_time})

    browser.close()
    return presents
