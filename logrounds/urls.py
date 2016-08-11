from django.conf.urls import url

from . import views
from logrounds.views import *
from django.contrib.auth.decorators import login_required

app_name = 'logrounds'
#[0-9]{4}-[0-9]{2}-[0-9]{2}%20[0-9]{2}:[0-9]{2}:[0-9]{2}
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^round/(?P<round_id>[0-9]+)/$', views.round_detail, name='detail'),

    url(r'^round/(?P<round_id>[0-9]+)/activities/$', views.activities, name='activities'),
    url(r'^round/(?P<round_id>[0-9]+)/grid/(?P<start_time>.+)/$'
        , views.data_grid, name='data_grid'),
    url(r'^$', views.index, name='index'),
    url(r'^create_round/$', login_required(RoundCreate.as_view()), name='create'),

    # url(r'^create_round/$', permission_required('RoundType.add_roundtype')(RoundCreate.as_view()), name='create'),
    url(r'^round/update/(?P<pk>[0-9]+)/$', login_required(RoundUpdate.as_view()), name='update_round'),
    url(r'^round/remove/(?P<pk>[0-9]+)/$', login_required(RoundDelete.as_view()), name='remove_round'),
    url(r'^add_period/$', views.add_period, name='new_period'),
    url(r'^add_logdef/(?P<round_id>[0-9]+)/$', views.create_logdef, name='new_logdef'),
    url(r'^logdef/(?P<logdef_id>[0-9]+)/$', views.logdef_detail,\
        name='logdef_detail'),
    url(r'^logdef/(?P<logdef_id>[0-9]+)/edit/$', views.edit_logdef,\
        name='edit_logdef'),
    url(r'^logdef/(?P<pk>[0-9]+)/remove/$', login_required(LogDefDelete.as_view()),\
        name='remove_logdef'),
    url(r'^round/(?P<round_id>[0-9]+)/(?P<ld_id>[0-9]+)/(?P<ls_id>[0-9]+)/create/$',
        views.create_entry, name='create_entry'),
    url(r'^round/(?P<round_id>[0-9]+)/(?P<ld_id>[0-9]+)/(?P<ls_id>[0-9]+)/(?P<pk>[0-9]+)/$',
        login_required(LogEntryDetailView.as_view()), name='entry_details'),
    url(r'^round/(?P<round_id>[0-9]+)/(?P<ld_id>[0-9]+)/(?P<ls_id>[0-9]+)/(?P<parent>[0-9]+)/update/$',
        views.entry_update, name='entry_update'),


]