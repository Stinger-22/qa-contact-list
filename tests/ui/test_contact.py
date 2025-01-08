import logging

from tests.ui.pages import ContactListPage

LOGGER = logging.getLogger(__name__)


class TestUIContact:
    contact_data_schema = (
        "firstName",
        "lastName",
        "birthdate",
        "email",
        "phone",
        "street1",
        "street2",
        "city",
        "stateProvince",
        "postalCode",
        "country",
    )

    contact_table_schema = (
        "firstName + lastName",
        "birthdate",
        "email",
        "phone",
        "street1 + street2",
        "city + stateProvince + postalCode",
        "country",
    )

    def test_add_contact(self, contact_list_page: ContactListPage, contact_default: dict):
        add_contact_page = contact_list_page.click_add_new_contact()
        for field in TestUIContact.contact_data_schema:
            add_contact_page.enter_into_field(field, contact_default[field])
        contact_list_page = add_contact_page.click_submit()
        parsed_contacts = contact_list_page.parse_contact_list_table()
        for contact in parsed_contacts:
            assert contact[0] == contact_default["firstName"] + " " + contact_default["lastName"]
            assert contact[1] == contact_default["birthdate"]
            assert contact[2] == contact_default["email"]
            assert contact[3] == contact_default["phone"]
            assert contact[4] == contact_default["street1"] + " " + contact_default["street2"]
            assert contact[5] == contact_default["city"] + " " + contact_default["stateProvince"] + " " + contact_default["postalCode"]
            assert contact[6] == contact_default["country"]

    def test_add_contact_invalid(self, contact_list_page: ContactListPage):
        contact_invalid = {
            "firstName": "Will",
            "lastName": "Smith",
            "birthdate": "123",
            "email": "will.smith@mail.com",
            "phone": "1234567890",
            "street1": "1 Main St.",
            "street2": "Apartment A",
            "city": "New York",
            "stateProvince": "NY",
            "postalCode": "10118",
            "country": "USA",
        }
        add_contact_page = contact_list_page.click_add_new_contact()
        for field in TestUIContact.contact_data_schema:
            add_contact_page.enter_into_field(field, contact_invalid[field])
        redirected_to = add_contact_page.click_submit_expecting_failure()
        assert redirected_to.is_error_present_with_text("Contact validation failed")
