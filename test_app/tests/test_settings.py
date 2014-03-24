from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class PjaxrSettingsTest(SeleniumTestCase):

    def test_settings_after_initial_request(self):
        self.browser_get_reverse('index')
        self.assert_title('index-title')
        self.assert_content('index-content')
        self.assert_body_attr('pjaxr-done', None)

        self.browser_get_reverse('settings')
        self.wait.until(lambda browser: browser.title == 'settings-title')
        self.assert_title('settings-title')
        self.assert_content('settings-content')
        self.assert_body_attr('pjaxr-done', None)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assert_title('about-title')
        self.assert_content('about-content')
        self.assert_body_attr('pjaxr-done', 'true')

        self.reset_body_attrs()
        self.assert_body_attr('pjaxr-done', None)

        self.browser.execute_script('$("body").attr("data-selenium-window-scrollTop", $(window).scrollTop());')
        self.assertEqual(self.browser.find_element_by_tag_name('body').get_attribute('data-selenium-window-scrollTop'), str(10))

        self.browser_go_back()

        # should go to index, because about was only replacing settings
        self.assert_current_url('index')

        self.assert_title('index-title')
        self.assert_content('index-content')
        self.assert_body_attr('pjaxr-done', None)

    def test_settings_after_pjaxr_request(self):
        self.browser_get_reverse('index')
        self.assert_title('index-title')
        self.assert_content('index-content')
        self.assert_body_attr('pjaxr-done', None)

        settings_link = self.browser.find_element_by_css_selector('#settings-link')
        settings_link.click()

        self.wait.until(lambda browser: browser.title == 'settings-title')
        self.assert_title('settings-title')
        self.assert_content('settings-content')
        self.assert_body_attr('pjaxr-done', 'true')

        self.reset_body_attrs()
        self.assert_body_attr('pjaxr-done', None)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assert_title('about-title')
        self.assert_content('about-content')

        self.reset_body_attrs()
        self.assert_body_attr('pjaxr-done', None)

        self.browser.execute_script('$("body").attr("data-selenium-window-scrollTop", $(window).scrollTop());')
        self.assertEqual(self.browser.find_element_by_tag_name('body').get_attribute('data-selenium-window-scrollTop'), str(10))

        self.browser_go_back()

        # should go to index, because about was only replacing settings
        self.assert_current_url('index')

        self.assert_title('index-title')
        self.assert_content('index-content')
        self.assert_body_attr('pjaxr-done', None)
