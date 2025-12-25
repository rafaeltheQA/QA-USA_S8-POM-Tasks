import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

from helpers import retrieve_phone_code
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    TAXI_ICON_LOCATOR = (By.XPATH, '//img[@src="/static/media/taxi-active.b0be3054.svg"]')
    TAXI_TEXT_LOCATOR = (By.XPATH, '//div[@class="results-text"]//div[@class="text"]')
    DURATION_TEXT_LOCATOR = (By.XPATH, '//div[@class="results-text"]//div[@class="duration"]')
    CALL_TAXI_BUTTON_LOCATOR = (By.XPATH, '//button[@class="button round"]')
    CLICK_SUPPORTIVE_PLAN_BUTTON_LOCATOR = (By.XPATH, '//button[@class="button round"]')
    SUPPORTIVE_PLAN_SELECTION_LOCATOR = (By. XPATH, '//div[contains(text(),"Supportive")]')
    ACTIVE_SELECTION_VALUE_LOCATOR = (By. CSS_SELECTOR, 'div[class="tcard active"]')
    PHONE_NUMBER_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div.np-text')
    PHONE_NUMBER_INPUT_LOCATOR = (By.ID, "phone")
    GET_PHONE_NUMBER_LOCATOR = (By.ID, "get_phone_number")
    SET_PHONE_CODE_LOCATOR = (By.ID, "set_phone_code")
    SEND_SMS_BUTTON_LOCATOR = (By.XPATH, "//button[@class='button full' and normalize-space(text())='Send SMS']")
    CLICK_CONFIRM_BUTTON_LOCATOR = (By.XPATH, "//button[contains(text(),'Confirm')]")
    CONFIRM_CODE_FIELD_LOCATOR = (By.ID, "sms_code")
    CLICK_PAYMENT_METHOD_LOCATOR = (By.XPATH, "//div[@class='pp-text']")
    ADD_CARD_LOCATOR = (By.XPATH, "//div[contains(text(),'Add card')]")
    ENTER_CREDIT_CARD_LOCATOR = (By.ID, "number")
    ENTER_CREDIT_CARD_CODE_LOCATOR = (By.ID, "code")
    CODE_FIELD_INPUT_LOCATOR = (By.XPATH, "//div[contains(@class,'card-code-input')]//input[@id='code']")
    LINK_BUTTON_LOCATOR = (By.XPATH, "//button[contains(., 'Link')]")
    VERIFY_CARD_ADDED_LOCATOR = (By.CLASS_NAME, "checkbox")
    PAYMENT_METHOD_VALUE = (By.XPATH, "//div[@class='pp-value-text']")
    COMMENT_INPUT = (By.ID, "comment")
    BLANKET_TOGGLE_SLIDER = (By.XPATH, "//div[normalize-space()='Blanket and handkerchiefs']"
                                       "/following-sibling::div//span[contains(@class, 'slider')]")
    BLANKET_TOGGLE_INPUT = (By.XPATH, "//div[normalize-space()='Blanket and handkerchiefs']"
                                       "/following-sibling::div//input[@type='checkbox']")
    ICE_CREAM_PLUS_BTN = (By.XPATH, "//div[.='Ice cream']/following::div[contains(@class, 'counter-plus')][1]")
    ICE_CREAM_COUNT = (By. XPATH, "//div[.='Ice cream']/following::div[contains(@class,'counter-value')][1]")
    MESSAGE_TO_DRIVER_INPUT = (By.ID, "comment")
    ORDER_BUTTON = (By.XPATH, "//button[.='Order']")

    def __init__(self, driver):
        self.driver = driver

    def enter_from_location(self, from_text):
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(from_text)
    def enter_to_location(self, to_text):
        self.driver.find_element(*self.TO_LOCATOR).send_keys(to_text)
    def get_from_location(self):
        return self.driver.find_element(*self.FROM_LOCATOR).get_attribute("value")
    def get_to_location(self):
        return self.driver.find_element(*self.TO_LOCATOR).get_attribute("value")

    def enter_locations(self, from_text, to_text):
            self.enter_from_location(from_text)
            self.enter_to_location(to_text)

    def taxi_icon_locator(self):
        wait = WebDriverWait(self.driver, timeout=10)
        taxi_button = wait.until(EC.element_to_be_clickable(self.TAXI_ICON_LOCATOR))
        if not taxi_button.get_attribute("class").__contains__("active"):
            taxi_button.click()
    def click_taxi_text_locator(self):
        self.driver.find_element(*self.TAXI_TEXT_LOCATOR).click()
    def click_duration_text_locator(self):
        self.driver.find_element(*self.DURATION_TEXT_LOCATOR).click()
    def click_call_taxi_button(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON_LOCATOR).click()
    def click_supportive_plan_button(self):
        try:
            current_value = self.get_active_selection_value()

            if current_value == "Supportive Plan":
                print("Supportive Plan is already selected")
                return

            wait = WebDriverWait(self.driver, 10)
            button = wait.until(
                EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_SELECTION_LOCATOR)
            )
            button.click()

        except TimeoutException:
            raise Exception("Supportive Plan was not clickable within 10 seconds.")

        except NoSuchElementException:
            raise Exception("Supportive Plan was not found on the page.")

        except Exception as e:
            raise Exception(f"Unexpected error while clicking Supportive Plan: {e}")
    def click_supportive_plan_select_locator(self):
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_SELECTION_LOCATOR))
            button.click()
    def get_active_selection_value(self):
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located(self.ACTIVE_SELECTION_VALUE_LOCATOR))
            return element.text

    def click_phone_field(self):
        print("DEBUG: About to click phone field")
        try:
            # First, try to find and click normally
            element = self.driver.find_element(*self.PHONE_NUMBER_BUTTON_LOCATOR)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            element.click()
            print("DEBUG: Phone field clicked successfully")
        except Exception as e:
            print(f"DEBUG: Normal click failed: {e}")
            # If normal click fails, try JavaScript click
            element = self.driver.find_element(*self.PHONE_NUMBER_BUTTON_LOCATOR)
            self.driver.execute_script("arguments[0].click();", element)
            print("DEBUG: Phone field clicked with JavaScript")
    def enter_phone_number(self, phone_number):
        phone_input = self.driver.find_element(*self.PHONE_NUMBER_INPUT_LOCATOR)
        phone_input.clear()
        phone_input.send_keys("+1 123 123 12 12")
    def send_sms_button(self):
        try:
            iframe = self.driver.find_element(By. ID, "iframe-id")
            self.driver.switch_to.frame(iframe)
            wait = WebDriverWait(self.driver, 10)
            send_btn = wait.until(EC.element_to_be_clickable(self.SEND_SMS_BUTTON_LOCATOR))
            send_btn.click()
        except Exception:
            pass
    def enter_confirmation_code(self):
        code = retrieve_phone_code
        assert code, "SMS confirmation code was not retrieved"
    def get_phone_number(self):
        return self.driver.find_element(*self.PHONE_NUMBER_INPUT_LOCATOR).get_attribute("value")
    def click_payment_method(self):
        self.driver.find_element(*self.CLICK_PAYMENT_METHOD_LOCATOR).click()
    def click_add_card_button(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.ADD_CARD_LOCATOR))
        element.click()

    def enter_credit_card(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.ENTER_CREDIT_CARD_LOCATOR))
        element.click()
        element.clear()
        element.send_keys('1234 5678 9100')
        element.send_keys(Keys.TAB)

    def enter_credit_card_code(self):
        time.sleep(2)
        print("About to look for credit card code field...")
        wait = WebDriverWait(self.driver, 15)
        element = wait.until(EC.visibility_of_element_located(self.ENTER_CREDIT_CARD_LOCATOR))
        element = wait.until(EC.element_to_be_clickable(self.ENTER_CREDIT_CARD_CODE_LOCATOR))
        print("Found code field successfully!")
        element.send_keys('1111')
        print("Entered code successfully!")
        element.send_keys(Keys.TAB)

    def change_focus_from_code_field(self):
        code_field = self.driver.find_element(*self.CODE_FIELD_INPUT_LOCATOR)
        code_field.send_keys(Keys.TAB)
    def click_outside_to_change_focus(self):
        self.driver.find_element(By. TAG_NAME, "body").click()
    def wait_for_link_button_clickable(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.LINK_BUTTON_LOCATOR))
    def click_link_button_locator(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.LINK_BUTTON_LOCATOR))
        element.click()
    def verify_card_added_checkmark(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located(self.VERIFY_CARD_ADDED_LOCATOR))
        element.click()
    def get_payment_method_text(self):
        return self.driver.find_element(*self.PAYMENT_METHOD_VALUE).text



    def enter_comment(self, text):
        self.driver.find_element(*self.COMMENT_INPUT).send_keys(text)
    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    def click_blanket_toggle(self):
        self.driver.find_element(*self.BLANKET_TOGGLE_SLIDER).click()
    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_TOGGLE_INPUT).get_property("checked")

    def order_ice_cream(self, times=1):
        plus_btn = self.driver.find_element(*self.ICE_CREAM_PLUS_BTN)
        for _ in range(times):
            plus_btn.click()
    def get_ice_cream_count(self):
        """Retrieve the displayed ice cream count"""
        return self.driver.find_element(*self.ICE_CREAM_COUNT).text

    def enter_message_for_driver(self, message):
        self.driver.find_element(*self.MESSAGE_TO_DRIVER_INPUT).send_keys(message)






