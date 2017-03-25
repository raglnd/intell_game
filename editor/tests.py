'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

    editor/tests.py
        EventTestCase
            test_create_event
            test_single_described_by
            test_multiple_described_by
        CharacterTestCase
            test_create_character
        LocationTestCase
            test_create_location
        DescriptionTestCase
            test_create_description
        IntegrationTestCase
            test_sending_fixture_with_title

    TODO:   Document additions.
'''

from django.test import TestCase, Client
from .models import *
import json

# Create your tests here.
'''
EventTestCase
    test_create_event
    test_single_described_by
    test_multiple_described_by
'''
class EventTestCase(TestCase):
    '''
        The dead parrot sketch test case
        tests event creation and connectors
    '''
    def setUp(self):
        michael = Character.objects.create(name="Michael", key=True,
            notes="Michael is a pet shop owner")
        john = Character.objects.create(name="John", key=True,
            notes="John needs to return a bird to the pet shop")
        sgtmajor = Character.objects.create(name="Sergeant Major", key=False,
            notes="The Sergeant Major does not approve of silliness")

        petshop = Location.objects.create(name="Pet Shop", x=0, y=10)
        bolton = Location.objects.create(name="Bolton Pet Shop", x=20, y=30)

        original = Description.objects.create(name="original transaction", 
            key=False,
            hidden=False, 
            text="Michael sold john a norwegian blue")
        returnAttempt = Description.objects.create(name="return attempt", 
            key=True, 
            hidden=False, 
            text="John tries to return the parrot but is sent to bolton")
        boltonReturn = Description.objects.create(name="bolton return attempt", 
            key=False,
            hidden=True,
            text="Michael tells john he isnt in bolton but rather ipswitch")
        tooSilly = Description.objects.create(name="the sgt major intervenes", 
            key=True,
            hidden=True,
            text="John believes things are gitting silly and the sgt major agrees")

		# Default case.
        e0 = Event.objects.create(turn=0)
		# Misinform check.
        e1 = Event.objects.create(turn=1, misinf=True)
		# Misinform negative check.
        e2 = Event.objects.create(turn=2, misinf=False)

        DescribedBy.objects.create(event=e0, description=original)
        DescribedBy.objects.create(event=e1, description=returnAttempt)
        DescribedBy.objects.create(event=e2, description=boltonReturn)
        DescribedBy.objects.create(event=e2, description=tooSilly)

        HappenedAt.objects.create(event=e0, location=petshop)
        HappenedAt.objects.create(event=e1, location=petshop)
		HappenedAt.objects.create(event=e1, location=bolton)
        HappenedAt.objects.create(event=e2, location=bolton)

        Involved.objects.create(event=e0, character=michael)
        Involved.objects.create(event=e1, character=michael)
        Involved.objects.create(event=e1, character=john)
        Involved.objects.create(event=e2, character=michael)
        Involved.objects.create(event=e2, character=john)
        Involved.objects.create(event=e2, character=sgtmajor)

    def test_create_event(self):
        '''test Event created'''
        event = Event.objects.get(turn=0)
        self.assertEqual(event.turn, 0)
		self.assertEqual(event.misinf, False)
		
		event = Event.objects.get(turn=1)
        self.assertEqual(event.turn, 1)
		self.assertEqual(event.misinf, True)
		
		event = Event.objects.get(turn=2)
        self.assertEqual(event.turn, 2)
		self.assertEqual(event.misinf, False)
        
    def test_single_describedby(self):
        '''test DescribedBy with 1-1 event-description'''
        e0 = Event.objects.get(turn=0)
        originalDB = DescribedBy.objects.get(event=e0)
        description = originalDB.description

        # get not failing implies only one object returned
        self.assertEqual(description.name, "original transaction")
		self.assertEqual(description.text, "Michael sold john a norwegian blue")
		self.assertEqual(description.hidden, False)
		self.assertEqual(description.key, False)
		
		e1 = Event.objects.get(turn=1)
        retAttDB = DescribedBy.objects.get(event=e1)
        description = retAttDB.description

        # get not failing implies only one object returned
        self.assertEqual(description.name, "return attempt")
		self.assertEqual(description.text, "John tries to return the parrot but is sent to bolton")
		self.assertEqual(description.hidden, False)
		self.assertEqual(description.key, True)

    def test_multiple_describedby(self):
        '''test DescribedBy with 1-M event-description'''
        e2 = Event.objects.get(turn=2)
        db = DescribedBy.objects.filter(event=e2)
        
        self.assertEqual(len(db), 2)
        d0 = db[0].description
        d1 = db[1].description

        self.assertNotEqual(d0, d1)
        valid_names = ["bolton return attempt", "the sgt major intervenes"]

        self.assertEqual(d0.name in valid_names, True)
        self.assertEqual(d1.name in valid_names, True)
		
		if d0.name == "bolton return attempt":
			braDesc = d0
			tsmiDesc = d1
		else:
			braDesc = d1
			tsmiDesc = d0
			
		self.assertEqual(braDesc.name, "bolton return attempt")
		self.assertEqual(braDesc.text, "Michael tells john he isnt in bolton but rather ipswitch")
		self.assertEqual(braDesc.hidden, True)
		self.assertEqual(braDesc.key, False)
		
		self.assertEqual(tsmiDesc.name, "the sgt major intervenes")
		self.assertEqual(tsmiDesc.text, "John believes things are gitting silly and the sgt major agrees")
		self.assertEqual(tsmiDesc.hidden, True)
		self.assertEqual(tsmiDesc.key, True)
		
	def test_single_happenedat(self):
		'''test HappenedAt with 1-1 event-location'''
        e0 = Event.objects.get(turn=0)
        HA = HappenedAt.objects.get(event=e0)
        location = HA.location

        # get not failing implies only one object returned
        self.assertEqual(location.name, "Pet Shop")
		self.assertEqual(location.x, 0)
		self.assertEqual(location.y, 10)
		
		e2 = Event.objects.get(turn=2)
        HA = HappenedAt.objects.get(event=e2)
        location = HA.location

        # get not failing implies only one object returned
        self.assertEqual(location.name, "Bolton Pet Shop")
		self.assertEqual(location.x, 20)
		self.assertEqual(location.y, 30)
		
	
	def test_multiple_happenedat(self):
		'''test HappenedAt with 1-M event-location'''
        e1 = Event.objects.get(turn=1)
        ha = HappenedAt.objects.filter(event=e1)
        
        self.assertEqual(len(ha), 2)
        l0 = ha[0].location
        l1 = ha[1].location

        self.assertNotEqual(l0, l1)
        valid_names = ["Pet Shop", "Bolton Pet Shop"]

        self.assertEqual(l0.name in valid_names, True)
        self.assertEqual(l1.name in valid_names, True)
		
		if l0.name == "Pet Shop":
			psLoc = l0
			bpsLoc = l1
		else:
			psLoc = l1
			bpsLoc = l0
			
		self.assertEqual(psLoc.name, "Pet Shop")
		self.assertEqual(psLoc.x, 0)
		self.assertEqual(psLoc.y, 10)
		
		self.assertEqual(bpsLoc.name, "Bolton Pet Shop")
		self.assertEqual(bpsLoc.x, 20)
		self.assertEqual(bpsLoc.y, 30)
	
	def test_single_involved(self):
		'''test Involved with 1-1 event-character'''
        e0 = Event.objects.get(turn=0)
        I = Involved.objects.get(event=e0)
        character = I.character

        # get not failing implies only one object returned
        self.assertEqual(character.name, "Michael")
		self.assertEqual(character.key, True)
		self.assertEqual(character.notes, "Michael is a pet shop owner")

		
	def test_multiple_involved(self):
		'''test Involved with 1-M event-character'''
        e1 = Event.objects.get(turn=1)
        I = Involved.objects.filter(event=e1)
        
        self.assertEqual(len(I), 2)
        c0 = I[0].character
        c1 = I[1].character

        self.assertNotEqual(c0, c1)
        valid_names = ["Michael", "John"]

        self.assertEqual(c0.name in valid_names, True)
        self.assertEqual(c1.name in valid_names, True)
		
		if c0.name == "Michael":
			mChar = c0
			jChar = c1
		else:
			mChar = c1
			jChar = c0
			
		self.assertEqual(mChar.name, "Michael")
		self.assertEqual(mChar.key, True)
		self.assertEqual(mChar.notes, "Michael is a pet shop owner")
		
		self.assertEqual(jChar.name, "John")
		self.assertEqual(jChar.key, True)
		self.assertEqual(jChar.notes, "John needs to return a bird to the pet shop")
		
		e2 = Event.objects.get(turn=2)
        I = Involved.objects.filter(event=e2)
        
        self.assertEqual(len(I), 3)
        c0 = I[0].character
        c1 = I[1].character
		c2 = I[2].character

        self.assertNotEqual(c0, c1)
		self.assertNotEqual(c0, c2)
		self.assertNotEqual(c1, c2)
        valid_names = ["Michael", "John", "Sergeant Major"]

        self.assertEqual(c0.name in valid_names, True)
        self.assertEqual(c1.name in valid_names, True)
		self.assertEqual(c2.name in valid_names, True)
		
		if c0.name == "Michael":
			mChar = c0
		elif c0.name == "John":
			jChar = c0
		else:
			smChar = c0
			
		if c1.name == "Michael":
			mChar = c1
		elif c1.name == "John":
			jChar = c1
		else:
			smChar = c1
			
		if c2.name == "Michael":
			mChar = c2
		elif c2.name == "John":
			jChar = c2
		else:
			smChar = c2
			
		self.assertEqual(mChar.name, "Michael")
		self.assertEqual(mChar.key, True)
		self.assertEqual(mChar.notes, "Michael is a pet shop owner")
		
		self.assertEqual(jChar.name, "John")
		self.assertEqual(jChar.key, True)
		self.assertEqual(jChar.notes, "John needs to return a bird to the pet shop")
		
		self.assertEqual(smChar.name, "Sergeant Major")
		self.assertEqual(smChar.key, False)
		self.assertEqual(smChar.notes, "The Sergeant Major does not approve of silliness")

'''
CharacterTestCase
    test_create_character
