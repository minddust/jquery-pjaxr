from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class NamespaceInterpretationTest(SeleniumTestCase):

    def setUp(self):
        super(NamespaceInterpretationTest, self).setUp()
        self.browser.get('{}/'.format(self.live_server_url))

    def test_namespaces_after_pjaxr(self):
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

        self.browser.execute_script("$('body').attr('data-current-namespace', $.fn.pjaxr.state.namespace);")
        self.assertBodyAttr('data-current-namespace', 'md.about')

        project_link = self.browser.find_element_by_css_selector('#project-link')
        project_link.click()

        self.wait.until(lambda browser: browser.title == 'project-title')
        self.assertTitle('project-title')
        self.assertContent('project-content')

        self.browser.execute_script("$('body').attr('data-current-namespace', $.fn.pjaxr.state.namespace);")
        self.assertBodyAttr('data-current-namespace', 'md.project.index')
