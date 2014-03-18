from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from .helpers import SeleniumTestCase


class PjaxrReadyPjaxrAlwaysTest(SeleniumTestCase):

    def setUp(self):
        super(PjaxrReadyPjaxrAlwaysTest, self).setUp()
        self.browser.get('{}/'.format(self.live_server_url))

    def test_pjaxr_ready_pjaxr_always(self):

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

        self.browser.get('{0}{1}'.format(self.live_server_url, reverse('pjaxr_ready_pjaxr_always')))

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 1)
        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-ready-div')) == 1)

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 2)
        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-ready-div')), 1)

    def test_disabled_pjaxr(self):

        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-always-div')), 0)
        self.assertEqual(len(self.browser.find_elements_by_class_name('pjaxr-ready-div')), 0)
        self.browser.execute_script('$.fn.pjaxr.disable();')

        self.browser.get('{0}{1}'.format(self.live_server_url, reverse('pjaxr_ready_pjaxr_always_disabled', kwargs={'disabled': 'true'})))

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 1)
        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-ready-div')) == 1)

        self.browser.get('{0}{1}'.format(self.live_server_url, reverse('about')))

        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-always-div')) == 0)
        self.wait.until(lambda browser: len(browser.find_elements_by_class_name('pjaxr-ready-div')) == 0)