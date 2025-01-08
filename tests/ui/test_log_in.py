import logging

from tests.ui.pages import LogInPage

LOGGER = logging.getLogger(__name__)


class TestUILogIn:
    def test_can_log_in(self, log_in_page: LogInPage, user_registered: dict) -> None:
        log_in_page.open_page()
        log_in_page.enter_email(user_registered["email"])
        log_in_page.enter_password(user_registered["password"])
        redirected_to = log_in_page.click_submit_log_in()
        assert redirected_to.is_browser_url_changed("https://thinking-tester-contact-list.herokuapp.com/contactList")

    def test_log_in_non_existent_user(self, log_in_page: LogInPage, user_default: dict) -> None:
        log_in_page.open_page()
        log_in_page.enter_email(user_default["email"])
        log_in_page.enter_password(user_default["password"])
        redirected_to = log_in_page.click_submit_log_in_expecting_failure()
        assert redirected_to.is_error_present_with_text("Incorrect username or password")

    def test_button_sign_up_is_working(self, log_in_page: LogInPage) -> None:
        log_in_page.open_page()
        redirected_to = log_in_page.click_sign_up()
        assert redirected_to.is_browser_url_changed("https://thinking-tester-contact-list.herokuapp.com/addUser")
