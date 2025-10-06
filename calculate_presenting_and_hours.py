"""There is main module to calculate actual the actual number of hours children are in kindergarten."""

from argparse import ArgumentParser
from os import environ

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from src.collected_data_from_ui import run
from src.helpers import print_calculation


def main(month: str, year: str):
    """The main function to execute script.

    :param month: Number of month from 1 to 12. If not specified, the current month is used.
    :param year: The year for which the calculation is to be made. If not specified, the current year is used.
    """
    load_dotenv()
    with sync_playwright() as playwright:
        presents = run(playwright, month, year)

    print_calculation(environ["WA_FIRST_NAME"], presents[environ["WA_ID"]])
    print_calculation(environ["WE_FIRST_NAME"], presents[environ["WE_ID"]])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-m",
        "--month",
        help="Number of month. Please input number from 1 to 12. If not specified, the current month is used.",
        required=False,
    )
    parser.add_argument(
        "-y",
        "--year",
        help="The year for which the calculation is to be made. If not specified, the current year is used.",
        required=False,
    )
    args = parser.parse_args()
    main(args.month, args.year)
