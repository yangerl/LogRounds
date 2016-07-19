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
	url(r'^add_logdef/$', LogDefCreate.as_view(), name='new_logdef'),
	url(r'^logdef/(?P<logdef_id>[0-9]+)/$', views.logdef_detail,\
		name='logdef_detail'),
	url(r'^logdef/(?P<logdef_id>[0-9]+)/edit/$', views.edit_logdef,\
		name='edit_logdef'),
	url(r'^logdef/(?P<pk>[0-9]+)/remove$', views.LogDefDelete.as_view(),\
		name='remove_logdef'),
	url(r'^round/(?P<round_id>[0-9]+)/activities$', views.activities, name='activities'),
	url(r'^round/(?P<round_id>[0-9]+)/(?P<logset_id>[0-9]+)$',\
		views.logset_details, name='logset_details'),
	url(r'^round/(?P<round_id>[0-9]+)/(?P<logset_id>[0-9]+)/(?P<logdef_id>[0-9]+)/(?P<logentry_id>[0-9]+)$',\
		views.logentry_details, name='logentry_details'),

]