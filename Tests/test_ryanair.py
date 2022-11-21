import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Locators.locators

driver = webdriver.Chrome(
    executable_path='GenesysTest/drivers/chromedriver.exe')
driver.implicitly_wait(30)
l = Locators.locators


class TestRyanair:

    # FIXTURES
    @pytest.fixture
    def search_flights(self):
        driver.get('https://www.ryanair.com/')
        # accept cookie popup
        driver.find_element(By.CLASS_NAME, "cookie-popup-with-overlay__button").click()
        driver.find_element(By.ID, 'input-button__destination').click()
        # select depart city
        driver.find_element(By.XPATH, l.from_field).click()
        driver.find_element(By.XPATH, l.from_city).click()
        city = driver.find_element(By.XPATH, l.city)
        city.click()
        driver.find_element(By.XPATH, l.month_april).click()
        driver.find_element(By.XPATH, l.depart_date_april_19).click()
        driver.find_element(By.XPATH, l.return_date_april_26).click()
        search = driver.find_element(By.XPATH, l.search_button)
        search.click()
        # Using sleep here as when I used an explicit wait the list index for test_suggested_flight_details
        # was out of range
        time.sleep(2)

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

    @pytest.fixture()
    def choose_seats(self):
        # This method will only work for the first time running the test as the chosen seats are kept for a few minutes
        # after choosing and will not be clickable. I tried to get a list of the seats and move to the next element in
        # the list each time the test ran but I kept getting an empty list and wasn't sure why.
        assert driver.find_element(By.XPATH, l.flight_detail).text == 'Dublin to Alicante'
        driver.find_element(By.ID, l.outward_flight_seat).click()
        driver.find_element(By.XPATH, l.next_flight_button).click()
        time.sleep(5)
        assert driver.find_element(By.XPATH, l.flight_detail).text == 'Alicante to Dublin'
        driver.find_element(By.ID, l.return_flight_seat).click()

    # TESTS
    def test_suggested_flights_details(self, search_flights):
        details = driver.find_element(By.XPATH, l.details)
        split_details = details.text.split()
        depart_date = split_details[1] + ' ' + split_details[2]
        assert depart_date == '19 Apr'
        return_date = split_details[4] + ' ' + split_details[5]
        assert return_date == '26 Apr'
        num_passengers = split_details[6]
        assert num_passengers == '1'

    def test_login_and_passengers_is_displayed_after_selecting_flights(self):
        # select departure flight
        driver.find_element(By.XPATH, l.departure_flight).click()
        # select return flight
        driver.find_element(By.XPATH, l.return_flight).click()
        #  select regular option
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, l.regular_option)))
        driver.find_element(By.XPATH, l.regular_option).click()
        login_to_my_ryanair_section = driver.find_element(By.XPATH, l.login_to_myryanair_section)
        assert login_to_my_ryanair_section.is_displayed()
        passengers_section = driver.find_element(By.XPATH, l.passengers_section)
        assert passengers_section.is_displayed()

    def test_passengers_section_becomes_enabled_after_skipping_login(self):
        login_later = driver.find_element(By.XPATH, l.login_later)
        login_later.click()
        passengers_section = driver.find_element(By.XPATH, l.passengers_section)
        assert passengers_section.is_enabled()

    def test_seating_page_outward_flight_is_displayed(self, enter_passenger_info):
        driver.find_element(By.XPATH, l.continuen_button).click()
        assert driver.find_element(By.XPATH, l.seating_page_tile).is_displayed()

    # The following 2 tests may fail when the test suite is ran for the second time in quick succession
    # due to the issue mentioned above in the choose_seats fixture. They will pass again once the seats have been
    # cleared after a few minutes
    def test_seating_page_return_flight_is_displayed(self):
        assert driver.find_element(By.XPATH, l.seat_continue_button).is_displayed()

    def test_bags_page_is_displayed(self, choose_seats):
        driver.find_element(By.XPATH, l.seat_continue_button).click()
        time.sleep(5)
        if(driver.find_element(By.XPATH, l.fast_track_popup)).is_displayed():
            driver.find_element(By.XPATH, l.fast_track_popup).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, l.cabin_bags_title)))
        assert driver.find_element(By.XPATH, l.cabin_bags_title).is_displayed()
