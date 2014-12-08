from django.conf.urls import url

from keys import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^details$', views.details, name='details'),
	url(r'^main$', views.main, name='main'),
	url(r'^exit$', views.exit, name='exit'),
]
