from selenium import webdriver
from helpers import retrieve_phone_code, is_url_reachable
from pages import UrbanRoutesPage
import data, time
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
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to the Urban Routes. Check the server is on and and still running")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert urban_routes_page.get_from_location() == data.ADDRESS_FROM
        assert urban_routes_page.get_to_location() == data.ADDRESS_TO

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.get_active_selection_value()
        actual_value = urban_routes_page.get_active_selection_value()
        expected_value = "Supportive"
        assert expected_value in actual_value, f"Expected {expected_value}' but got {actual_value}"

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_phone_field()
        urban_routes_page.enter_phone_number(data.PHONE_NUMBER)
        urban_routes_page.click_next_button()
        urban_routes_page.click_confirmation_code()
        urban_routes_page.click_confirm_button()
        assert urban_routes_page.get_phone_number() == data.PHONE_NUMBER


    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_payment_method()
        time.sleep(2)
        urban_routes_page.click_add_card_button()
        urban_routes_page.enter_credit_card(data.CARD_NUMBER)
        urban_routes_page.enter_credit_card_code(data.CARD_CODE)
        urban_routes_page.click_link_button_locator()
        assert urban_routes_page.get_payment_method_text() == "Card"

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.enter_comment(text=data.MESSAGE_FOR_DRIVER)
        actual_value = urban_routes_page.get_driver_comment()
        expected_value = data.MESSAGE_FOR_DRIVER
        assert actual_value == expected_value, f"Expected '{expected_value}' but got '{actual_value}'"

    def test_order_blanket_and_handkerchief(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_blanket_toggle()
        assert urban_routes_page.is_blanket_selected(),"Blanket and handkerchiefs toggle should be ON"

    def test_order_2_ice_cream(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.order_ice_cream(times=2)
        ice_cream_count = urban_routes_page.get_ice_cream_count()
        assert ice_cream_count == "2", f"Expected cont 2 but got {ice_cream_count}"

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban_routes_page = UrbanRoutesPage(self.driver)
        urban_routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban_routes_page.click_call_taxi_button()
        urban_routes_page.click_supportive_plan_button()
        urban_routes_page.click_phone_field()
        urban_routes_page.enter_phone_number(data.PHONE_NUMBER)
        urban_routes_page.click_next_button()
        urban_routes_page.click_confirmation_code()
        urban_routes_page.enter_comment(data.MESSAGE_FOR_DRIVER)
        print("About to look for order button...")
        urban_routes_page.click_order_button()
        assert urban_routes_page.is_car_search_modal_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()