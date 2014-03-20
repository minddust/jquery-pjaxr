from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from .helpers import SeleniumTestCase
from selenium.common.exceptions import NoSuchElementException


class PjaxrRequestTest(SeleniumTestCase):

    def test_pjaxr_request_depth_1(self):
        self.browser_get_reverse('index')
        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

        self.browser.find_element_by_class_name('wanna_be_removed_2')
        self.assertEqual(self.browser.find_element_by_class_name('wanna_be_removed').text, 'wanna_be_removed')

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')
        keywords_metatag = self.browser.find_element_by_css_selector('meta[name="keywords"]')
        self.assertEqual(keywords_metatag.get_attribute("content"), "This is a test")

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_class_name('wanna_be_removed_2')
        with self.assertRaises(NoSuchElementException):
            self.assertEqual(self.browser.find_element_by_class_name('wanna_be_removed').text, 'wanna_be_removed')

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

    def test_pjaxr_request_javascript(self):
        self.browser_get_reverse('index')
        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

        self.browser.find_element_by_class_name('wanna_be_removed_2')
        self.assertEqual(self.browser.find_element_by_class_name('wanna_be_removed').text, 'wanna_be_removed')

        self.browser.execute_script("$(document).pjaxr.request('{0}')".format(reverse('about')))

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')
        keywords_metatag = self.browser.find_element_by_css_selector('meta[name="keywords"]')
        self.assertEqual(keywords_metatag.get_attribute("content"), "This is a test")

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_class_name('wanna_be_removed_2')
        with self.assertRaises(NoSuchElementException):
            self.assertEqual(self.browser.find_element_by_class_name('wanna_be_removed').text, 'wanna_be_removed')

        self.assertBodyAttr('pjaxr-click', None)
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

    def test_pjaxr_request_depth_2_to_no_pjaxr_and_back(self):
        self.browser_get_reverse('index')
        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')

        self.assertBodyAttr('pjaxr-done', 'true')
        self.resetBodyAttrs()
        self.assertBodyAttr('pjaxr-done', None)

        project_link = self.browser.find_element_by_css_selector('#project-link')
        project_link.click()

        self.wait.until(lambda browser: browser.title == 'project-title')
        self.assertTitle('project-title')
        self.assertContent('project-content')

        self.assertBodyAttr('pjaxr-done', 'true')
        self.resetBodyAttrs()
        self.assertBodyAttr('pjaxr-done', None)

        no_pjaxr_response_link = self.browser.find_element_by_css_selector('#no-pjaxr-response-link')
        no_pjaxr_response_link.click()

        self.wait.until(lambda browser: browser.title == 'no-pjaxr-response-title')
        self.assertTitle('no-pjaxr-response-title')
        self.assertContent('no-pjaxr-response-content')
        self.assertBodyAttr('pjaxr-done', None)

        self.browser_go_back()

        # On Chrome/Webkit caching will return the content out of the pjaxr xhr-response, not a new initial content.
        # fix #16
        self.wait.until(lambda browser: browser.find_element_by_css_selector('#site'))

        self.wait.until(lambda browser: browser.title == 'project-title')
        self.assertTitle('project-title')
        self.assertContent('project-content')
        self.assertBodyAttr('pjaxr-done', None)
