from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class NoPjaxrResponseTest(SeleniumTestCase):

    def setUp(self):
        super(NoPjaxrResponseTest, self).setUp()
        self.browser.get('{}/'.format(self.live_server_url))

    def test_no_pjaxr_response(self):
        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

        # pjaxr request - depth 1
        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')
        self.assertBodyAttr('pjaxr-done', 'true')

        self.resetBodyAttrs()
        self.assertBodyAttr('pjaxr-done', None)

        # no-pjaxr-response request - returns full page markup
        no_pjaxr_response_link = self.browser.find_element_by_css_selector('#no-pjaxr-response-link')
        no_pjaxr_response_link.click()

        self.wait.until(lambda browser: browser.title == 'no-pjaxr-response-title')
        self.assertTitle('no-pjaxr-response-title')
        self.assertContent('no-pjaxr-response-content')
        self.assertBodyAttr('pjaxr-done', None)

        # back should trigger a full request cause namespace and blocks can't be reconstructed after a full return
        # issue: #17
        self.browser.back()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')
        self.assertBodyAttr('pjaxr-done', None)
