'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

    editor/models.py
        Django Models
            Scenario
            Character
            Location
            Description
            DescribedBy
            HappenedAt
            Involved
'''

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import json
# Create your models here.
'''
Scenario
    id          - auto gen primary key
    name        - author's name for scenario
    turn_num    - turns in game
    point_num   - starting points in game
    author      - author's name, db will actually connect author model to
                    their scenarios but this way the author can choose to
                    be anonomys - thats not spelled right sue me. 
    file_name   - location JSON dump will be stored (/static ?)
'''
class Scenario(models.Model):
    name = models.CharField(max_length=64, null=True)
    turn_num = models.IntegerField()
    point_num = models.IntegerField()
    author = models.ForeignKey(User, null=True)     # too short?
    file_name = models.FileField(upload_to='scenarios', null=True) 

    def __str__(self):
        if self.author != None:
            return self.author.username + " presents " + self.name
        else:
            return self.name

    def graph_dump(self):
        events = list(self.event_set.all())
        characters = []
        locations = []
        descriptions = []
        describedbys = []
        happenedats = []
        involveds = []

        for event in events:
            dbs = event.describedby_set.all()
            describedbys += list(dbs)
            for db in dbs:
                descriptions += [db.description]

            has = event.happenedat_set.all()
            happenedats += list(has)
            for ha in has:
                location = ha.location
                if location not in locations:
                    locations += [location]

            invs = event.involved_set.all()
            involveds += list(invs)
            for inv in invs:
                character = inv.character
                if character not in characters:
                    characters += [character]


        dump = [characters, locations, descriptions, events,
                describedbys, happenedats, involveds]
        for i in range(len(dump)):
            for j in range(len(dump[i])):
                dump[i][j] = dump[i][j].graph_dump()
        tables = ['Character', 'Location', 'Description', 'Event',
                  'DescribedBy', 'HappenedAt', 'Involved']
        schema = {"Character":["id", "name", "key"],
                  "Location":["id", "name", "x", "y"], 
                  "Description":["id", "text", "hidden"],
                  "Event":["id", "turn"],
                  "DescribedBy":["id", "event_id", "description_id"],
                  "HappenedAt":["id", "event_id", "location_id"],
                  "Involved":["id", "event_id", "character_id"]}
        split = 4

        return json.dumps({"tables": tables,
                           "schema": json.dumps(schema),
                           "dump": json.dumps(dump),
                           "split": split})

    '''
    load_events
        used to populate db if the events in the file are not in the db
        called when a game is being spun up
        for now unimplemnted (events always in db)
    '''
    def load_events(self):
        pass

    '''
    unload_events
        used to depopulate db when a game ends. 
        called by manager
        for now unimplemented (events always in db)
    '''
    def unload_events(self):
        pass

'''
Character
    id          - auto get primary key
    name        - name of character
    key         - is the character key to the scenario? True: user wins on
                    capture
    notes       - author notes about character
'''
class Character(models.Model):
    name = models.CharField(max_length=64)
    key = models.NullBooleanField()
    notes = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    def graph_dump(self):
        return {"key": self.key, "name": self.name, "id": self.pk}

    def get_absolute_url(self):
        return reverse("edit")

'''
Location
    id          - auto gen primary key
    name        - name of location
    x           - x coord of location
    y           - y coord of location
'''
class Location(models.Model):
    name = models.CharField(max_length=64)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.name

    def graph_dump(self):
        return {"x": self.x, "name": self.name, "y": self.y, "id": self.pk}

    def get_absolute_url(self):
        return reverse("edit")

'''
Description
    id          - auto gen primary key
    text        - description of the event (events can have multiple
                    description so multiple text's)
    hidden      - flag indicating whether the description is hidden by default
                    an Event's Description(s) can have different hidden flag
                    values (basis of investigations)
    name        - TODO:why does this have a name
    key         - flag indicating if the description is relevent to the
                    scenario 
                    TODO: should this be moved to event? (i say no)
'''
class Description(models.Model):
    text = models.CharField(max_length=512)
    hidden = models.BooleanField()
    name = models.CharField(max_length=64)
    key = models.NullBooleanField()

    def __str__(self):
        return self.text

    def graph_dump(self):
        return {"id": self.pk, "text": self.text, "hidden": self.hidden}

    def get_absolute_url(self):
        return reverse("edit")
        
'''
Event
    id          - auto gen primary key
    turn        - turn event occurs on
'''
class Event(models.Model):
    turn = models.IntegerField()
    scenario = models.ForeignKey("Scenario", null=True)
    misinf = models.BooleanField(default=False)

    def __str__(self):
        return "Event on turn "+str(self.turn)

    def graph_dump(self):
        return {"id": self.pk, "turn": self.turn}

    def get_absolute_url(self):
        return reverese("edit")

    def get_snippets(self):
        snippets = {}
        for descby in DescribedBy.objects.filter(event=self):
            snippets[descby.description.id] = descby.description.text
        return snippets

'''
Involved
    id          - auto gen primary key
    event       - id of event
    character   - id of character
'''
class Involved(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + \
               " and " + str(self.character)

    def graph_dump(self):
        return {"id": self.pk, 
                "event_id": self.event_id, 
                "character_id": self.character_id}

    def get_absolute_url(self):
        return reverse("edit")

'''
HappenedAt
    id          - auto gen primary key
    event       - id of event
    location    - id of location
'''
class HappenedAt(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + \
               " and " + str(self.location)

    def graph_dump(self):
        return {"id": self.pk, 
                "event_id": self.event_id, 
                "location_id": self.location_id}
    
    def get_absolute_url(self):
        return reverse("edit")

'''
DescribedBy
    id          - auto gen primary key
    event       - id of event
    description - id of description
'''
class DescribedBy(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.ForeignKey(Description, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + \
               " and " + str(self.description)

    def graph_dump(self):
        return {"id": self.pk, 
                "event_id": self.event_id, 
                "description_id": self.description_id}

    def get_absolute_url(self):
        return reverse("edit")
