import json
import unittest

import requests
import responses

from freshdesk.freshdesk import FRESHDESK_CREATE_CONTACT_API_URL, HEADERS, FRESHDESK_UPDATE_CONTACT_API_URL
from github.github import GITHUB_USERS_API_URL, AUTHORIZATION_HEADER_NAME, AUTHORIZATION_HEADER_VALUE_TOKEN, \
    ACCEPT_HEADER_NAME, ACCEPT_HEADER_VALUE_JSON, as_github_user
from main import migrate_github_user_to_freshdesk_contact
from mapping.github_to_freshdesk_mapping import GithubUserToFreshdeskContact

CONTACT_ID = 123456

username = "Username"
subdomain = "freshdesk_subdomain"
github_token = 'github_token'
json_data = {'name': "Test Name",
             'location': 'Sofia',
             'email': 'test@test.com',
             'bio': 'some bio',
             'twitter_username': 'twitter'}
github_user = as_github_user(json_data)
freshdesk_contact = GithubUserToFreshdeskContact.apply(github_user)


def request_callback_for_created(request):
    resp_body = {}
    headers = HEADERS
    return requests.status_codes.codes['CREATED'], headers, json.dumps(resp_body)


def request_callback_for_conflict(request):
    resp_body = {'errors': [{'additional_info': {'user_id': CONTACT_ID}}]}
    headers = HEADERS
    return requests.status_codes.codes['CONFLICT'], headers, json.dumps(resp_body)


def request_callback_for_update(request):
    resp_body = {}
    headers = HEADERS
    return requests.status_codes.codes['OK'], headers, json.dumps(resp_body)


class TestGithubToFreshdeskMapper(unittest.TestCase):

    @responses.activate
    def test_request_successfully_created(self):
        responses.add(responses.GET,
                      GITHUB_USERS_API_URL + username,
                      json=json_data,
                      status=requests.status_codes.codes['OK'],
                      headers={AUTHORIZATION_HEADER_NAME: AUTHORIZATION_HEADER_VALUE_TOKEN.format(github_token),
                               ACCEPT_HEADER_NAME: ACCEPT_HEADER_VALUE_JSON})

        responses.add_callback(
            responses.POST,
            FRESHDESK_CREATE_CONTACT_API_URL.format(subdomain),
            callback=request_callback_for_created
        )

        migrate_github_user_to_freshdesk_contact('freshdesk_token', github_token, username, subdomain)

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.url, GITHUB_USERS_API_URL + username)
        self.assertEqual(responses.calls[0].response.text, json.dumps(json_data))
        self.assertEqual(responses.calls[0].response.status_code, requests.status_codes.codes['OK'])
        self.assertEqual(responses.calls[0].response.headers[AUTHORIZATION_HEADER_NAME],
                         AUTHORIZATION_HEADER_VALUE_TOKEN.format(github_token))
        self.assertEqual(responses.calls[0].response.headers[ACCEPT_HEADER_NAME],
                         ACCEPT_HEADER_VALUE_JSON)
        self.assertEqual(responses.calls[1].request.url, FRESHDESK_CREATE_CONTACT_API_URL.format(subdomain))
        self.assertEqual(responses.calls[1].request.body, json.dumps(freshdesk_contact.__dict__))
        self.assertEqual(responses.calls[1].response.status_code, requests.status_codes.codes['CREATED'])

    @responses.activate
    def test_request_successfully_updated(self):
        responses.add(responses.GET,
                      GITHUB_USERS_API_URL + username,
                      json=json_data,
                      status=requests.status_codes.codes['OK'],
                      headers={AUTHORIZATION_HEADER_NAME: AUTHORIZATION_HEADER_VALUE_TOKEN.format(github_token),
                               ACCEPT_HEADER_NAME: ACCEPT_HEADER_VALUE_JSON})

        responses.add_callback(
            responses.POST,
            FRESHDESK_CREATE_CONTACT_API_URL.format(subdomain),
            callback=request_callback_for_conflict
        )

        responses.add_callback(
            responses.PUT,
            FRESHDESK_UPDATE_CONTACT_API_URL.format(subdomain, CONTACT_ID),
            callback=request_callback_for_update
        )

        migrate_github_user_to_freshdesk_contact('freshdesk_token', github_token, username, subdomain)

        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(responses.calls[0].request.url, GITHUB_USERS_API_URL + username)
        self.assertEqual(responses.calls[0].response.text, json.dumps(json_data))
        self.assertEqual(responses.calls[0].response.status_code, requests.status_codes.codes['OK'])
        self.assertEqual(responses.calls[0].response.headers[AUTHORIZATION_HEADER_NAME],
                         AUTHORIZATION_HEADER_VALUE_TOKEN.format(github_token))
        self.assertEqual(responses.calls[0].response.headers[ACCEPT_HEADER_NAME],
                         ACCEPT_HEADER_VALUE_JSON)
        self.assertEqual(responses.calls[1].request.url, FRESHDESK_CREATE_CONTACT_API_URL.format(subdomain))
        self.assertEqual(responses.calls[1].response.status_code, requests.status_codes.codes['CONFLICT'])
        self.assertEqual(responses.calls[1].request.body, json.dumps(freshdesk_contact.__dict__))
        self.assertEqual(responses.calls[2].request.url, FRESHDESK_UPDATE_CONTACT_API_URL.format(subdomain, CONTACT_ID))
        self.assertEqual(responses.calls[2].response.status_code, requests.status_codes.codes['OK'])
        self.assertEqual(responses.calls[2].request.body, json.dumps(freshdesk_contact.__dict__))


if __name__ == '__main__':
    unittest.main()
