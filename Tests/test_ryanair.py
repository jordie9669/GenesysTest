import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(
    executable_path='C:/Users/New User/PycharmProjects/GenesysTest/drivers/chromedriver.exe')


class TestRyanair:

    @pytest.fixture
    def search_flights(self):
        driver.get('https://www.ryanair.com/')
        # accept cookie popup
        driver.find_element(By.CLASS_NAME, "cookie-popup-with-overlay__button").click()
        driver.find_element(By.ID, 'input-button__destination').click()
        time.sleep(1)
        city = driver.find_element(By.XPATH,
                                   '//*[@id="ry-tooltip-3"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-destination-container/fsw-airports/div/fsw-airports-list/div[2]/div[1]/fsw-airport-item[4]')
        city.click()
        time.sleep(1)
        departure_date = driver.find_element(By.XPATH,
                                             '//*[@id="ry-tooltip-6"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-flexible-datepicker-container/fsw-datepicker/ry-datepicker-desktop/div[1]/calendar[1]/calendar-body/div[4]/div[16]/div')
        departure_date.click()

        return_date = driver.find_element(By.XPATH,
                                          '//*[@id="ry-tooltip-7"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-flexible-datepicker-container/fsw-datepicker/ry-datepicker-desktop/div[1]/calendar[2]/calendar-body/div[2]/div[10]/div')
        return_date.click()
        num_passengers = driver.find_element(By.XPATH,
                                             '/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/fsw-flight-search-widget-controls-container/fsw-flight-search-widget-controls/div[2]/fsw-input-button/div/div[2]')
        search = driver.find_element(By.XPATH, '/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/div/div/button')
        search.click()
        time.sleep(4)

    def test_suggested_flights_details(self, search_flights):
        details = driver.find_element(By.XPATH, '/html/body/app-root/flights-root/div/div/flights-trip-details-container/flights-trip-details/div/div[2]')
        split_details = details.text.split()
        depart_date = split_details[1] + ' ' + split_details[2]
        assert depart_date == '19 Nov'
        return_date = split_details[4] + ' ' + split_details[5]
        assert return_date == '1 Dec'
        num_passengers = split_details[6]
        assert num_passengers == '1'

    def test_login_and_passengers_is_displayed_after_selecting_flights(self):
        # select departure flight
        driver.find_element(By.XPATH,
                            '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/flight-list/div/flight-card/div/div/div[3]/button').click()
        # select return flight
        driver.find_element(By.XPATH,
                            '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[2]/journey-container/journey/flight-list/div/flight-card/div/div/div[3]/button').click()
        time.sleep(1)
        #  select regular option
        driver.find_element(By.XPATH,
                            '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/fare-selector-container/fare-selector/div/fare-table-container/fare-table/div[2]/ry-spinner/div[2]/div/div/fare-card/div/div/button').click()
        time.sleep(3)
        login_to_my_ryanair_section = driver.find_element(By.XPATH, '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-passengers/pax-app-container/pax-app/ry-spinner/ry-login-touchpoint-container/ry-login-touchpoint/div')
        assert login_to_my_ryanair_section.is_displayed()
        passengers_section = driver.find_element(By.XPATH, '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-passengers/pax-app-container/pax-app/ry-spinner/div/div')
        assert passengers_section.is_displayed()

    # def test_passengers_section_becomes_enabled_after_skipping_login(self):
    #     login_later = driver.find_element(By.XPATH,
    #                                           '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-passengers/pax-app-container/pax-app/ry-spinner/ry-login-touchpoint-container/ry-login-touchpoint/div/button/div')
    #     login_later.click()
