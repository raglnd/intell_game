'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com
    
    /game/urls.py
        Django url resolvers for game app
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games/$', views.games, name='games'),
    url(r'^games/create/$', views.create, name="create"),
    url(r'^games/(?P<pk>[0-9]+)/$', views.game_detail, name="game_detail"),
    url(r'^games/(?P<pk>[0-9]+)/join/$', views.join, name="join"),
    url(r'^games/(?P<pk>[0-9]+)/end/$', views.end, name="end"),
    url(r'^agents/$', views.agents, name='agents'),
    url(r'^agents/(?P<pk>[0-9]+)/$', views.agent_detail, name="agent_detail"),
    url(r'^players/$', views.players, name='players'),
    url(r'^players/(?P<pk>[0-9]+)/$', views.player_detail, name="player_detail"),
    url(r'^knowledges/$', views.knowledges, name='knowledges'),
    url(r'^knowledges/(?P<pk>[0-9]+)/$', views.knowledge_detail, name="knowledge_detail"),
    url(r'^play/(?P<pk>[0-9]+)/$', views.play, name="play"),
    url(r'^play/(?P<pk>[0-9]+)/submit_action/$', views.submit_action, name="submit_action"),
    url(r'^play/(?P<pk>[0-9]+)/get_status/$', views.get_status, name="get_status"),
    url(r'^play/(?P<pk>[0-9]+)/get_snippets/$', views.get_snippets, name="get_snippets"),
    url(r'^play/(?P<pk>[0-9]+)/get_characters/$', views.get_characters, name="get_characters"),
    url(r'^play/(?P<pk>[0-9]+)/get_locations/$', views.get_locations, name="get_locations"),
    url(r'^play/(?P<pk>[0-9]+)/get_agents/$', views.get_agents, name="get_agents"),
    url(r'^play/(?P<pk>[0-9]+)/get_own_agents/$', views.get_own_agents, name="get_own_agents"),
]
