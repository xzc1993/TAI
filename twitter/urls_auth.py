import views_auth
from django.conf.urls import include, url

urlpatterns = [
    url(r'^signInWithTwitter2', views_auth.signInWithTwitter2),
    url(r'^signInWithTwitter', views_auth.signInWithTwitter, name='signInWithTwitter' ),
    url(r'^logout', views_auth.logout, name='logout'),
]
