from django.conf.urls import patterns, url

from .views import HomeView, ActionSearchView, ActionListView, ActionCreateView, ActionDetailView, ActionUpdateView, \
    FlowSearchView, FlowListView, FlowCreateView, FlowDetailView, FlowUpdateView, PhaseSearchView, PhaseListView, \
    PhaseCreateView, PhaseDetailView, PhaseUpdateView, get_tag_list

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    # actions
    url(r'^action/search/$', ActionSearchView.as_view(), name='_action_search'),
    url(r'^action/list/$', ActionListView.as_view(), name='action_list'),
    url(r'^action/add/$', ActionCreateView.as_view(), name='action_add'),
    url(r'^action/update/(?P<pk>\d+)/$', ActionDetailView.as_view(), name='action_update'),
    url(r'^action/(?P<pk>\d+)/delete/$', ActionUpdateView.as_view(), name='action_delete'),

    #flows
    url(r'^flow/search/$', FlowSearchView.as_view(), name='_flow_search'),
    url(r'^flow/list/$', FlowListView.as_view(), name='flow_list'),
    url(r'^flow/add/$', FlowCreateView.as_view(), name='flow_add'),
    url(r'^flow/update/(?P<pk>\d+)/$', FlowDetailView.as_view(), name='flow_update'),
    url(r'^flow/(?P<pk>\d+)/delete/$', FlowUpdateView.as_view(), name='flow_delete'),

    # phases
    url(r'^phase/search/$', PhaseSearchView.as_view(), name='_phase_search'),
    url(r'^phase/list/$', PhaseListView.as_view(), name='phase_list'),
    url(r'^phase/add/$', PhaseCreateView.as_view(), name='phase_add'),
    url(r'^phase/update/(?P<pk>\d+)/$', PhaseDetailView.as_view(), name='phase_update'),
    url(r'^phase/(?P<pk>\d+)/delete/$', PhaseUpdateView.as_view(), name='phase_delete'),

    # tags
    url(r'^tags/$', get_tag_list),

)