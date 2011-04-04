from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from test_attachments.tester.views import index

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^attachments/', include('attachments.urls')),
    url(r'^$', index, name="index"),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT}),
    (r'^secure/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.SECURE_ROOT}),
)
