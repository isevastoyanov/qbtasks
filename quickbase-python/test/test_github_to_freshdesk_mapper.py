import unittest

from github.github_user import GithubUser
from mapping.github_to_freshdesk_mapping import GithubUserToFreshdeskContact


class TestGithubToFreshdeskMapper(unittest.TestCase):

    def test_happy_scenario(self):
        github_user = GithubUser("Username", "Sofia", "some_email@abv.bg", "Biography", "Twitter Account")

        freshdesk_contact = GithubUserToFreshdeskContact.apply(github_user)

        self.assertEqual(freshdesk_contact.name, github_user.name)
        self.assertEqual(freshdesk_contact.address, github_user.location)
        self.assertEqual(freshdesk_contact.email, github_user.email)
        self.assertEqual(freshdesk_contact.description, github_user.bio)
        self.assertEqual(freshdesk_contact.twitter_id, github_user.twitter_username)

    def test_all_empty_data(self):
        github_user = GithubUser(None, None, None, None, None)

        freshdesk_contact = GithubUserToFreshdeskContact.apply(github_user)

        self.assertEqual(freshdesk_contact.name, github_user.name)
        self.assertEqual(freshdesk_contact.address, github_user.location)
        self.assertEqual(freshdesk_contact.email, github_user.email)
        self.assertEqual(freshdesk_contact.description, github_user.bio)
        self.assertEqual(freshdesk_contact.twitter_id, github_user.twitter_username)

    def test_some_empty_data(self):
        github_user = GithubUser("Username", None, None, None, None)

        freshdesk_contact = GithubUserToFreshdeskContact.apply(github_user)

        self.assertEqual(freshdesk_contact.name, github_user.name)
        self.assertEqual(freshdesk_contact.address, github_user.location)
        self.assertEqual(freshdesk_contact.email, github_user.email)
        self.assertEqual(freshdesk_contact.description, github_user.bio)
        self.assertEqual(freshdesk_contact.twitter_id, github_user.twitter_username)


if __name__ == '__main__':
    unittest.main()
