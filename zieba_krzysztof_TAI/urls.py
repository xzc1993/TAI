from django.conf.urls import include, url
from django.contrib import admin
from tweeter import urls_auth, urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include(urls)),
    url(r'^auth/', include(urls_auth)),
]
