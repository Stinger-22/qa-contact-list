import pytest

from tests.api.test_cases_user import (
    USERS_PATCHED,
    USERS_PATCHED_INVALID,
    USERS_REGISTRATION,
    USERS_REGISTRATION_INVALID,
)
from tests.util.test_case_parse import get_test_case_id_payload_expected_id, get_test_case_id_payload_id


@pytest.fixture(params = USERS_REGISTRATION, ids = get_test_case_id_payload_id)
def user_raw_data(request) -> dict:
    return request.param[0]

@pytest.fixture(params = USERS_REGISTRATION_INVALID, ids = get_test_case_id_payload_id)
def user_raw_data_invalid(request) -> dict:
    return request.param[0]

@pytest.fixture(params = USERS_PATCHED, ids = get_test_case_id_payload_expected_id)
def user_updated_raw_data(request) -> dict:
    return (request.param[0], request.param[1])

@pytest.fixture(params = USERS_PATCHED_INVALID, ids = get_test_case_id_payload_id)
def user_updated_raw_data_invalid(request) -> dict:
    return request.param[0]
