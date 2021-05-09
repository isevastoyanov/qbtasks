import json
import logging

import requests

from .github_user import GithubUser

GITHUB_USERS_API_URL = "https://api.github.com/users/"
ACCEPT_HEADER_NAME = "Accept"
ACCEPT_HEADER_VALUE_JSON = "application/vnd.github.v3+json"
AUTHORIZATION_HEADER_NAME = 'Authorization'
AUTHORIZATION_HEADER_VALUE_TOKEN = 'token {}'


def as_github_user(github_user_json: dict) -> GithubUser:
    """"Creates a GithubUser from a dictionary."""
    return GithubUser(github_user_json['name'],
                      github_user_json['location'],
                      github_user_json['email'],
                      github_user_json['bio'],
                      github_user_json['twitter_username'])


class GithubUserRequest:
    """"The purpose of this class is to facilitate the work with the GitHub REST API. All CRUD operations
        over GitHub users should be here."""

    def __init__(self, token: str):
        self.__logger = logging.getLogger('github.GithubUserRequest')
        self.__headers = {AUTHORIZATION_HEADER_NAME: AUTHORIZATION_HEADER_VALUE_TOKEN.format(token),
                          ACCEPT_HEADER_NAME: ACCEPT_HEADER_VALUE_JSON}

    def get_github_user_by_username(self, username: str) -> GithubUser:
        """Retrieves a GitHub user by its username."""

        self.__logger.info("Retrieving data for GitHub user {}...".format(username))

        response = requests.get(GITHUB_USERS_API_URL + username, headers=self.__headers)

        if response.status_code == requests.status_codes.codes['OK']:
            json_data = json.loads(response.content)
            self.__logger.info("GitHub user info received successfully")

            return as_github_user(github_user_json=json_data)
        elif response.status_code == requests.status_codes.codes['NOT_FOUND']:
            raise RuntimeError('User {} not found'.format(username))
        else:
            json_data = json.loads(response.content)

            raise RuntimeError("Failed to get GitHub user data - {}".format(json_data["errors"]))
