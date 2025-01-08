import logging

import pytest
import requests

from util.admin.admin_api import AdminAPI, AdminAPIException
from util.admin.bearer_auth import BearerAuth

LOGGER = logging.getLogger(__name__)


class TestAPIUser:
    endpoint = "https://thinking-tester-contact-list.herokuapp.com/users/"
    myself = "me"
    login = "login"
    logout = "logout"

    def check_user_json_schema(self, user: dict) -> None:
        assert "_id" in user
        assert "firstName" in user
        assert "lastName" in user
        assert "email" in user
        assert "__v" in user
        LOGGER.info("User JSON schema is correct")

    def check_user_equals(self, user: dict, another: dict) -> None:
        assert user["firstName"] == another["firstName"]
        assert user["lastName"] == another["lastName"]
        assert user["email"] == another["email"]


    def test_create_user(self, admin: AdminAPI, user_raw_data: dict) -> None:
        LOGGER.debug("Creating user: %s", user_raw_data)
        response = requests.post(TestAPIUser.endpoint, json = user_raw_data)
        LOGGER.debug("Received response text: %s", response.text)
        assert response.status_code == 201
        assert "application/json" in response.headers["Content-Type"]
        LOGGER.info("Response status code and headers are correct")

        data = response.json()
        assert "user" in data
        self.check_user_json_schema(data["user"])
        self.check_user_equals(user_raw_data, data["user"])
        assert "token" in data
        LOGGER.info("Created user response JSON is correct")

        created_user = admin.get_user(data["token"])
        self.check_user_json_schema(created_user)
        self.check_user_equals(user_raw_data, created_user)
        LOGGER.info("Successfully received same registered user")

        # Cleanup
        admin.delete_user(data["token"])

    def test_create_user_invalid(self, admin: AdminAPI, user_raw_data_invalid: dict) -> None:
        LOGGER.debug("Creating invalid user: %s", user_raw_data_invalid)
        response = requests.post(TestAPIUser.endpoint, json = user_raw_data_invalid)
        LOGGER.debug("Received response text: %s", response.text)
        try:
            assert response.status_code == 400
            LOGGER.info("Invalid user was not created")
        except AssertionError as error:
            # Cleanup
            admin.delete_user(response.json()["token"])
            exception_msg = "Invalid user was created"
            raise AssertionError(exception_msg) from error


    def test_get_user_myself(self, user_registered: dict, token: str) -> None:
        LOGGER.debug("Getting user %s with token %s", user_registered, token)
        response = requests.get(TestAPIUser.endpoint + TestAPIUser.myself, auth = BearerAuth(token))
        LOGGER.debug("Received response text: %s", response.text)
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        LOGGER.info("Response status code and headers are correct")

        received_user = response.json()
        self.check_user_json_schema(received_user)
        self.check_user_equals(user_registered, received_user)
        LOGGER.info("Successfully received user")

    def test_get_user_myself_without_auth(self, user_registered: dict) -> None:
        LOGGER.debug("Getting user: %s", user_registered)
        response = requests.get(TestAPIUser.endpoint + TestAPIUser.myself)
        LOGGER.debug("Received response text: %s", response.text)
        assert response.status_code == 401
        LOGGER.info("Can't get user without authorization as it is intended")


    def test_patch_user(self, admin: AdminAPI, token: str, user_updated_raw_data: dict) -> None:
        LOGGER.debug("Updating user with %s", user_updated_raw_data[0])
        response = requests.patch(TestAPIUser.endpoint + TestAPIUser.myself, auth = BearerAuth(token), json = user_updated_raw_data[0])
        LOGGER.debug("Received response text: %s", response.text)
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        LOGGER.info("Response status code and headers are correct")

        data = response.json()
        self.check_user_json_schema(data)
        self.check_user_equals(user_updated_raw_data[1], data)
        LOGGER.info("Response with updated user JSON is correct")

        updated_user = admin.get_user(token)
        self.check_user_json_schema(updated_user)
        self.check_user_equals(user_updated_raw_data[1], updated_user)
        LOGGER.info("Successfully received user with updated fields")

    def test_patch_user_invalid(self, admin: AdminAPI, user_registered: dict, token: str, user_updated_raw_data_invalid: dict) -> None:
        LOGGER.debug("Updating user with %s", user_updated_raw_data_invalid)
        response = requests.patch(TestAPIUser.endpoint + TestAPIUser.myself, auth = BearerAuth(token), json = user_updated_raw_data_invalid)
        LOGGER.debug("Received response text: %s", response.text)
        assert response.status_code == 400
        LOGGER.info("Can't update user fields to invalid ones as it is intended")

        updated_user = admin.get_user(token)
        self.check_user_json_schema(updated_user)
        self.check_user_equals(user_registered, updated_user)
        LOGGER.info("User fields was not updated to invalid ones")


    def test_delete_user(self, admin: AdminAPI, user_default: dict) -> None:
        # Setup
        token = admin.create_user(user_default)

        LOGGER.debug("Deleting user: %s", user_default)
        response = requests.delete(TestAPIUser.endpoint + TestAPIUser.myself, auth = BearerAuth(token))
        LOGGER.debug("Received response text: %s", response.text)
        assert response.status_code == 200
        LOGGER.info("Deleted existing user")

        with pytest.raises(AdminAPIException):
            admin.get_user(token)
        LOGGER.info("Can't receive user that was deleted")
        with pytest.raises(AdminAPIException):
            admin.log_in(user_default["email"], user_default["password"])
        LOGGER.info("Can't log in user that was deleted")


    def test_log_in_user(self, admin: AdminAPI, user_registered: dict) -> None:
        log_in_data = {
            "email": user_registered["email"],
            "password": user_registered["password"],
        }
        response = requests.post(TestAPIUser.endpoint + TestAPIUser.login, json = log_in_data)
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        LOGGER.info("Response status code and headers are correct")

        data = response.json()
        assert "user" in data
        self.check_user_json_schema(data["user"])
        self.check_user_equals(user_registered, data["user"])
        assert "token" in data
        LOGGER.info("Successfully logged in to intended user account and received token")

        logged_in_user = admin.get_user(data["token"])
        self.check_user_json_schema(logged_in_user)
        self.check_user_equals(user_registered, logged_in_user)
        LOGGER.info("Can use received token and use it to get user")

    def test_log_out_user(self, admin: AdminAPI, user_registered: dict) -> None:
        # Setup
        token = admin.log_in(user_registered["email"], user_registered["password"])

        response = requests.post(TestAPIUser.endpoint + TestAPIUser.logout, auth = BearerAuth(token))
        assert response.status_code == 200
        LOGGER.info("Logged out from user account")

        with pytest.raises(AdminAPIException):
            admin.get_user(token)
        LOGGER.info("Can't use the same token after logging out with it")
