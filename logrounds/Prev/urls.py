from django.conf.urls import url

from . import views

app_name = 'logrounds'
urlpatterns = [
	url(r'^index/$', views.index, name='index'),
	url(r'^round/(?P<round_id>[0-9]+)/$', views.round_detail, name='detail'),
	url(r'^$', views.home, name='home'),
	url(r'^create/$', views.create, name='create'),
	url(r'^add_period/$', views.add_period, name='new_period'),
	url(r'^periods/$', views.periods, name='periods'),
	url(r'^add_logdef/$', views.add_logdef, name='new_logdef'),
	url(r'^logdef/(?P<logdef_id>[0-9]+)/$', views.logdef_detail,\
		name='logdef_detail'),
	url(r'^logdef/(?P<logdef_id>[0-9]+)/edit$', views.edit_logdef,\
		name='edit_logdef'),
	#url(r'^add_logset/$', views.add_logset, name='new_logset'),
	#url(r'^add_logset/$', views.add_logset, name='new_logset')
]