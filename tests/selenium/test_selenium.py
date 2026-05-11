import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from tests.selenium.conftest import BASE_URL, fill_form


def test_valid_submission_shows_result_table(driver):
    fill_form(driver, "100.00", "5.0", "australia", "standard")
    wait = WebDriverWait(driver, 5)
    table = wait.until(EC.visibility_of_element_located((By.ID, "result-table")))
    assert table.is_displayed()


def test_australia_10_percent_gst_in_result(driver):
    fill_form(driver, "100.00", "5.0", "australia", "standard")
    wait = WebDriverWait(driver, 5)
    wait.until(EC.visibility_of_element_located((By.ID, "result-table")))
    tax_cell = driver.find_element(By.ID, "tax-amount")
    assert "10.00" in tax_cell.text


def test_express_result_contains_express(driver):
    fill_form(driver, "100.00", "5.0", "australia", "express")
    wait = WebDriverWait(driver, 5)
    wait.until(EC.visibility_of_element_located((By.ID, "result-table")))
    shipping_type_cell = driver.find_element(By.ID, "result-shipping-type")
    assert "express" in shipping_type_cell.text.lower()


def test_empty_price_shows_error_element(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "weight").send_keys("5.0")
    Select(driver.find_element(By.ID, "region")).select_by_value("australia")
    Select(driver.find_element(By.ID, "shipping_type")).select_by_value("standard")
    driver.find_element(By.ID, "calculate-btn").click()
    wait = WebDriverWait(driver, 5)
    error = wait.until(EC.visibility_of_element_located((By.ID, "error-message")))
    assert error.is_displayed()


def test_negative_price_shows_negative_error(driver):
    fill_form(driver, "-10.00", "5.0", "australia", "standard")
    wait = WebDriverWait(driver, 5)
    error = wait.until(EC.visibility_of_element_located((By.ID, "error-message")))
    assert "negative" in error.text.lower()


def test_reset_clears_result_and_shows_form(driver):
    fill_form(driver, "100.00", "5.0", "australia", "standard")
    wait = WebDriverWait(driver, 5)
    wait.until(EC.visibility_of_element_located((By.ID, "result-table")))
    driver.find_element(By.ID, "reset-btn").click()
    wait.until(EC.invisibility_of_element_located((By.ID, "result-card")))
    form = driver.find_element(By.ID, "shipping-form")
    assert form.is_displayed()
    assert driver.current_url == BASE_URL + "/"