'''
class CharacterTestCase(TestCase):
    def setUp(self):
        Character.objects.create(name="Michael", key=True,
            notes="Michael is a pet shop owner")
        Character.objects.create(name="John", key=True,
            notes="John needs to return a bird to the pet shop")
        Character.objects.create(name="Sergeant Major", key=False,
            notes="The Sergeant Major does not approve of silliness")

    def test_create_character(self):
        '''Test creating characters'''
        michael = Character.objects.get(name="Michael")
		john = Character.objects.get(name="John")
        sgtmajor = Character.objects.get(name="Sergeant Major")

        self.assertEqual(michael.name, "Michael")
        self.assertEqual(michael.key, True)
		self.assertEqual(michael.notes, "Michael is a pet shop owner")
		
        self.assertEqual(john.name, "John")
        self.assertEqual(john.key, True)
		self.assertEqual(john.notes, "John needs to return a bird to the pet shop")
		
		self.assertEqual(sgtmajor.name, "Sergeant Major")
        self.assertEqual(sgtmajor.key, False)
		self.assertEqual(sgtmajor.notes, "The Sergeant Major does not approve of silliness")

'''
LocationTestCase
    test_create_location
'''
class LocationTestCase(TestCase):
    def setUp(self):
        Location.objects.create(name="Bikini Bottom", x=0, y=0)
        Location.objects.create(name="The Krusty Krab", x=0, y=10)

    def test_create_location(self):
        '''test creating locations'''
        krab = Location.objects.get(name="The Krusty Krab")
		bb = Location.objects.get(name="Bikini Bottom")

        self.assertEqual(krab.name, "The Krusty Krab")
        self.assertEqual(krab.x, 0)
        self.assertEqual(krab.y, 10)
		
		self.assertEqual(bb.name, "Bikini Bottom")
        self.assertEqual(bb.x, 0)
        self.assertEqual(bb.y, 0)

'''
DescriptionTestCase
    test_create_description
