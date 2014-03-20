from __future__ import unicode_literals

from .helpers import SeleniumTestCase
from selenium.common.exceptions import NoSuchElementException


class PjaxrNoMatchingIDTest(SeleniumTestCase):

    def test_no_matching_id_pjaxr_request(self):
        self.browser_get_reverse('index')
        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

        no_matching_id_link = self.browser.find_element_by_css_selector('#no-matching-id-link')
        no_matching_id_link.click()

        self.wait.until(lambda browser: browser.title == 'no-matching-id-title')
        self.assertTitle('no-matching-id-title')
        self.assertContent('index-content')

        self.assertBodyAttr('pjaxr-click', 'true')
        self.assertBodyAttr('pjaxr-before-send', 'true')
        self.assertBodyAttr('pjaxr-send', 'true')
        self.assertBodyAttr('pjaxr-timeout', None)
        self.assertBodyAttr('pjaxr-start', 'true')
        self.assertBodyAttr('pjaxr-success', 'true')
        self.assertBodyAttr('pjaxr-done', 'true')
        self.assertBodyAttr('pjaxr-fail', None)
        self.assertBodyAttr('pjaxr-always', 'true')
        self.assertBodyAttr('pjaxr-end', 'true')

        self.resetBodyAttrs()

        self.assertBodyAttr('pjaxr-click', None)
        self.assertBodyAttr('pjaxr-before-send', None)
        self.assertBodyAttr('pjaxr-send', None)
        self.assertBodyAttr('pjaxr-timeout', None)
        self.assertBodyAttr('pjaxr-start', None)
        self.assertBodyAttr('pjaxr-success', None)
        self.assertBodyAttr('pjaxr-done', None)
        self.assertBodyAttr('pjaxr-fail', None)
        self.assertBodyAttr('pjaxr-always', None)
        self.assertBodyAttr('pjaxr-end', None)

        self.browser_go_back()

        self.wait.until(lambda browser: browser.title == 'index-title')
        self.assertTitle('index-title')
        self.assertContent('index-content')

    def test_no_matching_id_initial_request(self):
        self.browser_get_reverse('no_matching_id')
        self.assertTitle('no-matching-id-title')
        with self.assertRaises(NoSuchElementException):
            self.assertContent('no-matching-id-content')
        self.assertEqual(self.browser.find_element_by_id('12381z2dh10298ez1291').text, 'no-matching-id-content')
        self.assertBodyAttr('pjaxr-done', None)

        index_link = self.browser.find_element_by_css_selector('#index-link')
        index_link.click()

        self.wait.until(lambda browser: browser.title == 'index-title')
        self.assertTitle('index-title')
        with self.assertRaises(NoSuchElementException):
            self.assertContent('index-content')
        self.assertEqual(self.browser.find_element_by_id('12381z2dh10298ez1291').text, 'no-matching-id-content')

        self.assertBodyAttr('pjaxr-click', 'true')
        self.assertBodyAttr('pjaxr-before-send', 'true')
        self.assertBodyAttr('pjaxr-send', 'true')
        self.assertBodyAttr('pjaxr-timeout', None)
        self.assertBodyAttr('pjaxr-start', 'true')
        self.assertBodyAttr('pjaxr-success', 'true')
        self.assertBodyAttr('pjaxr-done', 'true')
        self.assertBodyAttr('pjaxr-fail', None)
        self.assertBodyAttr('pjaxr-always', 'true')
        self.assertBodyAttr('pjaxr-end', 'true')

        self.resetBodyAttrs()

        self.assertBodyAttr('pjaxr-click', None)
        self.assertBodyAttr('pjaxr-before-send', None)
        self.assertBodyAttr('pjaxr-send', None)
        self.assertBodyAttr('pjaxr-timeout', None)
        self.assertBodyAttr('pjaxr-start', None)
        self.assertBodyAttr('pjaxr-success', None)
        self.assertBodyAttr('pjaxr-done', None)
        self.assertBodyAttr('pjaxr-fail', None)
        self.assertBodyAttr('pjaxr-always', None)
        self.assertBodyAttr('pjaxr-end', None)

        self.browser_go_back()

        self.wait.until(lambda browser: browser.title == 'no-matching-id-title')
        self.assertTitle('no-matching-id-title')
        with self.assertRaises(NoSuchElementException):
            self.assertContent('no-matching-id-content')
        self.assertEqual(self.browser.find_element_by_id('12381z2dh10298ez1291').text, 'no-matching-id-content')
