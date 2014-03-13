from __future__ import unicode_literals

from .helpers import SeleniumTestCase


class InitialRequestTest(SeleniumTestCase):

    def test_initial_request_index(self):
        self.browser.get('{}/'.format(self.live_server_url))

        self.assertTitle('index-title')
        self.assertContent('index-content')

    def test_initial_request_about(self):
        self.browser.get('{}/about/'.format(self.live_server_url))

        self.assertTitle('about-title')
        self.assertContent('about-content')

    def test_initial_request_project(self):
        self.browser.get('{}/project/'.format(self.live_server_url))

        self.assertTitle('project-title')
        self.assertContent('project-content')

    def test_initial_request_project_blog(self):
        self.browser.get('{}/project/blog/'.format(self.live_server_url))

        self.assertTitle('project-blog-title')
        self.assertContent('project-blog-content')

    def test_initial_request_project_gallery(self):
        self.browser.get('{}/project/gallery/'.format(self.live_server_url))

        self.assertTitle('project-gallery-title')
        self.assertContent('project-gallery-content')
