import os
import platform

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from sendEmail import send_to_me


class TlsChecker:
    def __init__(self, user_email, user_password, target_emails):
        self.driver = self.initiate_driver()
        self.user_email = user_email
        self.user_password = user_password
        self.target_emails = target_emails

    def initiate_driver(self):

        # disabling cookies
        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.cookie.cookieBehavior", 2)

        firefox_options = Options()
        firefox_options.add_argument("-headless")
        current_directory = os.getcwd()
        return webdriver.Firefox(executable_path=current_directory + '/drivers/' + self.get_os(), options=firefox_options, firefox_profile=fp)

    def login(self):
        if 'myapp' in self.driver.current_url:
            print('refresh')
            self.driver.refresh()
            return True
        else:
            self.driver.get('https://de-legalization.tlscontact.com/eg/CAI/login.php')

            email = self.driver.find_element_by_id("email")
            email.clear()
            email.send_keys(self.user_email)

            passwd = self.driver.find_element_by_id('pwd')
            passwd.clear()
            passwd.send_keys(self.user_password)

            self.driver.find_element_by_class_name("submit").click()

            delay = 5  # seconds
            time.sleep(delay)

            if 'myapp' in self.driver.current_url:
                print('Login Successful')
                return True

            else:
                print('Login Unuccessful !!')
                return False

    def is_an_appointment_free(self):
        table = self.driver.find_element_by_id('timeTable')
        table_content = BeautifulSoup(table.get_attribute('innerHTML'), features="html.parser")

        days = table_content.find_all("a")
        for day in days:
            if day.has_attr('href'):
                print('Appointment found')
                return True

        print('No appointments found')
        return False

    def check(self, loggedIn):
        try:
            if loggedIn and self.is_an_appointment_free():
                title = 'TLS Appointment is free'
                message = 'Luke, Iam your father ... U have to go there now => https://de-legalization.tlscontact.com/eg/CAI/login.php'
                send_to_me(message, title, self.target_emails)
                return True

        except Exception as e:
            message = str(e)
            print(message)
            # send_to_me(message, title)

    def get_os(self):
        uname = platform.uname()
        driver_name = 'geckodriver'
        if uname.system == 'Darwin':
            driver_name += '_macos'

        if uname.system == 'Linux':
            driver_name += '_linux'

        if uname.system == 'Windows':
            driver_name += '_win'

            if uname.machine == 'x86_64':
                driver_name += '64.exe'
            else:
                driver_name += '32.exe'

        return driver_name

    def terminate(self):
        self.driver.quit()
