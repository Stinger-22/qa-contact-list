import logging

import pytest

from tests.api.test_cases_user import USERS_REGISTRATION
from util.admin.admin_api import AdminAPI, AdminAPIException

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def token(admin: AdminAPI, user_registered: dict) -> str:
    return admin.log_in(user_registered["email"], user_registered["password"])
