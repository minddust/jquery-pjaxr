from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^invalid-metatag/$', TemplateView.as_view(template_name='invalid_metatag.html'), name='invalid_metatag'),
    url(r'^project/$', TemplateView.as_view(template_name='project.html'), name='project'),
    url(r'^project/blog/$', TemplateView.as_view(template_name='project_blog.html'), name='project_blog'),
    url(r'^project/gallery/$', TemplateView.as_view(template_name='project_gallery.html'), name='project_gallery')
)
