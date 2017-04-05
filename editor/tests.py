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

    TODO:   add more!
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

        petshop = Location.objects.create(name="Pet Shop", x=0, y=0)
        bolton = Location.objects.create(name="Bolton Pet Shop", x=20, y=20)

        original = Description.objects.create(name="original transaction", 
            key=True,
            hidden=False, 
            text="Michael sold john a norwegian blue")
        returnAttempt = Description.objects.create(name="return attempt", 
            key=True, 
            hidden=False, 
            text="John tries to return the parrot but is sent to bolton")
        boltonReturn = Description.objects.create(name="bolton return attempt", 
            key=True,
            hidden=False,
            text="Michael tells john he isnt in bolton but rather ipswitch")
        tooSilly = Description.objects.create(name="the sgt major intervenes", 
            key=True,
            hidden=False,
            text="John believes things are gitting silly and the sgt major agrees")

        e0 = Event.objects.create(turn=0)
        e1 = Event.objects.create(turn=1)
        e2 = Event.objects.create(turn=2)

        DescribedBy.objects.create(event=e0, description=original)
        DescribedBy.objects.create(event=e1, description=returnAttempt)
        DescribedBy.objects.create(event=e2, description=boltonReturn)
        DescribedBy.objects.create(event=e2, description=tooSilly)

        HappenedAt.objects.create(event=e0, location=petshop)
        HappenedAt.objects.create(event=e1, location=petshop)
        HappenedAt.objects.create(event=e2, location=bolton)

        Involved.objects.create(event=e0, character=michael)
        Involved.objects.create(event=e0, character=john)
        Involved.objects.create(event=e1, character=michael)
        Involved.objects.create(event=e1, character=john)
        Involved.objects.create(event=e2, character=michael)
        Involved.objects.create(event=e2, character=john)
        Involved.objects.create(event=e2, character=sgtmajor)

    def test_create_event(self):
        '''test Event created'''
        event = Event.objects.get(turn=0)

        self.assertEqual(event.turn, 0)
        
    def test_single_describedby(self):
        '''test DescribedBy with 1-1 event-description'''
        e0 = Event.objects.get(turn=0)
        originalDB = DescribedBy.objects.get(event=e0)
        description = originalDB.description

        # get not failing implies only one object returned
        self.assertEqual(description.name, "original transaction")

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
        sgtmajor = Character.objects.get(name="Sergeant Major")

        self.assertEqual(michael.name, "Michael")
        self.assertEqual(michael.key, True)
        self.assertEqual(sgtmajor.key, False)

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

        self.assertEqual(krab.name, "The Krusty Krab")
        self.assertEqual(krab.x, 0)
        self.assertEqual(krab.y, 10)

'''
DescriptionTestCase
    test_create_description
'''
class DescriptionTestCase(TestCase):
    def setUp(self):
        Description.objects.create(text="Joe went to the store", hidden=False,
            name="Joe store", key=False)

    def test_create_description(self):
        '''test creating descriptions'''
        joestore = Description.objects.get(name="Joe store")

        self.assertEqual(joestore.name, "Joe store")
        self.assertEqual(joestore.text, "Joe went to the store")
        self.assertEqual(joestore.hidden, False)
        self.assertEqual(joestore.key, False)

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

        #TODO: test number of other things

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
