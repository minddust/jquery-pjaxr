from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView


urlpatterns = patterns('',
    # main functionality
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^project/$', TemplateView.as_view(template_name='project.html'), name='project'),
    url(r'^project/blog/$', TemplateView.as_view(template_name='project_blog.html'), name='project_blog'),
    url(r'^project/gallery/$', TemplateView.as_view(template_name='project_gallery.html'), name='project_gallery'),

    # pjaxrReady and pjaxrAlways
    url(r'^pjaxr-ready-pjaxr-always/$', TemplateView.as_view(template_name='pjaxr_ready_pjaxr_always.html'), name='pjaxr_ready_pjaxr_always'),
    url(r'^pjaxr-ready-pjaxr-always/(?P<disabled>[(true)]+)/$', TemplateView.as_view(template_name='pjaxr_ready_pjaxr_always.html'), name='pjaxr_ready_pjaxr_always_disabled'),

    # issue urls
    url(r'^ignored-metatag/$', TemplateView.as_view(template_name='ignored_metatag.html'), name='ignored_metatag'),
    url(r'^no-pjaxr-response/$', TemplateView.as_view(template_name='no_pjaxr_response.html'), name='no_pjaxr_response'),

    # prevent travis 404 logs
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
)
