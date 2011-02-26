from django.conf.urls.defaults import *
#from staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from test_attachments.tester.views import index

urlpatterns = patterns('',
    # Example:
    # (r'^test_attachments/', include('test_attachments.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^attachments/', include('attachments.urls')),

    url(r'^$', index, name="index"),
)

#if settings.DEBUG:
#    urlpatterns += staticfiles_urlpatterns()
