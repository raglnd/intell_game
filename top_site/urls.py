'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

    top_site/urls.py
        Django url resolvers
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'accounts/profile/$', views.profile, name='profile'),
    url(r'^register', views.register, name="register"),
]
