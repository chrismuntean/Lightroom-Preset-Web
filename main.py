import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import dotenv
import time

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
if not EMAIL or not PASSWORD:
    raise EnvironmentError(
        "EMAIL and PASSWORD environment variables must be set for the login script"
    )
GeneralSleepTime = 5  # General sleep time to wait for elements to load - change if needed depending on your internet speed

driver = webdriver.Firefox()
driver.get("https://lightroom.adobe.com/signin")

# Wait up to 100 seconds for the email input to exist
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "EmailPage-EmailField")))
time.sleep(GeneralSleepTime)
driver.find_element(By.ID, "EmailPage-EmailField").send_keys(EMAIL)

# Click the "Continue" button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ntVziG_spectrum-Button")))
driver.find_element(By.CLASS_NAME, "ntVziG_spectrum-Button").click() # Click the "Continue" button to proceed (either goes to password or 2FA page)

# Check if the end or the URL contains "/challenge/verify/email" to determine if we need to handle 2FA
time.sleep(GeneralSleepTime)
fragment = driver.execute_script("return window.location.hash")
print("URL Fragment:", fragment)

if "challenge/verify/email" in fragment:
    print("2FA challenge detected via hash")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ntVziG_spectrum-BaseButton")))
    driver.find_element(By.CLASS_NAME, "ntVziG_spectrum-BaseButton").click()  # Click the "Send Code" button
else:
    print("No 2FA detected (hash doesn't match)")

# Wait up to 5 minutes for the password field to exist
WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "PasswordPage-PasswordField")))
driver.find_element(By.ID, "PasswordPage-PasswordField").send_keys(PASSWORD)

# Click the "Continue" button
passContinue_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ntVziG_spectrum-Button")))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", passContinue_btn)
passContinue_btn.click() # Click the "Continue" button to proceed
# driver.find_element(By.CLASS_NAME, "ntVziG_spectrum-Button").click() # Click the "Continue" button to complete the login process
