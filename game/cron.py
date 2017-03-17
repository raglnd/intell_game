'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com/

        game/cron.py
            django-crontab game crontab functions
            using - https://github.com/kraiz/django-crontab
            to schedule events.
                check_games

        TODO: think of a better way to do this
'''

from .models import Game
from django.utils.timezone import datetime, make_aware

'''
check_games
    check if any games need to be started or the next turn
    needs to be proccessed
'''
def check_games():
    current_time = make_aware(datetime.now())
    for game in Game.objects.all():
        game.check_game()
        '''
        if current_time > game.next_turn:
            #check if next turn can start
            if game.started:
                game.start_next_turn()
            #check if game is ready to start. If so call start
            else:
                game.start()
        ...
