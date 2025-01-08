import logging

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from tests.ui.pages import ContactListPage, LogInPage, SignUpPage

LOGGER = logging.getLogger(__name__)


@pytest.fixture(params = ["Chrome", "Firefox"])
def driver(request):
    _driver = None
    if request.param == "Chrome":
        _driver = webdriver.Chrome()
    elif request.param == "Firefox":
        _driver = webdriver.Firefox()
    _driver.implicitly_wait(10)
    yield _driver
    _driver.quit()

@pytest.fixture
def log_in_page(driver: WebDriver) -> LogInPage:
    return LogInPage(driver)

@pytest.fixture
def sign_up_page(driver: WebDriver) -> SignUpPage:
    return SignUpPage(driver)

@pytest.fixture
def contact_list_page(log_in_page: LogInPage, user_registered: dict) -> ContactListPage:
    log_in_page.open_page()
    log_in_page.enter_email(user_registered["email"])
    log_in_page.enter_password(user_registered["password"])
    return log_in_page.click_submit_log_in()
