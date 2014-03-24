from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class InitialRequestTest(SeleniumTestCase):

    def test_initial_request_index(self):
        self.browser_get_reverse('index')

        self.assert_title('index-title')
        self.assert_content('index-content')

    def test_initial_request_about(self):
        self.browser_get_reverse('about')

        self.assert_title('about-title')
        self.assert_content('about-content')

        keywords_metatag = self.browser.find_element_by_css_selector('meta[name="keywords"]')
        self.assertEqual(keywords_metatag.get_attribute('content'), 'This is a test')

    def test_initial_request_project(self):
        self.browser_get_reverse('project')

        self.assert_title('project-title')
        self.assert_content('project-content')

    def test_initial_request_project_blog(self):
        self.browser_get_reverse('project_blog')

        self.assert_title('project-blog-title')
        self.assert_content('project-blog-content')

    def test_initial_request_project_gallery(self):
        self.browser_get_reverse('project_gallery')

        self.assert_title('project-gallery-title')
        self.assert_content('project-gallery-content')
