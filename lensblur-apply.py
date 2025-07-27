import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import dotenv
import time

driver = webdriver.Firefox()
driver.get("https://lightroom.adobe.com/signin")


# First open the Filmstrip to see the number of total photos
# Get this by aria-label="Show filmstrip"
filmstrip_button = WebDriverWait(driver, 600).until(
    EC.element_to_be_clickable((By.XPATH, "//sp-action-button[@aria-label='Show filmstrip']"))
)
filmstrip_button.click()

# Then open the edit panel to see the options
# Get this by aria-label="Edit"
edit_button = WebDriverWait(driver, 600).until(
    EC.element_to_be_clickable((By.XPATH, "//sp-action-button[@aria-label='Edit']"))
)
edit_button.click()

while True:
    # Wait for 10 seconds until the class Checkbox-ZWrGvMdAjlkjKK7Q is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Checkbox-ZWrGvMdAjlkjKK7Q"))
    )

    # Find the first checkbox and check it's state 
    checkbox = driver.find_element(By.CLASS_NAME, "Checkbox-ZWrGvMdAjlkjKK7Q")
    if not checkbox.is_selected():
        # Click the checkbox via JavaScript to ensure it works even if the checkbox is not scrolled into view
        driver.execute_script("arguments[0].click();", checkbox)

    # The checkbox should then temporarily have the attribute disabled="disabled" wait for it to be removed
    WebDriverWait(driver, 600).until(
        EC.staleness_of(checkbox)
    )

    # Print the inner-html content of FlagRatingControl-zwIxfDzsuL8sYBva
    flag_rating_control = driver.find_element(By.CLASS_NAME, "FlagRatingControl-zwIxfDzsuL8sYBva")
    print(flag_rating_control.get_attribute("innerHTML"))

    # Press the right arrow key button to continue to the next photo
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ARROW_RIGHT)