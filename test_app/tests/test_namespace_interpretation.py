from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class NamespaceInterpretationTest(SeleniumTestCase):

    def test_namespaces_after_pjaxr(self):
        self.browser_get_reverse('index')
        self.assert_title('index-title')
        self.assert_content('index-content')
        self.assert_body_namespace('md.index')

        about_link = self.browser.find_element_by_css_selector('#about-link')
        about_link.click()

        self.wait.until(lambda browser: browser.title == 'about-title')
        self.assert_title('about-title')
        self.assert_content('about-content')
        self.assert_current_namespace('md.about')

        project_link = self.browser.find_element_by_css_selector('#project-link')
        project_link.click()

        self.wait.until(lambda browser: browser.title == 'project-title')
        self.assert_title('project-title')
        self.assert_content('project-content')
        self.assert_current_namespace('md.project.index')  # multiline namespace - prove for #24
