from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

MAX_WAIT = 15  # 15 seconds is too long for a client to wait for a page to load
POLLING_RATE = 0.1  # Check webpage no more often than every 0.1 seconds

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def send_keys_and_wait_for_refresh(self, element, keys):
        element.send_keys(keys)
        self.wait_for_page_refresh(element)

    def wait_for_page_refresh(self, element_going_stale):
        exceptions = [WebDriverException]
        WebDriverWait(self.browser, MAX_WAIT, POLLING_RATE, exceptions).until(
            EC.staleness_of(element_going_stale)
        )

    def wait_for_row_in_list_table(self, row_text):
        exceptions = [WebDriverException]
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
        self.send_keys_and_wait_for_refresh(inputbox, Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Text box must allow another entry

        # Enter "Use peacock feathers to make a fly
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        self.send_keys_and_wait_for_refresh(inputbox, Keys.ENTER)

        # Page update, with both items
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Test complete

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User A starts a to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        self.send_keys_and_wait_for_refresh(inputbox, Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # The list has a unique URL
        list_url_a = self.browser.current_url
        self.assertRegex(list_url_a, '/lists/.+')

        # Clean state
        self.browser.delete_all_cookies()
        
        # User B starts a new list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Enter a new item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        self.send_keys_and_wait_for_refresh(inputbox, Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Hey look! A new URL!
        list_url_b = self.browser.current_url
        self.assertRegex(list_url_a, '/lists/.+')
        self.assertNotEqual(list_url_a, list_url_b)

        # Check again
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Test complete

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        # In this example, the browser window is a fixed size
        width = 1024
        height = 768
        self.browser.set_window_size(width, height)

        # Check that the input box is centered
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            width / 2,
            delta=10
        )

        # Start a new list and check if centered
        inputbox.send_keys('testing')
        self.send_keys_and_wait_for_refresh(inputbox, Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            width / 2,
            delta=10
        )
