from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class PjaxrRequestTest(SeleniumTestCase):

    def setUp(self):
        super(PjaxrRequestTest, self).setUp()
        self.browser.get('{}/'.format(self.live_server_url))

    def test_pjaxr_request_index(self):
        self.assertTitle('index-title')
        self.assertContent('index-content')

        body = self.browser.find_element_by_css_selector('body')
        body_pjaxr = body.get_attribute('js-pjaxr-done')
        self.assertEqual(body_pjaxr, None)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')

        self.assertBodyAttr('js-pjaxr-click', 'true')
        self.assertBodyAttr('js-pjaxr-before-send', 'true')
        self.assertBodyAttr('js-pjaxr-send', 'true')
        self.assertBodyAttr('js-pjaxr-timeout', None)
        self.assertBodyAttr('js-pjaxr-start', 'true')
        self.assertBodyAttr('js-pjaxr-success', 'true')
        self.assertBodyAttr('js-pjaxr-done', 'true')
        self.assertBodyAttr('js-pjaxr-fail', None)
        self.assertBodyAttr('js-pjaxr-always', 'true')
        self.assertBodyAttr('js-pjaxr-end', 'true')

        self.resetBodyAttrs()

        self.assertBodyAttr('js-pjaxr-click', None)
        self.assertBodyAttr('js-pjaxr-before-send', None)
        self.assertBodyAttr('js-pjaxr-send', None)
        self.assertBodyAttr('js-pjaxr-timeout', None)
        self.assertBodyAttr('js-pjaxr-start', None)
        self.assertBodyAttr('js-pjaxr-success', None)
        self.assertBodyAttr('js-pjaxr-done', None)
        self.assertBodyAttr('js-pjaxr-fail', None)
        self.assertBodyAttr('js-pjaxr-always', None)
        self.assertBodyAttr('js-pjaxr-end', None)
