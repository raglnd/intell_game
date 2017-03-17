'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

    editor/urls.py
        Django url resolvers
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    #index
    url(r'^$', views.index, name='index'),

    #ajax_scenario
    url(r'^accept_ajax_scenario/$', views.accept_ajax_scenario, name='accept_ajax_scenario'),
    url(r'^dump_request/$', views.dump_request, name='dump_request'),

    #manual html page based editor 
    #TODO: migrate to FE js/html editor
    #bootstrap html
    url(r'^edit/$', views.edit, name='edit'),


    url(r'^dump_session/$', views.dump_session, name='dump_sesssion'),

    #manual html character pages
    url(r'^edit/character/$', views.CharacterList.as_view(), name="character-view"),
    url(r'^edit/character/add/$', views.CharacterCreate.as_view(), name="character-add"),
    url(r'^edit/character/(?P<pk>[0-9]+)/$', views.CharacterUpdate.as_view(), name="character-update"),
    url(r'^edit/character/(?P<pk>[0-9]+)/delete/$', views.CharacterDelete.as_view(), name="character-delete"),

    #manual html location pages
    url(r'^edit/location/$', views.LocationList.as_view(), name="character-view"),
    url(r'^edit/location/add/$', views.LocationCreate.as_view(), name="character-add"),
    url(r'^edit/location/(?P<pk>[0-9]+)/$', views.LocationUpdate.as_view(), name="character-update"),
    url(r'^edit/location/(?P<pk>[0-9]+)/delete/$', views.LocationDelete.as_view(), name="character-delete"),
    
    #manual html description pages
    url(r'^edit/description/$', views.DescriptionList.as_view(), name="character-view"),
    url(r'^edit/description/add/$', views.DescriptionCreate.as_view(), name="character-add"),
    url(r'^edit/description/(?P<pk>[0-9]+)/$', views.DescriptionUpdate.as_view(), name="character-update"),
    url(r'^edit/description/(?P<pk>[0-9]+)/delete/$', views.DescriptionDelete.as_view(), name="character-delete"),

    #manual html describedby pages
    url(r'^edit/describedby/$', views.DescribedByList.as_view(), name="character-view"),
    url(r'^edit/describedby/add/$', views.DescribedByCreate.as_view(), name="character-add"),
    url(r'^edit/describedby/(?P<pk>[0-9]+)/$', views.DescribedByUpdate.as_view(), name="character-update"),
    url(r'^edit/describedby/(?P<pk>[0-9]+)/delete/$', views.DescribedByDelete.as_view(), name="character-delete"),
   
    #manual html happenedat pages
    url(r'^edit/happenedat/$', views.HappenedAtList.as_view(), name="character-view"),
    url(r'^edit/happenedat/add/$', views.HappenedAtCreate.as_view(), name="character-add"),
    url(r'^edit/happenedat/(?P<pk>[0-9]+)/$', views.HappenedAtUpdate.as_view(), name="character-update"),
    url(r'^edit/happenedat/(?P<pk>[0-9]+)/delete/$', views.HappenedAtDelete.as_view(), name="character-delete"),

    #manual html involved pages
    url(r'^edit/involved/$', views.InvolvedList.as_view(), name="character-view"),
    url(r'^edit/involved/add/$', views.InvolvedCreate.as_view(), name="character-add"),
    url(r'^edit/involved/(?P<pk>[0-9]+)/$', views.InvolvedUpdate.as_view(), name="character-update"),
    url(r'^edit/involved/(?P<pk>[0-9]+)/delete/$', views.InvolvedDelete.as_view(), name="character-delete"),
    
    #manual html event pages
    url(r'^edit/event/$', views.EventList.as_view(), name="character-view"),
    url(r'^edit/event/add/$', views.EventCreate.as_view(), name="character-add"),
    url(r'^edit/event/(?P<pk>[0-9]+)/$', views.EventUpdate.as_view(), name="character-update"),
    url(r'^edit/event/(?P<pk>[0-9]+)/delete/$', views.EventDelete.as_view(), name="character-delete"),

    url(r'^scenarios/(?P<pk>[0-9]+)/$', views.scenario_details, name="scenario_details"),
    url(r'^scenarios/$', views.scenario_list, name="scenario_list"),
    url(r'^scenarios/(?P<pk>[0-9]+)/graph/$', views.scenario_graph, name="scenario_graph"),
]
