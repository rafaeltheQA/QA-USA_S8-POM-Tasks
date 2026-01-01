import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import retrieve_phone_code


class UrbanRoutesPage:
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_TAXI_BUTTON_LOCATOR = (By.XPATH, '//button[@class="button round"]')
    SUPPORTIVE_PLAN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(text(), 'Supportive')]")
    ACTIVE_SELECTION_VALUE_LOCATOR = (By. CSS_SELECTOR, 'div[class="tcard active"]')
    PHONE_NUMBER_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div.np-text')
    PHONE_NUMBER_INPUT_LOCATOR = (By.ID, "phone")
    GET_PHONE_NUMBER_LOCATOR = (By.ID, "get_phone_number")
    SET_PHONE_CODE_LOCATOR = (By.ID, "set_phone_code")
    SMS_INPUT_LOCATOR = (By.XPATH, "//input[contains(@class, 'input')]")
    SEND_SMS_BUTTON_LOCATOR = (By.XPATH, "//button[contains(@class, 'button')]")
    CLICK_CONFIRM_BUTTON_LOCATOR = (By.XPATH, "//button[contains(text(),'Confirm')]")
    CONFIRM_CODE_FIELD_LOCATOR = (By.ID, "code")
    CLICK_PAYMENT_METHOD_LOCATOR = (By.XPATH, "//div[@class='pp-text']")
    ADD_CARD_LOCATOR = (By.XPATH, "//div[contains(text(),'Add card')]")
    ENTER_CREDIT_CARD_LOCATOR = (By.ID, "number")
    ENTER_CREDIT_CARD_CODE_LOCATOR = (By.ID, "code")
    CODE_FIELD_INPUT_LOCATOR = (By. XPATH, "//div[@class='input-container']//input[@id='code']")
    LINK_BUTTON_LOCATOR = (By.XPATH, "//button[contains(., 'Link')]")
    VERIFY_CARD_ADDED_LOCATOR = (By.CLASS_NAME, "checkbox")
    PAYMENT_METHOD_VALUE = (By.XPATH, "//div[@class='pp-value-text']")
    COMMENT_INPUT = (By.ID, "comment")
    BLANKET_TOGGLE_SWITCH = (By.XPATH, "//div[normalize-space()='Blanket and handkerchiefs']/following-sibling::div//div[@class='switch']")
    BLANKET_CHECKBOX = (By. XPATH, "//div[normalize-space()='Blanket and handkerchiefs']/following-sibling::div//input[@type='checkbox']")
    ICE_CREAM_PLUS_BTN = (By.XPATH, "//div[.='Ice cream']/following::div[contains(@class, 'counter-plus')][1]")
    ICE_CREAM_COUNT = (By. XPATH, "//div[.='Ice cream']/following::div[contains(@class,'counter-value')][1]")
    MESSAGE_TO_DRIVER_INPUT = (By.ID, "comment")
    CLICK_ORDER_BUTTON = (By.XPATH, "//button[.='Order']")

    def __init__(self, driver):
        self.driver = driver

    def enter_from_location(self, from_text):
        wait = WebDriverWait(self.driver, 10)
        from_field = wait.until(EC.element_to_be_clickable(self.FROM_LOCATOR))
        from_field.send_keys(from_text)
    def enter_to_location(self, to_text):
        wait = WebDriverWait(self.driver, 10)
        to_field = wait.until(EC.element_to_be_clickable(self.TO_LOCATOR))
        to_field.send_keys(to_text)
    def get_from_location(self):
        return self.driver.find_element(*self.FROM_LOCATOR).get_attribute("value")
    def get_to_location(self):
        return self.driver.find_element(*self.TO_LOCATOR).get_attribute("value")

    def enter_locations(self, from_text, to_text):
            self.enter_from_location(from_text)
            self.enter_to_location(to_text)

    def click_call_taxi_button(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON_LOCATOR))
        element.click()
    def click_supportive_plan_button(self):
        wait = WebDriverWait(self.driver, 10)
        supportive_plan: WebElement = wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_BUTTON_LOCATOR))
        supportive_plan.click()

    def get_active_selection_value(self):
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located(self.ACTIVE_SELECTION_VALUE_LOCATOR))
            return element.text

    def click_phone_field(self):
        element = self.driver.find_element(*self.PHONE_NUMBER_BUTTON_LOCATOR)
        element.click()
    def enter_phone_number(self, phone_number):
        wait = WebDriverWait(self.driver, 10)
        phone_input = wait.until(EC.element_to_be_clickable(self.PHONE_NUMBER_INPUT_LOCATOR))
        phone_input.clear()
        phone_input.send_keys(phone_number)

    def enter_sms_input_locator(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.SMS_INPUT_LOCATOR))
        element.click()

    def send_sms_button(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.SEND_SMS_BUTTON_LOCATOR))
        element.click()

    def enter_confirmation_code(self):
        code = retrieve_phone_code(self.driver)
        sms_field = self.driver.find_element(*self.SMS_INPUT_LOCATOR)
        sms_field.send_keys(phone_code)

    def get_phone_number(self):
        self.driver.find_element(*self.GET_PHONE_NUMBER_LOCATOR).click()

    def click_payment_method(self):
        self.driver.find_element(*self.CLICK_PAYMENT_METHOD_LOCATOR).click()
    def click_add_card_button(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.ADD_CARD_LOCATOR))
        element.click()

    def enter_credit_card(self, card_number):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.ENTER_CREDIT_CARD_LOCATOR))
        element.click()
        element.clear()
        element.send_keys('1234 5678 9100')
        element.send_keys(Keys.TAB)

    def enter_credit_card_code(self, card_code):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.CODE_FIELD_INPUT_LOCATOR))
        element.clear()
        element.send_keys(card_code)
        element.send_keys(Keys.TAB)



    def click_link_button_locator(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.LINK_BUTTON_LOCATOR))
        element.click()

    def get_payment_method_text(self):
        return self.driver.find_element(*self.PAYMENT_METHOD_VALUE).text


    def enter_comment(self, text):
        self.driver.find_element(*self.COMMENT_INPUT).send_keys(text)
    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    def click_blanket_toggle(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE_SWITCH))
        element.click()
    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).is_selected()

    def order_ice_cream(self, times):
        plus_btn = self.driver.find_element(*self.ICE_CREAM_PLUS_BTN)
        for _ in range(times):
            plus_btn.click()
    def get_ice_cream_count(self):
        """Retrieve the displayed ice cream count"""
        return self.driver.find_element(*self.ICE_CREAM_COUNT).text

    def click_order_button(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(self.CLICK_ORDER_BUTTON))
        element.click()

    def is_car_search_modal_displayed(self):
        pass

