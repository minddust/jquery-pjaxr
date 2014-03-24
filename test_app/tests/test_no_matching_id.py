from __future__ import unicode_literals

from selenium.common.exceptions import NoSuchElementException

from .helpers import SeleniumTestCase


class PjaxrNoMatchingIDTest(SeleniumTestCase):

    def test_no_matching_id_pjaxr_request(self):
        self.browser_get_reverse('index')
        self.assert_title('index-title')
        self.assert_content('index-content')
        self.assert_body_attr('pjaxr-done', None)

        no_matching_id_link = self.browser.find_element_by_css_selector('#no-matching-id-link')
        no_matching_id_link.click()

        self.wait.until(lambda browser: browser.title == 'no-matching-id-title')
        self.assert_title('no-matching-id-title')
        self.assert_content('index-content')  # container not found --> not applied

        self.assert_body_attr('pjaxr-click', 'true')
        self.assert_body_attr('pjaxr-before-send', 'true')
        self.assert_body_attr('pjaxr-send', 'true')
        self.assert_body_attr('pjaxr-timeout', None)
        self.assert_body_attr('pjaxr-start', 'true')
        self.assert_body_attr('pjaxr-success', 'true')
        self.assert_body_attr('pjaxr-done', 'true')
        self.assert_body_attr('pjaxr-fail', None)
        self.assert_body_attr('pjaxr-always', 'true')
        self.assert_body_attr('pjaxr-end', 'true')

        self.reset_body_attrs()

        self.assert_body_attr('pjaxr-click', None)
        self.assert_body_attr('pjaxr-before-send', None)
        self.assert_body_attr('pjaxr-send', None)
        self.assert_body_attr('pjaxr-timeout', None)
        self.assert_body_attr('pjaxr-start', None)
        self.assert_body_attr('pjaxr-success', None)
        self.assert_body_attr('pjaxr-done', None)
        self.assert_body_attr('pjaxr-fail', None)
        self.assert_body_attr('pjaxr-always', None)
        self.assert_body_attr('pjaxr-end', None)

        self.browser_go_back()

        self.wait.until(lambda browser: browser.title == 'index-title')
        self.assert_title('index-title')
        self.assert_content('index-content')

    def test_no_matching_id_initial_request(self):
        self.browser_get_reverse('no_matching_id')
        self.assert_title('no-matching-id-title')
        with self.assertRaises(NoSuchElementException):
            self.assert_content('no-matching-id-content')
        self.assertEqual(self.browser.find_element_by_id('not-matching-456').text, 'no-matching-id-content')
        self.assert_body_attr('pjaxr-done', None)

        index_link = self.browser.find_element_by_css_selector('#index-link')
        index_link.click()

        self.wait.until(lambda browser: browser.title == 'index-title')
        self.assert_title('index-title')
        with self.assertRaises(NoSuchElementException):
            self.assert_content('index-content')
        self.assertEqual(self.browser.find_element_by_id('not-matching-456').text, 'no-matching-id-content')

        self.assert_body_attr('pjaxr-click', 'true')
        self.assert_body_attr('pjaxr-before-send', 'true')
        self.assert_body_attr('pjaxr-send', 'true')
        self.assert_body_attr('pjaxr-timeout', None)
        self.assert_body_attr('pjaxr-start', 'true')
        self.assert_body_attr('pjaxr-success', 'true')
        self.assert_body_attr('pjaxr-done', 'true')
        self.assert_body_attr('pjaxr-fail', None)
        self.assert_body_attr('pjaxr-always', 'true')
        self.assert_body_attr('pjaxr-end', 'true')

        self.reset_body_attrs()

        self.assert_body_attr('pjaxr-click', None)
        self.assert_body_attr('pjaxr-before-send', None)
        self.assert_body_attr('pjaxr-send', None)
        self.assert_body_attr('pjaxr-timeout', None)
        self.assert_body_attr('pjaxr-start', None)
        self.assert_body_attr('pjaxr-success', None)
        self.assert_body_attr('pjaxr-done', None)
        self.assert_body_attr('pjaxr-fail', None)
        self.assert_body_attr('pjaxr-always', None)
        self.assert_body_attr('pjaxr-end', None)

        self.browser_go_back()

        self.wait.until(lambda browser: browser.title == 'no-matching-id-title')
        self.assert_title('no-matching-id-title')
        with self.assertRaises(NoSuchElementException):
            self.assert_content('no-matching-id-content')
        self.assertEqual(self.browser.find_element_by_id('not-matching-456').text, 'no-matching-id-content')
