import time
import logging

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@dataclass(frozen=True)
class Data:
  hotIp: str = "192.168.1.1"

class HotClient:
  def __init__(self) -> None:
    options = ChromeOptions()
    options.add_argument('headless')
    # Create a new instance of the Chrome driver
    self.driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Open the website and wait for it to load
    self.driver.get(f"http://{Data.hotIp}/")
    self.wait = WebDriverWait(self.driver, 10)

  def __login__(self):
    # Find the username and password fields and fill them in
    logging.info("Logging in the site...")
    credentials: dict = {
      "username" : self.wait.until(EC.presence_of_element_located((By.NAME, "loginUsername"))),
      "password" : self.driver.find_element(By.NAME, "loginPassword")
    }
    for cred in credentials.values():
      cred.send_keys("admin")
    # Find the login button and click it
    login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
    login_button.click()
    logging.info("Successfully logged in")

  def open_basic_tab(self):
    logging.info("Opening basic tab...")
    # Find the "Basic" tab and click it
    basic_tab = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Basic')))
    basic_tab.click()
    logging.info("Successfully opened basic tab")

  def __reboot__(self):
    logging.info("Rebooting router...")
    # Find the "Reboot" button and click it
    reboot_button = self.driver.find_element(By.XPATH, "//input[@value='Reboot']")
    reboot_button.click()
    self.switch_to_alert()

  def switch_to_alert(self):
    # Wait for the alert to be displayed and accept it
    self.wait.until(EC.alert_is_present())
    alert = self.driver.switch_to.alert
    # Press the OK button
    alert.accept()
    logging.info("Successfully rebooted")

  def main(self):
    self.__login__()
    self.open_basic_tab()
    self.__reboot__()
    time.sleep(5)
    self.driver.quit()

if __name__ == "__main__":
  HotClient().main()
