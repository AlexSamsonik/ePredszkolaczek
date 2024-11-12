"""There is main module to calculate actual the actual number of hours children are in kindergarten."""

import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from os import environ

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from src.collected_data_from_ui import run
from src.helpers import get_first_and_last_day_of_month, calculate_interval_hours

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", level=logging.INFO)


@dataclass
class ActualPresent:
    """Dataclass to storage actual presenting children in kindergarten."""

    num: str
    sur_name: str
    first_name: str
    unit: str
    day: str
    start_time: str
    end_time: str


def print_calculation(first_name: str, presenting: list[ActualPresent]) -> None:
    """Calculate and log the total days, meal payments, hours, and hour payments for a child in kindergarten.

    :param first_name: The first name of the child.
    :param presenting: A list of ActualPresent objects representing the child's attendance.
    """
    hours = sum([(calculate_interval_hours(i.start_time, i.end_time)) for i in presenting])

    logger.info(f"{first_name}. Days in kindergarten: '{len(presenting)}'.")
    logger.info(f"{first_name}. Payment for meals: '{len(presenting) * int(environ["PAYMENT_FOR_MEALS_FOR_DAY"])}' zl.")

    logger.info(f"{first_name}. Hours in kindergarten: '{hours}'.")
    logger.info(f"{first_name}. Payment for hours: '{hours * float(environ["PAYMENT_FOR_HOUR"])}' zl.")


def main(month: str):
    """The main function to execute script.

    :param month: Number of month from 1 to 12. If not specified, the current month is used.
    """
    load_dotenv()
    first_day, last_day = get_first_and_last_day_of_month(month)
    with sync_playwright() as playwright:
        presents = run(playwright, first_day, last_day)

    actual_presents: list[ActualPresent] = [ActualPresent(*presents[i : i + 7]) for i in range(0, len(presents), 7)]
    wa_present: list[ActualPresent] = [ap for ap in actual_presents if ap.first_name == environ["WA_FIRST_NAME"]]
    we_present: list[ActualPresent] = [ap for ap in actual_presents if ap.first_name == environ["WE_FIRST_NAME"]]

    print_calculation(environ["WA_FIRST_NAME"], wa_present)
    print_calculation(environ["WE_FIRST_NAME"], we_present)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-m",
        "--month",
        help="Number of month. Please input number from 1 to 12. If not specified, the current month is used.",
        required=False,
    )
    args = parser.parse_args()
    main(args.month)
