import views_auth
from django.conf.urls import include, url

urlpatterns = [
    url(r'^register2', views_auth.register2),
    url(r'^register', views_auth.register),
    url(r'^login', views_auth.login),
    url(r'^logout', views_auth.logout),
]
