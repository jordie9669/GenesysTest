import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

import Locators.locators

driver = webdriver.Chrome(
    executable_path='C:/Users/New User/PycharmProjects/GenesysTest/drivers/chromedriver.exe')
l = Locators.locators


class TestRyanair:

    @pytest.fixture
    def search_flights(self):
        driver.get('https://www.ryanair.com/')
        # accept cookie popup
        driver.find_element(By.CLASS_NAME, "cookie-popup-with-overlay__button").click()
        driver.find_element(By.ID, 'input-button__destination').click()
        time.sleep(1)
        # select city
        city = driver.find_element(By.XPATH, l.city)
        city.click()
        time.sleep(1)
        departure_date = driver.find_element(By.XPATH, l.departure_date)
        departure_date.click()
        return_date = driver.find_element(By.XPATH, l.return_date)
        return_date.click()
        search = driver.find_element(By.XPATH, l.search_button)
        search.click()
        time.sleep(4)

    def test_suggested_flights_details(self, search_flights):
        details = driver.find_element(By.XPATH, l.details)
        split_details = details.text.split()
        depart_date = split_details[1] + ' ' + split_details[2]
        assert depart_date == '19 Nov'
        return_date = split_details[4] + ' ' + split_details[5]
        assert return_date == '1 Dec'
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
