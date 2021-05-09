import argparse
import logging
import os
import sys
import traceback

from typing import Tuple

from freshdesk.freshdesk import FreshdeskContactRequest
from github.github import GithubUserRequest
from mapping.github_to_freshdesk_mapping import GithubUserToFreshdeskContact

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def main() -> None:
    setup_logging()

    logger = logging.getLogger('Main')

    if sys.version_info < (3, 0):
        logger.error("Use Python 3+ to run the script")

    try:
        username, subdomain = parse_args_from_command_line()
        github_token = os.environ['GITHUB_TOKEN']
        freshdesk_token = os.environ['FRESHDESK_TOKEN']

        logger.info(
            "Starting to migrate GitHub user {} to a Freshdesk contact in subdomain {}".format(username, subdomain))

        migrate_github_user_to_freshdesk_contact(freshdesk_token, github_token, username, subdomain)
    except Exception:
        logger.error("Something went wrong, see the traceback for more details")
        logger.error(traceback.format_exc())


def migrate_github_user_to_freshdesk_contact(freshdesk_token: str,
                                             github_token: str,
                                             username: str,
                                             subdomain: str) -> None:
    github_user_request = GithubUserRequest(token=github_token)
    github_user = github_user_request.get_github_user_by_username(username=username)

    freshdesk_contact = GithubUserToFreshdeskContact.apply(github_user)
    freshdesk_contact_request = FreshdeskContactRequest(subdomain=subdomain, token=freshdesk_token)
    freshdesk_contact_request.create_or_update_freshdesk_contact(freshdesk_contact=freshdesk_contact)


def setup_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    root.addHandler(handler)


def parse_args_from_command_line() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(description='Retrieves the information of a GitHub user and creates a new contact '
                                                 'or updates an existing contact in Freshdesk.')
    parser.add_argument('--username', type=str, action='store', help='the GitHub username', required=True)
    parser.add_argument('--subdomain', type=str, action='store', help='the Freshdesk subdomain', required=True)
    args = parser.parse_args()

    return args.username, args.subdomain


if __name__ == "__main__":
    main()
