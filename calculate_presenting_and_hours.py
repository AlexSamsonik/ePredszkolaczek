"""There is main module to calculate actual the actual number of hours children are in kindergarten."""

from argparse import ArgumentParser
from os import environ

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from src.collected_data_from_api import get_obecnosci
from src.collected_data_from_ui import run
from src.helpers import print_calculation, compose_string_from_dict_list, extract_entrance_exit_times

load_dotenv()


def main(month: str, year: str):
    """The main function to execute script.

    :param month: Number of month from 1 to 12. If not specified, the current month is used.
    :param year: The year for which the calculation is to be made. If not specified, the current year is used.
    """
    with sync_playwright() as playwright:
        cookies = run(playwright, headless=bool(int(environ["HEADLESS_MODE"])))

    # Getting cookies for API request
    cookies_for_request = compose_string_from_dict_list(
        dict_list=cookies,
        field_order=["ADFSClientFedUtilCookie", "ADFSClientFedUtilCookie1", "__Host-ASP.NET_SessionId_Intendent"],
    )
    children = [
        {"id": environ["WA_ID"], "first_name": environ["WA_FIRST_NAME"]},
        {"id": environ["WE_ID"], "first_name": environ["WE_FIRST_NAME"]},
    ]
    for child in children:
        obecnosci = get_obecnosci(child_id=child["id"], month=month, year=year, cookies=cookies_for_request)
        presenting = extract_entrance_exit_times(attendance_data=obecnosci)
        print_calculation(first_name=child["first_name"], presenting=presenting)


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
