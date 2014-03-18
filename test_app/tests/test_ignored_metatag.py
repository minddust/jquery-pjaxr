from __future__ import unicode_literals

from selenium.common.exceptions import NoSuchElementException

from .helpers import SeleniumTestCase


class IgnoredMetatagTest(SeleniumTestCase):

    def test_ignored_metatag_pjaxr(self):
        self.browser_get_reverse('index')
        self.assertTitle('index-title')
        self.assertContent('index-content')

        ignored_metatag_link = self.browser.find_element_by_css_selector('#ignored-metatag-link')
        ignored_metatag_link.click()

        self.wait.until(lambda browser: browser.title == 'ignored-metatag-title')
        self.assertTitle('ignored-metatag-title')
        self.assertContent('ignored-metatag-content')

        self.assertBodyAttr('pjaxr-success', 'true')
        self.assertBodyAttr('pjaxr-done', 'true')

        # ignored metatags won't raise an error nor be processed - more: #12
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_css_selector('meta[http-equiv="X-UA-Compatible"]')

    def test_ignored_metatag_initial(self):
        self.browser_get_reverse('ignored_metatag')
        self.assertTitle('ignored-metatag-title')
        self.assertContent('ignored-metatag-content')

        # ignored metatags aren't affected by normal rendering
        self.browser.find_element_by_css_selector('meta[http-equiv="X-UA-Compatible"]')
