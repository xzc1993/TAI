import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^main', views.main, name='main'),
]
