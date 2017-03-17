'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

    editor/admin.py
        Django Admin settings for editor app
        currently expose all models
'''
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Scenario)
admin.site.register(Character)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Description)
admin.site.register(DescribedBy)
admin.site.register(HappenedAt)
admin.site.register(Involved)
