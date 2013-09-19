from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import AboutView

admin.autodiscover()

urlpatterns = patterns('',
    # main
    url(r'^about/', AboutView.as_view(), name='about'),
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # planner
    url(r'^planner/', include('planner.urls', namespace='planner')),

)
