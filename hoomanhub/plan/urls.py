from django.conf.urls import patterns, url

from .views import HomeView, ActionSearchView, ActionListView, ActionCreateView, ActionDetailView, ActionUpdateView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^action/search/$', ActionSearchView.as_view(), name='_action_search'),
    url(r'^action/list/$', ActionListView.as_view(), name='action_list'),
    url(r'^action/add/$',ActionCreateView.as_view(), name='action_add'),
    url(r'^action/update/(?P<pk>\d+)/$',ActionDetailView.as_view(), name='action_update'),
    url(r'^action/(?P<pk>\d+)/delete/$',ActionUpdateView.as_view(), name='action_delete'),
)