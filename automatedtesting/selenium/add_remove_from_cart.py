# #!/usr/bin/env python
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import logging
import os

# Start the browser and login with standard_user
def add_remove_from_cart (user, password):
    logger = get_logger()
    output_file = open("selenium-output.txt", "w")

    save_message (logger, output_file, 'Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Firefox()
    save_message (logger, output_file, 'Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')

    # Login test
    save_message (logger, output_file, 'Login')
    driver.find_element(By.CSS_SELECTOR, "input[id='user-name']").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "input[id='password']").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    save_message (logger, output_file, 'Check login worked')
    assert 'inventory' in driver.current_url
    save_message(logger, output_file, "User " + user + " is logged in")

    # Shopping tests
    # Add product to cart should update cart counter
    save_message (logger, output_file, 'Add Backpack to cart')
    driver.find_element(By.CSS_SELECTOR, "button[id='add-to-cart-sauce-labs-backpack']").click()
    save_message (logger, output_file, 'Check Cart counter is updated')
    counter_cart = driver.find_element(By.CSS_SELECTOR, "div[id='shopping_cart_container'] > a > span").text
    assert counter_cart == '1'

    # Check remove button is present
    save_message (logger, output_file, 'Check Remove button is shown')
    assert_element_exists(driver, "button[id='remove-sauce-labs-backpack']", 1)

    save_message (logger, output_file, 'Check Add button is not shown')
    assert_element_exists(driver, "button[id='add-sauce-labs-backpack']", 0)

    # Correct product was added in cart
    product_title = driver.find_element(By.CSS_SELECTOR, "a[id='item_4_title_link'] > div").text
    save_message (logger, output_file, 'Go to cart')
    driver.find_element(By.CSS_SELECTOR, "div[id='shopping_cart_container']").click()
    assert 'cart.html' in driver.current_url
    save_message (logger, output_file, 'Assert correct product displayed')
    assert product_title == driver.find_element(By.CSS_SELECTOR, "a[id='item_4_title_link'] > div").text
    save_message (logger, output_file, 'Assert buttons are present')
    assert_element_exists(driver, "button[id='remove-sauce-labs-backpack']", 1)
    assert_element_exists(driver, "button[id='continue-shopping']", 1)
    assert_element_exists(driver, "button[id='checkout']", 1)

    # Remove product
    save_message (logger, output_file, "Remove Backpack product")
    driver.find_element(By.CSS_SELECTOR, "button[id='remove-sauce-labs-backpack']").click()
    assert_element_exists(driver, "div[id='shopping_cart_container'] > a > span", 0)
    assert_element_exists(driver, "div[class='cart_list'] > .cart_item", 0)

    #Return to shopping
    save_message (logger, output_file, 'Return to shopping')
    driver.find_element(By.CSS_SELECTOR, "button[id='continue-shopping']").click()
    assert 'inventory' in driver.current_url
    save_message (logger, output_file, 'Add Backpack to cart')
    driver.find_element(By.CSS_SELECTOR, "button[id='add-to-cart-sauce-labs-backpack']").click()
    save_message (logger, output_file, 'Check Remove button is shown')
    assert_element_exists(driver, "button[id='remove-sauce-labs-backpack']", 1)
    save_message (logger, output_file, 'Remove Backpack product')
    driver.find_element(By.CSS_SELECTOR, "button[id='remove-sauce-labs-backpack']").click()
    save_message (logger, output_file, 'Check shopping cart counter is not present')
    assert_element_exists(driver, "div[id='shopping_cart_container'] > a > span", 0)

    save_message(logger, output_file, 'Add 6 items to the cart')
    items = ['sauce-labs-backpack','sauce-labs-bike-light','sauce-labs-bolt-t-shirt','sauce-labs-fleece-jacket','sauce-labs-onesie','test.allthethings()-t-shirt-(red)']
    for item in items:
        save_message(logger, output_file, "Add " + item)
        driver.find_element(By.CSS_SELECTOR, "button[id='add-to-cart-" + item + "']").click()
    save_message(logger, output_file, "Check Shopping Card Counter shows 6 items")
    counter_cart = driver.find_element(By.CSS_SELECTOR, "div[id='shopping_cart_container'] > a > span").text
    assert counter_cart == '6'

    save_message(logger, output_file, 'Remove the 6 items from the cart')
    for item in items:
        save_message(logger, output_file, "Remove " + item)
        driver.find_element(By.CSS_SELECTOR, "button[id='remove-" + item + "']").click()
    save_message(logger, output_file, "Check Shopping Card Counter is not present")
    assert_element_exists(driver, "div[id='shopping_cart_container'] > a > span", 0)

    save_message (logger, output_file, 'All tests have passed!')
    output_file.close()

def assert_element_exists(driver, selector, expect_exists):
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
        exists = 1
    except NoSuchElementException:
        exists = 0
    assert expect_exists == exists

def get_logger():
    if os.path.exists("selenium.log"):
        os.remove("selenium.log")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    f_handler = logging.FileHandler('./selenium.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")

    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)

    return logger

def save_message(logger, file, message):
    logger.info(message)
    file.write(message + "\r")

add_remove_from_cart('standard_user', 'secret_sauce')

