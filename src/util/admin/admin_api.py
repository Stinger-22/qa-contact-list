import logging

import requests

from util.admin.bearer_auth import BearerAuth

LOGGER = logging.getLogger(__name__)


class AdminAPIException(Exception):
    """Raised for any kind of wrong behaviour in AdminAPI."""


class AdminAPI:
    """Wrapper for safe use of Contact List Application API.

    Attributes:
        url (str):       Contact List Application base url.

    """

    url = "https://thinking-tester-contact-list.herokuapp.com/"

    def __init__(self):
        LOGGER.info("Created AdminAPI")

    def _is_token_none(self, token: str) -> None:
        if token is None:
            exception_msg = "Received token is None"
            raise TypeError(exception_msg)

    def create_user(self, user: dict) -> str:
        LOGGER.debug("Creating user: %s", user)
        response = requests.post(AdminAPI.url + "users", json = user)
        if response.status_code != 201:
            exception_msg = f"Couldn't create user: {response.text}"
            raise AdminAPIException(exception_msg)
        token = response.json()["token"]
        LOGGER.debug("Created user and received token: %s", token)
        return token

    def log_in(self, email: str, password: str) -> str:
        LOGGER.debug("Logging in user with credentials: {email: %s, password: %s}", email, password)
        login_data = {
            "email": email,
            "password": password,
        }
        response = requests.post(AdminAPI.url + "users/login", json = login_data)
        if response.status_code != 200:
            exception_msg = f"Couldn't log in: {response.text}"
            raise AdminAPIException(exception_msg)
        token = response.json()["token"]
        LOGGER.debug("Logged in and received token: %s", token)
        return token

    def log_out(self, token: str) -> None:
        LOGGER.debug("Logging out with token: %s", token)
        self._is_token_none(token)
        response = requests.post(AdminAPI.url + "users/logout", auth = BearerAuth(token))
        if response.status_code != 200:
            exception_msg = f"Couldn't log out: {response.text}"
            raise AdminAPIException(exception_msg)
        LOGGER.debug("Logged out")

    def get_user(self, token: str) -> dict:
        LOGGER.debug("Getting user with token: %s", token)
        self._is_token_none(token)
        response = requests.get(AdminAPI.url + "users/me", auth = BearerAuth(token))
        if response.status_code != 200:
            exception_msg = f"Couldn't get user: {response.text}"
            raise AdminAPIException(exception_msg)
        user = response.json()
        LOGGER.debug("Received user: %s", user)
        return user

    def delete_user(self, token: str) -> None:
        LOGGER.debug("Deleting user with token: %s", token)
        self._is_token_none(token)
        response = requests.delete(AdminAPI.url + "users/me", auth = BearerAuth(token))
        if response.status_code != 200:
            exception_msg = f"Couldn't delete user: {response.text}"
            raise AdminAPIException(exception_msg)
        LOGGER.debug("User deleted")

    def create_contact(self, token: str, contact: dict) -> dict:
        LOGGER.debug("Using token: %s. Creating contact: %s", token, contact)
        self._is_token_none(token)
        response = requests.post(AdminAPI.url + "contacts", auth = BearerAuth(token), json = contact)
        if response.status_code != 201:
            exception_msg = f"Couldn't create contact: {response.text}"
            raise AdminAPIException(exception_msg)
        created_contact = response.json()
        LOGGER.debug("Contact created: %s", created_contact)
        return created_contact

    def get_contact(self, token: str, contact_id: str) -> dict:
        LOGGER.debug("Getting contact with id: %s using token: %s", contact_id, token)
        self._is_token_none(token)
        response = requests.get(AdminAPI.url + f"contacts/{contact_id}", auth = BearerAuth(token))
        if response.status_code != 200:
            exception_msg = f"Couldn't get contact: {response.text}"
            raise AdminAPIException(exception_msg)
        contact = response.json()
        LOGGER.debug("Received contact: %s", contact)
        return contact

    def delete_contact(self, token: str, contact_id: str) -> None:
        LOGGER.debug("Deleting contact with id: %s using token: %s", contact_id, token)
        self._is_token_none(token)
        response = requests.delete(AdminAPI.url + f"contacts/{contact_id}", auth = BearerAuth(token))
        if response.status_code != 200:
            exception_msg = f"Couldn't delete contact: {response.text}"
            raise AdminAPIException(exception_msg)
        LOGGER.debug("Contact deleted")

    def get_contact_list(self, token: str) -> list:
        LOGGER.debug("Getting contact list using token: %s", token)
        self._is_token_none(token)
        response = requests.get(AdminAPI.url + "contacts", auth = BearerAuth(token))
        if response.status_code != 200:
            exception_msg = f"Couldn't get contact list: {response.text}"
            raise AdminAPIException(exception_msg)
        contact_list = response.json()
        LOGGER.debug("Received contact list: %s", contact_list)
        return contact_list

    def delete_contact_list(self, token: str) -> None:
        LOGGER.debug("Deleting contact list using token: %s", token)
        self._is_token_none(token)
        response = requests.delete(AdminAPI.url + "contacts", auth = BearerAuth(token))
        if response.status_code != 200:
            exception_msg = f"Couldn't delete contacts: {response.text}"
            raise AdminAPIException(exception_msg)
        LOGGER.debug("Contact list deleted")
