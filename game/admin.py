'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

        game/admin.py
            Django admin settings for game
            currently all models exposed
'''
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Agent)
admin.site.register(Action)
admin.site.register(Knowledge)
admin.site.register(Message)
admin.site.register(Misinformation)
