from __future__ import unicode_literals

from os import getenv

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support import ui


class SeleniumTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        if getenv('SAUCE_USERNAME'):
            cls.browser = cls.sauce_labs_driver()
        else:
            cls.browser = webdriver.Chrome()
        cls.wait = ui.WebDriverWait(cls.browser, 10)
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    @classmethod
    def sauce_labs_driver(cls):
        username = getenv('SAUCE_USERNAME')
        access_key = getenv('SAUCE_ACCESS_KEY')
        caps = {
            'platform': getenv('SELENIUM_PLATFORM'),
            'browserName': getenv('SELENIUM_BROWSER'),
            'version': getenv('SELENIUM_VERSION'),
            'javascriptEnabled': getenv('SELENIUM_JAVASCRIPT', True),
            'tunnel-identifier': getenv('TRAVIS_JOB_NUMBER'),
            'name': 'jquery-pjaxr',
            'build': getenv('TRAVIS_BUILD_NUMBER'),
        }
        hub_url = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'.format(username, access_key)
        return webdriver.Remote(desired_capabilities=caps, command_executor=str(hub_url))  # webdriver.Remote only accepts str - not unicode

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
