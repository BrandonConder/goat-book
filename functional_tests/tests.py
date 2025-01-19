from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

MAX_WAIT = 15  # 15 seconds is too long for a client to wait for a page to load
POLLING_RATE = 0.5  # Check webpage no more often than every 0.5 seconds

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        exceptions = [WebDriverException]  # I've left off AssertionError as it wouldn't apply here. Is this a mistake?
        table = WebDriverWait(self.browser, MAX_WAIT, POLLING_RATE, exceptions).until(
            EC.presence_of_element_located((By.ID, 'id_list_table'))
        )
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])        

    def test_can_start_a_todo_list(self):
        # Let's check on our to-do list
        self.browser.get(self.live_server_url)

        # The header tells us we're in the to-do application
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Enter a to-do item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # 1. Buy peacock feathers
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Text box must allow another entry

        # Enter "Use peacock feathers to make a fly
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Page update, with both items
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Test complete