'''
class DescriptionTestCase(TestCase):
    def setUp(self):
        Description.objects.create(text="Joe went to the store", hidden=False,
            name="Joe store", key=False)
		Description.objects.create(text="Joe went to the hidden store", hidden=True,
            name="Joe hidden store", key=False)
		Description.objects.create(text="Joe importantly went to the store", hidden=False,
            name="Joe important store", key=True)
		Description.objects.create(text="Joe importantly went to the hidden store", hidden=True,
            name="Joe important hidden store", key=True)

    def test_create_description(self):
        '''test creating descriptions'''
        joestore = Description.objects.get(name="Joe store")
		joehstore = Description.objects.get(name="Joe hidden store")
		joeistore = Description.objects.get(name="Joe important store")
		joeihstore = Description.objects.get(name="Joe important hidden store")

        self.assertEqual(joestore.name, "Joe store")
        self.assertEqual(joestore.text, "Joe went to the store")
        self.assertEqual(joestore.hidden, False)
        self.assertEqual(joestore.key, False)
		
		self.assertEqual(joehstore.name, "Joe hidden store")
        self.assertEqual(joehstore.text, "Joe went to the hidden store")
        self.assertEqual(joehstore.hidden, True)
        self.assertEqual(joehstore.key, False)
		
		self.assertEqual(joeistore.name, "Joe important store")
        self.assertEqual(joeistore.text, "Joe importantly went to the store")
        self.assertEqual(joeistore.hidden, False)
        self.assertEqual(joeistore.key, True)
		
		self.assertEqual(joeihstore.name, "Joe important hidden store")
        self.assertEqual(joeihstore.text, "Joe importantly went to the hidden store")
        self.assertEqual(joeihstore.hidden, True)
        self.assertEqual(joeihstore.key, True)

'''
IntegrationTestCase
    test_sending_fixture_with_title
