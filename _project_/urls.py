from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.admin import site

from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="base.html"), name='home'),

    # enable the admin:
    url(r'^admin/', include(site.urls)),
)

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT})
    )