import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^main', views.main, name='main'),
    url(r'^events', views.events, name='events'),
    url(r'^event/new', views.newEvent, name='newEvent'),
    url(r'^event/create', views.createEvent, name='createEvent'),

    url(r'^event/(?P<event_id>\d+)/comment/new', views.newComment, name='newComment'),
    url(r'^event/(?P<event_id>\d+)/comment/create', views.createComment, name='createComment'),
    url(r'^event/(?P<event_id>\d+)', views.showEvent, name='showEvent'),
    #url(r'^showComment/(?P<id>\d+)', views.showComment, name='showComment'),
]
