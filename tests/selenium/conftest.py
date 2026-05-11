import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


def fill_form(driver, price, weight, region, shipping_type):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select

    driver.get(BASE_URL)

    driver.find_element(By.ID, "price").clear()
    driver.find_element(By.ID, "price").send_keys(price)

    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys(weight)

    Select(driver.find_element(By.ID, "region")).select_by_value(region)
    Select(driver.find_element(By.ID, "shipping_type")).select_by_value(shipping_type)

    driver.find_element(By.ID, "calculate-btn").click()
