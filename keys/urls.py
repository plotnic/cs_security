from django.conf.urls import url

from keys import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^details$', views.details, name='details'),
	url(r'^main$', views.main, name='main'),
	url(r'^exit$', views.exit, name='exit'),
	url(r'^new$', views.get_codes, name='get_codes'),	
	url(r'^register$', views.register_new, name='register_new'),
	url(r'^getKey$', views.get_key, name='get_key'),
	url(r'^img/([A-Za-z0-9]+)$', views.get_img, name='get_img'),
]
