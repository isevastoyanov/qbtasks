import json
import logging

import requests

from freshdesk.freshdesk_contact import FreshdeskContact

FRESHDESK_CREATE_CONTACT_API_URL = "https://{}.freshdesk.com/api/v2/contacts"
FRESHDESK_UPDATE_CONTACT_API_URL = FRESHDESK_CREATE_CONTACT_API_URL + "/{}"
HEADERS = {"Content-Type": "application/json"}
PASSWORD = "x"


class FreshdeskContactRequest:
    """"The purpose of this class is to facilitate the work with the FreshDesk Contacts REST API. All CRUD operations
    over Freshdesk contacts should be here."""

    def __init__(self, subdomain: str, token: str):
        self.__logger = logging.getLogger('freshdesk.FreshdeskContactRequest')
        self.__subdomain = subdomain
        self.__token = token

    def create_or_update_freshdesk_contact(self, freshdesk_contact: FreshdeskContact) -> None:
        """"Creates a contact if it does not already exist, otherwise updates the contact."""

        self.__logger.info("Creating Freshdesk contact {}...".format(freshdesk_contact.name))

        response = requests.post(FRESHDESK_CREATE_CONTACT_API_URL.format(self.__subdomain),
                                 auth=(self.__token, PASSWORD),
                                 data=json.dumps(freshdesk_contact.__dict__),
                                 headers=HEADERS)

        if response.status_code == requests.status_codes.codes['CREATED']:
            self.__logger.info("Contact created successfully")
        elif response.status_code == requests.status_codes.codes['CONFLICT']:
            self.__logger.info("Contact already exists, trying to update")

            json_data = json.loads(response.content)
            contact_id = json_data["errors"][0]["additional_info"]["user_id"]
            self.__update_freshdesk_contact(contact_id=contact_id, freshdesk_contact=freshdesk_contact)
        else:
            json_data = json.loads(response.content)

            raise RuntimeError("Failed to create contact - {}".format(json_data["errors"]))

    def __update_freshdesk_contact(self, contact_id: int, freshdesk_contact: FreshdeskContact) -> None:
        self.__logger.info("Updating contact info for contact ID {}".format(contact_id))

        response = requests.put(FRESHDESK_UPDATE_CONTACT_API_URL.format(self.__subdomain, contact_id),
                                auth=(self.__token, PASSWORD),
                                data=json.dumps(freshdesk_contact.__dict__),
                                headers=HEADERS)
        if response.status_code == requests.status_codes.codes['OK']:
            self.__logger.info("Contact updated successfully")
        else:
            json_data = json.loads(response.content)

            raise RuntimeError("Failed to update contact - {}".format(json_data["errors"]))
