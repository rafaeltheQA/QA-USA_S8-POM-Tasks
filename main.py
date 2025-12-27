from selenium import webdriver
from helpers import retrieve_phone_code, is_url_reachable
from pages import UrbanRoutesPage
import data
from selenium.webdriver import DesiredCapabilities


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

        if is_url_reachable(data.URBAN_ROUTES_URL):
            print("some success message here")
            cls.driver.get(data.URBAN_ROUTES_URL)
        else:
            print("Cannot connect to the Urban Routes. Check the server is on and and still running")

    def test_set_route(self):
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations("East 2nd Street, 601", "1300 1st St")
        assert urban_routes_page.get_from_location() == "East 2nd Street, 601"
        assert urban_routes_page.get_to_location() == "1300 1st St"

    def test_select_plan(self):
       urban_routes_page = UrbanRoutesPage(self.driver)
       urban_routes_page.enter_from_location("East 2nd Street, 601")
       urban_routes_page.enter_to_location("1300 1st St")
       urban_routes_page.taxi_icon_locator()
       urban_routes_page.click_taxi_text_locator()
       urban_routes_page.click_duration_text_locator()
       urban_routes_page.click_call_taxi_button()
       urban_routes_page.click_supportive_plan_button()
       urban_routes_page.click_supportive_plan_select_locator()
       actual_value = urban_routes_page.get_active_selection_value()
       expected_value = "Supportive\n$8.35"
       assert actual_value in expected_value, f"Expected {expected_value}' but got {actual_value}"

    def test_fill_phone_number(self):
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_from_location("East 2nd Street, 601")
        urban_routes_page.enter_to_location("1300 1st St")
        urban_routes_page.taxi_icon_locator()
        urban_routes_page.click_taxi_text_locator()
        urban_routes_page.click_duration_text_locator()
        urban_routes_page.click_phone_field()
        urban_routes_page.enter_phone_number(self.driver)
        urban_routes_page.send_sms_button()
        urban_routes_page.enter_confirmation_code()
        actual_phone = urban_routes_page.get_phone_number()
        expected_phone = "+1 123 123 12 12"
        assert expected_phone in actual_phone, f"Expected '{expected_phone}', but got '{actual_phone}'"

    def test_fill_card(self):
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_from_location("East 2nd Street, 601")
        urban_routes_page.enter_to_location("1300 1st St")
        urban_routes_page.taxi_icon_locator()
        urban_routes_page.click_taxi_text_locator()
        urban_routes_page.click_duration_text_locator()
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_supportive_plan_select_locator()
        urban_routes_page.click_payment_method()
        urban_routes_page.click_add_card_button()
        urban_routes_page.enter_credit_card()
        urban_routes_page.enter_credit_card_code()
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.change_focus_from_code_field()
        urban_routes_page.click_link_button_locator()
        urban_routes_page.verify_card_added_checkmark()
        urban_routes_page.get_payment_method_text()
        assert urban_routes_page.get_payment_method_text() == "Card"

    def test_comment_for_driver(self):
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_from_location("East 2nd Street, 601")
        urban_routes_page.enter_to_location("1300 1st St")
        urban_routes_page.taxi_icon_locator()
        urban_routes_page.click_taxi_text_locator()
        urban_routes_page.click_duration_text_locator()
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_supportive_plan_select_locator()
        urban_routes_page.enter_comment(text='Stop at the juice bar, please')
        actual_value = urban_routes_page.get_driver_comment()
        expected_value = "Stop at the juice bar, please"
        assert actual_value == expected_value,  \
            f"Expected '{expected_value}' but got '{actual_value}'"

    def test_order_blanket_and_handkerchief(self):
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_from_location("East 2nd Street, 601")
        urban_routes_page.enter_to_location("1300 1st St")
        urban_routes_page.taxi_icon_locator()
        urban_routes_page.click_taxi_text_locator()
        urban_routes_page.click_duration_text_locator()
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_supportive_plan_select_locator()
        urban_routes_page.click_blanket_toggle()
        assert urban_routes_page.is_blanket_selected() is True, \
            "Blanket and handkerchiefs toggle should be ON"


    def test_order_2_ice_cream(self):
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_from_location("East 2nd Street, 601")
        urban_routes_page.enter_to_location("1300 1st St")
        urban_routes_page.taxi_icon_locator()
        urban_routes_page.click_taxi_text_locator()
        urban_routes_page.click_duration_text_locator()
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_supportive_plan_select_locator()
        urban_routes_page.order_ice_cream(times=2)
        ice_cream_count = urban_routes_page.get_ice_cream_count()
        assert ice_cream_count == "2", f"Expected cont 2 but got {ice_cream_count}"

    def test_car_search_model_appears(self):
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_from_location("East 2nd Street, 601")
        urban_routes_page.enter_to_location("1300 1st St")
        urban_routes_page.taxi_icon_locator()
        urban_routes_page.click_taxi_text_locator()
        urban_routes_page.click_duration_text_locator()
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_supportive_plan_select_locator()
        urban_routes_page.click_phone_field()
        urban_routes_page.enter_phone_number(self.driver)
        urban_routes_page.send_sms_button()
        urban_routes_page.enter_confirmation_code()
        actual_phone = urban_routes_page.get_phone_number()
        expected_phone = "+1 123 123 12 12"
        assert expected_phone in actual_phone, f"Expected '{expected_phone}', but got '{actual_phone}'"
        urban_routes_page.enter_message_for_driver('Stop at the juice bar, please')


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()