'''
class IntegrationTestCase(TestCase):
    def setUp(self):
        pass

    def test_sending_fixture_with_title(self):
        '''test posting json scenario'''
        self.assertEqual(len(Scenario.objects.all()), 0)
        #create request
        c = Client()
        file_in= open("editor/static/editor/fixture.json", 'r')
        body = file_in.read()
        file_in.close()
        response = c.post("/editor/accept_ajax_scenario/", 
                          content_type="application/json",
                          data=body)
        self.assertEqual(len(Scenario.objects.all()), 1)
        
        scenario = Scenario.objects.all()[0]
        self.assertEqual(scenario.name, "Fixture")

        #there are 29 characters in fixture.json
        self.assertEqual(len(Character.objects.all()), 29)
		
		#there are 33 locations in fixture.json
        self.assertEqual(len(Location.objects.all()), 33)
		
		#there are 25 events in fixture.json
        self.assertEqual(len(Event.objects.all()), 25)
		
		#there are 25 descriptions in fixture.json
        self.assertEqual(len(Description.objects.all()), 25)
		
		#there are 25 descriedbys in fixture.json
        self.assertEqual(len(DescribedBy.objects.all()), 25)
		
		#there are 29 involveds in fixture.json
        self.assertEqual(len(Involved.objects.all()), 29)

'''
EditorViewsTestCase
    test_index
    test_edit
    test_accept_ajax_scenario
    test_dump_session
    test_dump_request
'''
class EditorViewsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("user1", 
                                        "user@intellproject.com",
                                        "1234pass")
        self.client.force_login(user)

    def test_index(self):
        response = self.client.get("/editor/")
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        response = self.client.get("/editor/edit/")
        self.assertEqual(response.status_code, 200)

    def test_accept_ajax_scenario(self):
        response = self.client.get("/editor/accept_ajax_scenario/")
        self.assertEqual(response.status_code, 404)

        file_in = open("editor/static/editor/fixture.json", "r")
        body = file_in.read()
        file_in.close()

        response = self.client.post("/editor/accept_ajax_scenario/",
                                    body,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.post("/editor/accept_ajax_scenario/",
                                    body,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_dump_session(self):
        response = self.client.get("/editor/dump_session/")
        self.assertEqual(response.status_code, 200)

    def test_dump_request(self):
        response = self.client.get("/editor/dump_request/")
        self.assertEqual(response.status_code, 200)

    def test_scenario_details(self):
        file_in = open("editor/static/editor/fixture.json", "r")
        body = file_in.read()
        file_in.close()

        response = self.client.post("/editor/accept_ajax_scenario/",
                                    body,
                                    content_type="application/json")
        response = self.client.get("/editor/scenarios/1/")
        self.assertEqual(response.status_code, 200)
    def test_scenario_graph(self):
        file_in = open("editor/static/editor/fixture.json", "r")
        body = file_in.read()
        file_in.close()

        response = self.client.post("/editor/accept_ajax_scenario/",
                                    body,
                                    content_type="application/json")
        response = self.client.get("/editor/scenarios/1/graph/")
        self.assertEqual(response.status_code, 200)
