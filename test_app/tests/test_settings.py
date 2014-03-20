from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class PjaxrSettingsTest(SeleniumTestCase):

    def test_settings_after_initial_request(self):
        self.browser_get_reverse('index')
        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

        self.browser_get_reverse('settings')
        self.wait.until(lambda browser: browser.title == 'settings-title')
        self.assertTitle('settings-title')
        self.assertContent('settings-content')
        self.assertBodyAttr('pjaxr-done', None)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')

        self.browser.execute_script('$("body").attr("data-selenium-window-scrollTop", $(window).scrollTop());')
        self.assertEqual(self.browser.find_element_by_tag_name('body').get_attribute('data-selenium-window-scrollTop'), str(10))

        self.browser_go_back()

        # should go to index, because about was only replacing settings
        self.assert_url_reverse('index')

        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

    def test_settings_after_pjaxr_request(self):
        self.browser_get_reverse('index')
        self.assertTitle('index-title')
        self.assertContent('index-content')
        self.assertBodyAttr('pjaxr-done', None)

        settings_link = self.browser.find_element_by_css_selector('#settings-link')
        settings_link.click()

        self.wait.until(lambda browser: browser.title == 'settings-title')
        self.assertTitle('settings-title')
        self.assertContent('settings-content')
        self.assertBodyAttr('pjaxr-done', 'true')

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assertTitle('about-title')
        self.assertContent('about-content')

        self.browser.execute_script('$("body").attr("data-selenium-window-scrollTop", $(window).scrollTop());')
        self.assertEqual(self.browser.find_element_by_tag_name('body').get_attribute('data-selenium-window-scrollTop'), str(10))

        self.browser_go_back()

        # should go to index, because about was only replacing settings
        self.assert_url_reverse('index')

        self.assertTitle('index-title')
        self.assertContent('index-content')
