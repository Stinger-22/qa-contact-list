from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

LOGGER = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver, url: str) -> None:
        self.driver = driver
        if url is None:
            self.url = driver.current_url
        else:
            self.url = url

    def open_page(self) -> None:
        self.driver.get(self.url)
        LOGGER.info("Opened page")

    def enter_into_field(self, input_id: str, value: str) -> None:
        self.find_element_by_id(input_id).send_keys(value)
        LOGGER.info("Entered %s", input_id)

    def find_element_by_id(self, id: str) -> WebElement:
        return self.driver.find_element(By.ID, id)

    def is_element_displayed(self, element: WebElement) -> bool:
        try:
            WebDriverWait(element, 5).until(lambda element: element.is_displayed())
        except TimeoutException as exception:
            return False
        return True

    def is_browser_url_changed(self, new_url: str) -> bool:
        try:
            WebDriverWait(self.driver, 5).until(lambda driver: driver.current_url == new_url)
        except TimeoutException as exception:
            return False
        return True

    def is_error_present_with_text(self, error_msg: str) -> bool:
        error = self.find_element_by_id("error")
        return (error is not None) and (self.is_element_displayed(error)) and (error_msg in error.text)

class LogInPage(BasePage):
    def __init__(self, driver: WebDriver):
        url = "https://thinking-tester-contact-list.herokuapp.com/login"
        super().__init__(driver, url)
        LOGGER.info("Created POM: LogInPage")

    def enter_email(self, email: str):
        self.find_element_by_id("email").send_keys(email)
        LOGGER.info("Entered email")

    def enter_password(self, password: str):
        self.find_element_by_id("password").send_keys(password)
        LOGGER.info("Entered password")

    def click_submit_log_in(self) -> ContactListPage:
        self.find_element_by_id("submit").click()
        LOGGER.info("Clicked on Log In button")
        return ContactListPage(self.driver)

    def click_submit_log_in_expecting_failure(self) -> LogInPage:
        self.find_element_by_id("submit").click()
        LOGGER.info("Clicked on Log In button with invalid credentials")
        return self

    def click_sign_up(self) -> SignUpPage:
        self.find_element_by_id("signup").click()
        LOGGER.info("Clicked on Sign Up button")
        return SignUpPage(self.driver)

class SignUpPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        url = "https://thinking-tester-contact-list.herokuapp.com/addUser"
        super().__init__(driver, url)
        LOGGER.info("Created POM: SignUpPage")

    def enter_first_name(self, first_name: str) -> None:
        self.find_element_by_id("firstName").send_keys(first_name)
        LOGGER.info("Entered first name")

    def enter_last_name(self, last_name: str) -> None:
        self.find_element_by_id("lastName").send_keys(last_name)
        LOGGER.info("Entered last name")

    def enter_email(self, email: str) -> None:
        self.find_element_by_id("email").send_keys(email)
        LOGGER.info("Entered email")

    def enter_password(self, password: str) -> None:
        self.find_element_by_id("password").send_keys(password)
        LOGGER.info("Entered password")

    def click_sign_up(self) -> ContactListPage:
        self.find_element_by_id("submit").click()
        LOGGER.info("Clicked on Sign Up button")
        return ContactListPage(self.driver)

    def click_sign_up_expecting_failure(self) -> SignUpPage:
        self.find_element_by_id("submit").click()
        LOGGER.info("Clicked on Sign Up button with invalid credentials")
        return self

    def click_cancel(self) -> LogInPage:
        self.find_element_by_id("cancel").click()
        LOGGER.info("Clicked on Cancel button")
        return LogInPage(self.driver)

class ContactListPage(BasePage):
    def __init__(self, driver: WebDriver):
        url = "https://thinking-tester-contact-list.herokuapp.com/contactList"
        super().__init__(driver, url)
        LOGGER.info("Created POM: ContactListPage")

    def parse_contact_list_table(self) -> list:
        parsed_contacts = []
        table_xpath = "/html/body/div/div/table"
        table_rows_xpath = f"{table_xpath}/tr"
        number_of_rows = len(self.driver.find_elements(by = "xpath", value = table_rows_xpath)) + 1
        number_of_columns = len(self.driver.find_elements(by = "xpath", value = table_rows_xpath + "[1]/td")) + 1
        for row in range(1, number_of_rows):
            contact = []
            for col in range(2, number_of_columns):
                text = self.driver.find_element(by = "xpath", value = f"{table_xpath}/tr[{row}]/td[{col}]").text
                contact.append(text)
            parsed_contacts.append(contact)
        LOGGER.info("Parsed contacts table")
        return parsed_contacts

    def click_add_new_contact(self) -> AddContactPage:
        self.find_element_by_id("add-contact").click()
        LOGGER.info("Clicked on Add a New Contact button")
        return AddContactPage(self.driver)

    def click_log_out(self) -> LogInPage:
        self.find_element_by_id("logout").click()
        LOGGER.info("Clicked on Log Out button")
        return LogInPage(self.driver)

class AddContactPage(BasePage):
    def __init__(self, driver: WebDriver):
        url = "https://thinking-tester-contact-list.herokuapp.com/addContact"
        super().__init__(driver, url)
        LOGGER.info("Created POM: AddContactPage")

    def click_submit(self) -> ContactListPage:
        self.find_element_by_id("submit").click()
        LOGGER.info("Clicked on Submit button")
        return ContactListPage(self.driver)

    def click_submit_expecting_failure(self) -> AddContactPage:
        self.find_element_by_id("submit").click()
        LOGGER.info("Clicked on Submit button with invalid contact")
        return AddContactPage(self.driver)

    def click_cancel(self) -> LogInPage:
        self.find_element_by_id("cancel").click()
        LOGGER.info("Clicked on Cancel button")
        return ContactListPage(self.driver)

    def click_log_out(self) -> LogInPage:
        self.find_element_by_id("logout").click()
        LOGGER.info("Clicked on Log Out button")
        return LogInPage(self.driver)
