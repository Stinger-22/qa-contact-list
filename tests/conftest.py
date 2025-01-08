import contextlib
import logging
import warnings

import pytest

from tests.api.contact.test_cases_contact import CONTACTS
from tests.api.test_cases_user import USERS_REGISTRATION, USERS_REGISTRATION_INVALID
from util.admin.admin_api import AdminAPI, AdminAPIException

LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse = True, scope = "session")
def admin():
    return AdminAPI()

@pytest.fixture(autouse = True, scope = "session")
def unique_credentials():
    _unique_credentials = set()
    user_test_cases = USERS_REGISTRATION + USERS_REGISTRATION_INVALID
    for user in user_test_cases:
        if "email" in user[0] and "password" in user[0]:
            credential = (user[0]["email"], user[0]["password"])
            _unique_credentials.add(credential)
    LOGGER.info("Set up set of unique credentials from User test cases")
    return _unique_credentials

@pytest.fixture(autouse = True, scope = "session")
def cleanup(admin: AdminAPI, unique_credentials: set):
    for credential in unique_credentials:
        with contextlib.suppress(AdminAPIException):
            token = admin.log_in(credential[0], credential[1])
            admin.delete_user(token)
    LOGGER.info("Performed data cleanup")

@pytest.fixture
def user_default() -> dict:
    return USERS_REGISTRATION[0][0]

@pytest.fixture
def contact_default() -> dict:
    return CONTACTS[0][0]

@pytest.fixture
def contact_list_default() -> dict:
    contact_list = []
    contact_list.append(CONTACTS[0][0])
    contact_list.append(CONTACTS[1][0])
    contact_list.append(CONTACTS[2][0])
    return contact_list

@pytest.fixture
def user_registered(admin: AdminAPI, user_default):
    token = admin.create_user(user_default)
    LOGGER.info("Created registered user")
    yield user_default
    try:
        admin.delete_user(token)
        LOGGER.info("Deleted registered user")
    except AdminAPIException as exception:
        LOGGER.warning("Registered user was not deleted from the first try")
        warnings.warn("Registered user was not deleted from the first try")
        LOGGER.warning("For some reason original token was invalidated. Couldn't delete user required for test from the first attempt")
        warnings.warn("For some reason original token was invalidated. Couldn't delete user required for test from the first attempt")
        LOGGER.info("Logging in to receive new token")
        token = admin.log_in(user_default["email"], user_default["password"])
        admin.delete_user(token)
        LOGGER.info("Registered user was deleted from the second try")