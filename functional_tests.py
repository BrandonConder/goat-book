import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Let's check on our to-do list
        self.browser.get('http://localhost:8000')

        # The header tells us we're in the to-do application
        self.assertIn('To-Do', self.browser.title)

        # Enter a to-do item
        # 1. Buy peacock feathers

        # Text box must allo another entry
        # Enter "Use peacock feathers to make a fly

        # Page update, with both items

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
