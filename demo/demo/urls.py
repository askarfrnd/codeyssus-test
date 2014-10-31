from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'user_profiles.views.home'),
    url(r'^login', 'user_profiles.views.login_user'),
    url(r'^dashboard/$', 'user_profiles.views.dashboard'),
    url(r'^logout/$', 'user_profiles.views.logout_user'),
    url(r'^accounts/signup', 'user_profiles.views.home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
