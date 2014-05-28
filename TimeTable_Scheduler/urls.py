import django
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib.auth import admin
from django.views import static
from TimeTable_Scheduler import settings
from timetable import urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TimeTable_Scheduler.views.home', name='home'),
    # url(r'^TimeTable_Scheduler/', include('TimeTable_Scheduler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^timetable/', include(urls)),


)



urlpatterns += staticfiles_urlpatterns()



