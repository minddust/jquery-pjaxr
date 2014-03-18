from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class PjaxrReadyPjaxrAlwaysTest(SeleniumTestCase):

    def test_pjaxr_ready_pjaxr_always(self):
        self.browser_get_reverse('index')

        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-always-div')), 0)
        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-ready-div')), 0)

        pjaxr_ready_pjaxr_always_link = self.browser.find_element_by_css_selector('#pjaxr-ready-pjaxr-always-link')
        pjaxr_ready_pjaxr_always_link.click()

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 1)
        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-ready-div')) == 1)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 2)
        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-ready-div')), 1)

        project_link = self.browser.find_element_by_css_selector('#project-link')
        project_link.click()

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 3)
        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-ready-div')), 1)

        self.browser_get_reverse('pjaxr_ready_pjaxr_always')

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 1)
        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-ready-div')) == 1)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 2)
        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-ready-div')), 1)

    def test_disabled_pjaxr(self):
        self.browser_get_reverse('index')

        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-always-div')), 0)
        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-ready-div')), 0)
        self.browser.execute_script('$.fn.pjaxr.disable();')

        self.browser_get_reverse('pjaxr_ready_pjaxr_always', pjaxr_state='disabled')

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 1)
        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-ready-div')) == 1)

        self.browser_get_reverse('about')

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 0)
        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-ready-div')) == 0)
