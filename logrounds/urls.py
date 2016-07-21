from django.conf.urls import url

from . import views
from logrounds.views import *

app_name = 'logrounds'
urlpatterns = [
	url(r'^index/$', views.index, name='index'),
	url(r'^round/(?P<round_id>[0-9]+)/$', views.round_detail, name='detail'),
	url(r'^$', views.home, name='home'),
	url(r'^create_round/$', RoundCreate.as_view(), name='create'),
	url(r'^round/update/(?P<pk>[0-9]+)/$', RoundUpdate.as_view(), name='update_round'),
	url(r'^round/remove/(?P<pk>[0-9]+)/$', RoundDelete.as_view(), name='remove_round'),
	url(r'^add_period/$', views.add_period, name='new_period'),
	url(r'^periods/$', views.periods, name='periods'),
	url(r'^add_logdef/(?P<round_id>[0-9]+)/$', views.create_logdef, name='new_logdef'),
	url(r'^logdef/(?P<logdef_id>[0-9]+)/$', views.logdef_detail,\
		name='logdef_detail'),
	url(r'^logdef/(?P<logdef_id>[0-9]+)/edit/$', views.edit_logdef,\
		name='edit_logdef'),
	url(r'^logdef/(?P<pk>[0-9]+)/remove/$', views.LogDefDelete.as_view(),\
		name='remove_logdef'),
	url(r'^round/(?P<round_id>[0-9]+)/activities/$', views.activities, name='activities'),
	url(r'^round/(?P<round_id>[0-9]+)/(?P<ld_id>[0-9]+)/(?P<ls_id>[0-9]+)/create/$',
		views.create_entry, name='create_entry'),
	url(r'^round/(?P<round_id>[0-9]+)/(?P<ld_id>[0-9]+)/(?P<ls_id>[0-9]+)/(?P<pk>[0-9]+)/$',
		views.LogEntryDetailView.as_view(), name='entry_details'),
	url(r'^round/(?P<round_id>[0-9]+)/(?P<ld_id>[0-9]+)/(?P<ls_id>[0-9]+)/(?P<parent>[0-9]+)/update/$',
		views.entry_update, name='entry_update'),

]