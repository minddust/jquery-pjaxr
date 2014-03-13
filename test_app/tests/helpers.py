from __future__ import unicode_literals

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support import ui


class SeleniumTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()
        cls.wait = ui.WebDriverWait(cls.browser, 10)
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def assertTitle(self, title):
        self.assertEqual(self.browser.title, title)

    def assertContent(self, content):
        c = self.browser.find_element_by_css_selector('#content').text
        self.assertEqual(c, content)

    def assertBodyAttr(self, attribute, value):
        body = self.browser.find_element_by_css_selector('body')
        body_attr = body.get_attribute(attribute)
        self.assertEqual(body_attr, value)

    def resetBodyAttrs(self):
        self.browser.execute_script('$("body").removeAttrs(/^js-pjaxr-/);')
