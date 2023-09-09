# In order to use this test a set of preconditions has to be met:
# 1. Application is running at localhost:5888
# 2. selenium is installed (pip install selenium)
# 3. Proper versions of browser drivers are copied to /usr/bin
# (or other appropriate directory) and have permission to execute
# 4. Test is launched with python selenium_test_dl.py browser_letter
# where browser_letter is one of the following: [f, c, o]

import unittest
import sys

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

browsers = {"f": "Firefox", "c": "Chrome", "o": "Opera"}
browser = browsers.get(sys.argv.pop(1))
if browser is None:
    sys.exit("Invalid browser selected")
elif browser == "Firefox":
    from selenium.webdriver.firefox.options import Options
elif browser == "Chrome":
    from selenium.webdriver.chrome.options import Options
elif browser == "Opera":
    from selenium.webdriver.opera.options import Options

print("browser is %s" % browser)

jq_url = "https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"


class DownloadTest(unittest.TestCase):

    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=dP15zlyra3c"
        options = Options()
        if browser == "Firefox":
            self.browser = webdriver.Firefox(options=options)
        elif browser == "Chrome":
            self.browser = webdriver.Chrome(options=options)
        elif browser == "Opera":
            self.browser = webdriver.Opera(options=options)

        self.jquery = requests.get(jq_url).text

    def test_task_submission_success(self):
        self.browser.get("http://localhost:5888/")
        self.assertIn("Index page", self.browser.title)
        input_url = self.browser.find_element(By.NAME, "url")
        input_url.send_keys(self.url)
        select = Select(self.browser.find_element(By.NAME, "format"))
        select.select_by_value('mp4')
        input_url.submit()
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("task_id", body.text)

    def test_task_submission_error(self):
        self.browser.get("http://localhost:5888/")
        self.assertIn("Index page", self.browser.title)
        input_url = self.browser.find_element(By.NAME, "url")
        input_url.submit()
        WebDriverWait(self.browser, 2).until(EC.title_contains("Server error"))

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
