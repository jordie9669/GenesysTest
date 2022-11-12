import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Locators.locators

driver = webdriver.Chrome(
    executable_path='GenesysTest/drivers/chromedriver.exe')
driver.implicitly_wait(10)
l = Locators.locators


class TestRyanair:

    # FIXTURES
    @pytest.fixture
    def search_flights(self):
        driver.get('https://www.ryanair.com/')
        # accept cookie popup
        driver.find_element(By.CLASS_NAME, "cookie-popup-with-overlay__button").click()
        driver.find_element(By.ID, 'input-button__destination').click()
        # select city
        city = driver.find_element(By.XPATH, l.city)
        city.click()
        driver.find_element(By.XPATH, l.month_april).click()
        driver.find_element(By.XPATH, l.depart_date_april_19).click()
        driver.find_element(By.XPATH, l.return_date_april_27).click()
        search = driver.find_element(By.XPATH, l.search_button)
        search.click()
        time.sleep(4)

    @pytest.fixture
    def enter_passenger_info(self):
        driver.find_element(By.XPATH, l.passenger_title).click()
        driver.find_element(By.XPATH, l.passenger_title_mr).click()
        first_name_field = driver.find_element(By.XPATH, l.passenger_first_name)
        first_name_field.click()
        first_name_field.send_keys('John')
        last_name_field = driver.find_element(By.XPATH, l.passenger_last_name)
        last_name_field.click()
        last_name_field.send_keys('Doe')
        driver.find_element(By.XPATH, l.continuen_button).click()

    @pytest.fixture()
    def choose_seats(self):
        driver.find_elements(By.XPATH, l.row_of_seats)
        assert driver.find_element(By.XPATH, l.outward_flight_detail).text == 'Dublin to Alicante'
        driver.find_element(By.XPATH, l.outward_flight_seat).click()
        driver.find_element(By.XPATH, l.next_flight_button).click()
        time.sleep(3)
        assert driver.find_element(By.XPATH, l.outward_flight_detail).text == 'Alicante to Dublin'
        driver.find_element(By.XPATH, l.return_flight_seat).click()
        driver.find_element(By.XPATH, l.seat_continue_button).click()
        if(driver.find_element(By.XPATH, l.fast_track_popup)).is_displayed():
            driver.find_element(By.XPATH, l.fast_track_popup).click()
        time.sleep(3)

    # TESTS
    def test_suggested_flights_details(self, search_flights):
        details = driver.find_element(By.XPATH, l.details)
        split_details = details.text.split()
        depart_date = split_details[1] + ' ' + split_details[2]
        assert depart_date == '19 Apr'
        return_date = split_details[4] + ' ' + split_details[5]
        assert return_date == '27 Apr'
        num_passengers = split_details[6]
        assert num_passengers == '1'

    def test_login_and_passengers_is_displayed_after_selecting_flights(self):
        # select departure flight
        driver.find_element(By.XPATH, l.departure_flight).click()
        # select return flight
        driver.find_element(By.XPATH, l.return_flight).click()
        time.sleep(1)
        #  select regular option
        driver.find_element(By.XPATH, l.regular_option).click()
        time.sleep(3)
        login_to_my_ryanair_section = driver.find_element(By.XPATH, l.login_to_myryanair_section)
        assert login_to_my_ryanair_section.is_displayed()
        passengers_section = driver.find_element(By.XPATH, l.passengers_section)
        assert passengers_section.is_displayed()

    def test_passengers_section_becomes_enabled_after_skipping_login(self):
        login_later = driver.find_element(By.XPATH, l.login_later)
        login_later.click()
        passengers_section = driver.find_element(By.XPATH, l.passengers_section)
        assert passengers_section.is_enabled()

    def test_seating_page_first_flight_is_displayed(self, enter_passenger_info):
        assert driver.find_element(By.XPATH, l.seating_page_tile).is_displayed()

    def test_bags_page_is_displayed(self, choose_seats):
        assert driver.find_element(By.XPATH, l.cabin_bags_title).is_displayed()
