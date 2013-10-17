from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import AboutView, HomeView

admin.autodiscover()

urlpatterns = patterns('',
    # main
    url(r'^hoomanhub/$', HomeView.as_view(), name='home'),
    url(r'^hoomanhub/about/$', AboutView.as_view(), name='about'),
    # admin
    url(r'^hoomanhub/admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^hoomanhub/admin/', include(admin.site.urls)),
    # plan
    url(r'^hoomanhub/plan/', include('plan.urls', namespace='plan')),
    #do
    url(r'^hoomanhub/do/', include('do.urls', namespace='do')),
    #monitor
    url(r'^hoomanhub/monitor/', include('monitor.urls', namespace='monitor')),
    #connect
    url(r'^hoomanhub/connect/', include('connect.urls', namespace='connect')),

)
