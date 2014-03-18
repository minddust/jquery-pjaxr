from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class InitialRequestTest(SeleniumTestCase):

    def test_initial_request_index(self):
        self.browser_get_reverse('index')

        self.assertTitle('index-title')
        self.assertContent('index-content')

    def test_initial_request_about(self):
        self.browser_get_reverse('about')

        self.assertTitle('about-title')
        self.assertContent('about-content')

    def test_initial_request_project(self):
        self.browser_get_reverse('project')

        self.assertTitle('project-title')
        self.assertContent('project-content')

    def test_initial_request_project_blog(self):
        self.browser_get_reverse('project_blog')

        self.assertTitle('project-blog-title')
        self.assertContent('project-blog-content')

    def test_initial_request_project_gallery(self):
        self.browser_get_reverse('project_gallery')

        self.assertTitle('project-gallery-title')
        self.assertContent('project-gallery-content')
