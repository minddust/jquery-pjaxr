from __future__ import unicode_literals

import base64
import httplib
import json
from os import getenv
import sys

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support import ui


class SeleniumTestCase(LiveServerTestCase):

    def setUp(self):
        if getenv('SAUCE_USERNAME'):
            self.browser = self.sauce_labs_driver()
        else:
            self.browser = webdriver.Chrome()
        self.wait = ui.WebDriverWait(self.browser, 10)
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        if hasattr(self, 'sauce_username'):
            self.report_status()
        self.browser.quit()
        super(SeleniumTestCase, self).tearDown()

    def sauce_labs_driver(self):
        self.sauce_username = getenv('SAUCE_USERNAME')
        self.sauce_access_key = getenv('SAUCE_ACCESS_KEY')
        self.sauce_auth = base64.encodestring('{0}:{1}'.format(self.sauce_username, self.sauce_access_key))[:-1]
        caps = {
            'platform': getenv('SELENIUM_PLATFORM'),
            'browserName': getenv('SELENIUM_BROWSER'),
            'version': getenv('SELENIUM_VERSION'),
            'javascriptEnabled': getenv('SELENIUM_JAVASCRIPT', True),
            'tunnel-identifier': getenv('TRAVIS_JOB_NUMBER'),
            'name': 'jquery-pjaxr-{}'.format(self._testMethodName),
            'build': getenv('TRAVIS_BUILD_NUMBER'),
        }
        hub_url = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'.format(self.sauce_username, self.sauce_access_key)
        return webdriver.Remote(desired_capabilities=caps, command_executor=str(hub_url))  # webdriver.Remote only accepts str - not unicode

    def report_status(self):
        info = sys.exc_info()
        passed = info[0] is None

        url = '/rest/v1/{0}/jobs/{1}'.format(self.sauce_username, self.browser.session_id)
        data = {'passed': passed}
        headers = {'Authorization': 'Basic {0}'.format(self.sauce_auth)}

        connection = httplib.HTTPConnection('saucelabs.com')
        connection.request('PUT', url, json.dumps(data), headers)
        result = connection.getresponse()
        return result.status == 200

    def assertTitle(self, title):
        self.assertEqual(self.browser.title, title)

    def assertContent(self, content):
        c = self.browser.find_element_by_css_selector('#content').text
        self.assertEqual(c, content)

    def assertBodyNamespace(self, namespace):
        body = self.browser.find_element_by_css_selector('body')
        body_attr = body.get_attribute('data-pjaxr-namespace')
        self.assertEqual(body_attr, namespace)

    def assertCurrentNamespace(self, namespace):
        self.browser.execute_script("$('body').attr('data-selenium-pjaxr-current-namespace', $.fn.pjaxr.state.namespace);")
        self.assertBodyAttr('pjaxr-current-namespace', namespace)

    def assertBodyAttr(self, attribute, value):
        body = self.browser.find_element_by_css_selector('body')
        body_attr = body.get_attribute('data-selenium-' + attribute)
        self.assertEqual(body_attr, value)

    def resetBodyAttrs(self):
        self.browser.execute_script('$("body").removeAttrs(/^data-selenium-/);')
