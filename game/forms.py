'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com


    game/forms.py
        Django forms
            GameForm
'''

from django.forms import ModelForm
from .models import Game

'''
GameForm
    used by create view to make new games
    presents scenario, turn_length, next_turn fields
'''
class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['scenario', 'turn_length']
