import logging

from src.util.admin.admin_api import AdminAPI
from tests.ui.pages import SignUpPage

LOGGER = logging.getLogger(__name__)


class TestUISignUp:
    def enter_sign_up_data(self, sign_up_page: SignUpPage, user: dict):
        sign_up_page.enter_first_name(user["firstName"])
        sign_up_page.enter_last_name(user["lastName"])
        sign_up_page.enter_email(user["email"])
        sign_up_page.enter_password(user["password"])

    def test_can_sign_up(self, admin: AdminAPI, sign_up_page: SignUpPage, user_default: dict) -> None:
        sign_up_page.open_page()
        self.enter_sign_up_data(sign_up_page, user_default)
        redirected_to = sign_up_page.click_sign_up()
        assert redirected_to.is_browser_url_changed("https://thinking-tester-contact-list.herokuapp.com/contactList")

        # Cleanup
        token = admin.log_in(user_default["email"], user_default["password"])
        admin.delete_user(token)

    def test_sign_up_used_mail(self, sign_up_page: SignUpPage, user_registered: dict) -> None:
        sign_up_page.open_page()
        self.enter_sign_up_data(sign_up_page, user_registered)
        redirected_to = sign_up_page.click_sign_up_expecting_failure()
        assert redirected_to.is_error_present_with_text("Email address is already in use")

    def test_sign_up_invalid_user(self, sign_up_page: SignUpPage, user_registered: dict) -> None:
        sign_up_page.open_page()
        sign_up_page.enter_email("john.green mail.com")
        sign_up_page.enter_password(1)
        redirected_to = sign_up_page.click_sign_up_expecting_failure()
        assert redirected_to.is_error_present_with_text("User validation failed")

    def test_button_cancel_sign_up_is_working(self, sign_up_page: SignUpPage) -> None:
        sign_up_page.open_page()
        redirected_to = sign_up_page.click_cancel()
        assert redirected_to.is_browser_url_changed("https://thinking-tester-contact-list.herokuapp.com/login")
