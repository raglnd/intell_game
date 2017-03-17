'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com/

        /game/tests.py
            Django TestCase's
                GameTestCase
                    test_start_next_turn
                    test_games_init
                    test_add_player
                    test_start_game
                PlayerTestCase
                    test_create_player
                ProcessActionTestCase
                    test_tail_action
                    test_investigate_action
                    test_check_action
                    test_misinf_action <- not implemented
                    test_recruit_action
                    test_apprehend_action
                    test_research_action
                    test_terminate_action

        TODO: add other model test cases
        TODO: add routing/templates/view test cases
        TODO: add documentation for which test maps to which TestCase
'''
from django.test import TestCase
from .models import *
from editor.models import Scenario
from django.contrib.auth.models import User
from django.test import Client
from datetime import timedelta
import json
from casper.tests import CasperTestCase
import os.path

# Create your tests here.
'''
GameTestCase
    used to test game model
        test_start_next_turn
        test_games_init
        test_add_player
        test_start_game
'''
class  GameTestCase(TestCase):
    def setUp(self):
        Scenario.objects.create(name="test",
                                turn_num=20,
                                point_num=20,
                                file_name="fixture.json")
        Game.objects.create(scenario=Scenario.objects.all()[0])

    def test_knowledge_model(self):
        knowledge = Knowledge(turn=10)
        knowledge.save()
        str(knowledge)

    def test_start_next_turn(self):
        '''test turn timing function works'''
        game = Game.objects.get(pk=1)
        u1 = User.objects.create_user("user1",
                                      "user1@intellproject.com",
                                      "1234pass")
        u1.save()
        game.add_player(u1)

        self.assertEqual(game.started, False)
        next_turn = game.next_turn
        self.assertEqual(next_turn, None)

        #start game
        game.start()
        self.assertEqual(game.started, True)
        self.assertNotEqual(game.next_turn, next_turn)

        next_turn = game.next_turn

        self.assertEqual(game.turn, 1)
        game.start_next_turn()
        self.assertEqual(game.turn, 2)
        self.assertNotEqual(game.next_turn, next_turn)

        next_turn = game.next_turn

        self.assertEqual(game.turn, 2)
        game.start_next_turn()
        self.assertEqual(game.turn, 3)
        self.assertNotEqual(game.next_turn, next_turn)
        #self.assertAlmostEqual(game.next_turn.timestamp(), (next_turn+game.turn_length).timestamp())

        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        action = Action(acttype="research")
        action.save()
        agent.action = action

        game.start_next_turn()

        player.points = 0
        player.save()
        action = Action(acttype="tail", acttarget=1)
        action.save()
        agent.action = action

        game.start_next_turn()

    def test_games_init(self):
        '''test game initialized'''
        game = Game.objects.get(pk=1)
        scenario = game.scenario

        self.assertEqual(scenario.name, "test")
        self.assertEqual(scenario.turn_num, 20)
        self.assertEqual(scenario.point_num, 20)
        self.assertEqual(scenario.file_name, "fixture.json")
        self.assertEqual(game.started, False)

    def test_add_player(self):
        '''test that a user can only join a game once'''
        game = Game.objects.get(pk=1)

        u1 = User(username="user1", first_name="Test 1")
        u2 = User(username="user2", first_name="Test 2")
        u3 = User(username="user3", first_name="Test 3")

        u1.save()
        u2.save()
        u3.save()

        self.assertEqual(len(game.player_set.all()), 0)

        game.add_player(u1)
        game.add_player(u2)
        game.add_player(u3)

        self.assertEqual(len(game.player_set.all()), 3)
        self.assertEqual(game.player_set.all()[0].user.username, "user1")

        game.add_player(u1)
        game.add_player(u2)
        game.add_player(u3)

        self.assertEqual(len(game.player_set.all()), 3)

    def test_start_game(self):
        '''test games start correctly'''
        game = Game.objects.get(pk=1)

        game.start()
        self.assertEqual(game.started, True)

'''
PlayerTestCase
    used to test Player model
        test_create_player
'''
class PlayerTestCase(TestCase):
    def test_create_player(self):
        '''test creating player'''
        u1 = User(username="user1", first_name="Test 1")
        u1.save()
        scenario = Scenario(name="test",
                            turn_num=20,
                            point_num=20,
                            file_name="fixture.json")
        scenario.save()
        game = Game.objects.create(scenario=scenario)
        game.save()
        player = Player(user=u1, game=game)
        player.save()

        self.assertEqual(len(Player.objects.all()), 1)
        self.assertEqual(player.user.username, "user1")

'''
ProcessActionsTestCase
    used to test action processing
        test_tail_action
        test_investigate_action
        test_check_action
        test_misinf_action <- not implemented
        test_recruit_action
        test_apprehend_action
        test_research_action
        test_terminate_action
'''
class ProcessActionsTestCase(TestCase):
    def setUp(self):
        u1 = User(username="user1", first_name="Test 1")
        u2 = User(username="user2", first_name="Test 2")
        u3 = User(username="user3", first_name="Test 3")

        u1.save()
        u2.save()
        u3.save()

        #fixture scenario
        c = Client()
        file_in = open("editor/static/editor/fixture.json", 'r')
        body = file_in.read()
        file_in.close()
        response = c.post("/editor/accept_ajax_scenario/",
                          content_type="application/json",
                          data=body)
        game = Game(scenario=Scenario.objects.all()[0])
        game.save()
        game.add_player(u1)
        game.add_player(u2)
        game.add_player(u3)
        game.start()           

    def test_tail_action(self):
        '''test tail action'''
        game = Game.objects.all()[0]
        ted = Character.objects.get(name="Ted Kaczynski")
        #targeting character ted kazinski
        action = Action(acttype="tail", acttarget=ted.pk)
        action.save()
        #using player 1's 1st agent (only at this point)
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        #first turn involving ted is 9
        game.turn = 9
        game.save()

        point_count = player.points
        knowledge_count = len(player.get_knowledge())
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["tail"])
        #new knowledge?
        self.assertNotEqual(len(player.get_knowledge()), knowledge_count)

        game.turn = 0
        game.save()

        #create a character not in the scenario
        michael = Character(name="Michael", key=False, notes="")
        michael.save()
        action.acttarget = michael.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

    def test_tail_succeed(self):
        '''test a tail action that finds a hidden description'''
        #add target event/descriptions/character
        d_public = Description(name="public description",
                               text="Anyone can see this",
                               key=True,
                               hidden=False)
        d_public.save()
        d_private = Description(name="private description",
                                text="Must tail character/investigate loc",
                                key=True,
                                hidden=True)
        d_private.save()

        event = Event(turn=0, scenario=Scenario.objects.all()[0], misinf=False)
        event.save()

        db_public = DescribedBy(event=event, description=d_public)
        db_public.save()
        db_private = DescribedBy(event=event, description=d_private)
        db_public.save()

        character = Character(name="Follow Me", key=True, notes="")
        character.save()

        involved = Involved(event=event, character=character)
        involved.save()

        #try to investigate
        game = Game.objects.all()[0]
        action = Action(acttype="tail", acttarget=character.pk)
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()

        #sanity check (other test should cover this)
        self.assertEqual(game.is_target_valid(action), True)

        #check that knowledge and message objects created
        pre_knowledge = len(player.get_knowledge())
        pre_messages = len(player.get_messages())

        game.perform_action(action)

        player.refresh_from_db()

        post_knowledge = len(player.get_knowledge())
        post_messages = len(player.get_messages())

        self.assertEqual(pre_knowledge+1, post_knowledge)
        self.assertEqual(pre_messages+1, post_messages)

    def test_investigate_action(self):
        '''test investigate action'''
        game = Game.objects.all()[0]
        seattle = Location.objects.get(name="Seattle")
        #targeting location seattle
        action = Action(acttype="investigate", acttarget=seattle.pk)
        action.save()
        #using player 1's 1st agent (only at this point)
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        #first seattle turn is 7
        game.turn = 8
        game.save()

        point_count = player.points
        knowledge_count = len(player.get_knowledge())
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["investigate"])
        #new knowledge?
        self.assertNotEqual(len(player.get_knowledge()), knowledge_count)

        game.turn = 0
        game.save()

        action.acttarget = Location.objects.get(name="SanFrancisco").pk
        action.save()
        self.assertEqual(game.is_target_valid(action), False)

        #create a location not in the scenario
        moon = Location(name="The Moon", x=0, y=0)
        moon.save()
        action.acttarget = moon.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

    def test_investigate_succeed(self):
        '''test an investigate action that finds a hidden description'''
        #add target event/descriptions/character
        d_public = Description(name="public description",
                               text="Anyone can see this",
                               key=True,
                               hidden=False)
        d_public.save()
        d_private = Description(name="private description",
                                text="Must tail character/investigate loc",
                                key=True,
                                hidden=True)
        d_private.save()

        event = Event(turn=0, scenario=Scenario.objects.all()[0], misinf=False)
        event.save()

        db_public = DescribedBy(event=event, description=d_public)
        db_public.save()
        db_private = DescribedBy(event=event, description=d_private)
        db_public.save()

        location = Location(name="Look here", x=0, y=0)
        location.save()

        happenedat = HappenedAt(event=event, location=location)
        happenedat.save()

        #try to investigate
        game = Game.objects.all()[0]
        action = Action(acttype="investigate", acttarget=location.pk)
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()

        #sanity check (other test should cover this)
        self.assertEqual(game.is_target_valid(action), True)

        #check that knowledge and message objects created
        pre_knowledge = len(player.get_knowledge())
        pre_messages = len(player.get_messages())

        game.perform_action(action)

        player.refresh_from_db()

        post_knowledge = len(player.get_knowledge())
        post_messages = len(player.get_messages())

        self.assertEqual(pre_knowledge+1, post_knowledge)
        self.assertEqual(pre_messages+1, post_messages)

    def test_check_action(self):
        '''test check info action'''
        game = Game.objects.all()[0]
        reserv_cairo = Description.objects.get(
            text__contains="reservations for Cairo"
        )
        #targeting description "Ata hari makes ...."
        action = Action(acttype="check", acttarget=reserv_cairo.pk)
        action.save()
        #using player 1's 1st agent
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["check"])

        #create a description not in the scenario
        jogging = Description(text="Someone went jogging", hidden=False,
                              name="Jogging", key=False)
        jogging.save()
        action.acttarget = jogging.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

    def test_check_succeed(self):
        '''test check action finds bogus info'''
        description = Description(name="bad info",
                                  key=False,
                                  hidden=False,
                                  text="This is bs")
        description.save()

        character = Character.objects.get(name="Ted Kaczynski")
        location = Location.objects.get(name="Seattle")

        event = Event(turn=0, scenario=Scenario.objects.all()[0], misinf=True)
        event.save()

        describedby = DescribedBy(event=event, description=description)
        happenedat = HappenedAt(event=event, location=location)
        involved = Involved(event=event, character=character)
        describedby.save()
        happenedat.save()
        involved.save()

        #try to check
        game = Game.objects.all()[0]
        action = Action(acttype="check", acttarget=description.pk)
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        
        #sanity check (other test should cover this)
        self.assertEqual(game.is_target_valid(action), True)

        #check that knowledge and message objects created
        pre_knowledge = len(player.get_knowledge())
        pre_messages = len(player.get_messages())

        game.perform_action(action)

        player.refresh_from_db()

        post_knowledge = len(player.get_knowledge())
        post_messages = len(player.get_messages())

        self.assertEqual(pre_knowledge+1, post_knowledge)
        self.assertEqual(pre_messages+1, post_messages)


    def test_misinf_action(self):
        '''test create misinf action'''
        game = Game.objects.all()[0]
        action = Action(acttype="misInfo")
        action.actdict = json.dumps({"character":1, 
                                     "location":1, 
                                     "description":""})
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["misInfo"])

    def test_recruit_action(self):
        '''test recruit agent action'''
        game = Game.objects.all()[0]
        action = Action(acttype="recruit")
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #test that player has an additional agent after performing action
        agent_count = len(player.agent_set.all())
        game.perform_action(action)
        self.assertEqual(len(player.agent_set.all()),
                         agent_count+1)
        #check that points deducted correctly
        point_count = player.points
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["recruit"])


    def test_apprehend_action(self):
        '''test apprehend character action'''
        game = Game.objects.all()[0]
        ted = Character.objects.get(name="Ted Kaczynski")
        action = Action(acttype="apprehend", acttarget=ted.pk)
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["apprehend"])

        #create a character not in the scenario
        michael = Character(name="Michael", key=False, notes="")
        michael.save()
        action.acttarget = michael.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

        #try to apprehend a character in the scenario but not involved in plot
        hitler = Character.objects.get(name="Adolf Hitler")
        action.acttarget = hitler.pk
        action.save()
        self.assertTrue(game.is_target_valid(action))


    def test_research_action(self):
        '''test research action'''
        game = Game.objects.all()[0]
        action = Action(acttype="research")
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #test that the player has additionalk points after performing action
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["research"])

    def test_terminate__action(self):
        '''test terminate agent action'''
        game = Game.objects.all()[0]
        p2_agent = game.player_set.all()[1].agent_set.all()[0]
        action = Action(acttype="terminate", acttarget=p2_agent.pk)
        action.save()
        player = game.player_set.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points,
                         point_count-game.ACTION_COSTS["terminate"])

        #create agent not belonging to a player
        dummy_action = Action(acttype="research")
        dummy_action.save()
        agent = Agent(name="", action=dummy_action)
        agent.save()
        action.acttarget = agent.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

'''
GameSiteTestCase
    test_index
    test_games
    test_game_details
    test_create
    test_join
    test_agents
    test_agent_detail
    test_players
    test_player_detail
    test_knowledges
    test_knowledge_detail
'''
class GameListViewsTestCase(TestCase):
    def setUp(self):
        #make game
        file_in = open("editor/static/editor/fixture.json", 'r')
        body = file_in.read()
        file_in.close()
        response = self.client.post("/editor/accept_ajax_scenario/",
                          content_type="application/json",
                          data=body)
        user = User.objects.create_user('user1',
                                        'user1@intellproject.com',
                                        '1234pass')
        game = Game(scenario=Scenario.objects.all()[0], creator=user)
        game.save()
        self.client.force_login(user)

    def test_index(self):
        response = self.client.get("/game/")
        self.assertEqual(response.status_code, 302)

    def test_games(self):
        response = self.client.get("/game/games/")
        self.assertEqual(response.status_code, 200)

    def test_game_details(self):
        response = self.client.get("/game/games/1/")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.get("/game/games/create/")
        self.assertEqual(response.status_code, 200)
        #TODO: create post test

    def test_join(self):
        response = self.client.get("/game/games/1/join/")
        self.assertEqual(response.status_code, 200)
        #TODO test if joined game

    def test_agents(self):
        response = self.client.get("/game/agents/")
        self.assertEqual(response.status_code, 200)

    def test_agent_detail(self):
        #TODO crete agent and test view
        pass

    def test_players(self):
        response = self.client.get("/game/players/")
        self.assertEqual(response.status_code, 200)

    def test_player_detail(self):
        #TODO joing game and test view
        pass

    def test_knowledges(self):
        response = self.client.get("/game/knowledges/")
        self.assertEqual(response.status_code, 200)

    def test_knowledge_detail(self):
        #TODO test view
        pass

    def test_end(self):
        user_owner = User.objects.all()[0]
        user_not_owner = User.objects.create_user("user2",
                                                  "balh@blah.com",
                                                  "1234pass")
        self.client.force_login(user_not_owner)

        response = self.client.get("/game/games/1/end/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content.decode())["deleted"])

        self.client.force_login(user_owner)
        response = self.client.get("/game/games/1/end/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content.decode())["deleted"])
'''
GamePlayViewsTestCase
    test_submit_action
    test_play
    test_get_status
    test_get_snippets
    test_get_characters
    test_get_locations
    test_get_agents
    test_get_own_agents
'''
class GamePlayViewsTestCase(TestCase):
    def setUp(self):
        #make game
        file_in = open("editor/static/editor/fixture.json", 'r')
        body = file_in.read()
        file_in.close()
        response = self.client.post("/editor/accept_ajax_scenario/",
                          content_type="application/json",
                          data=body)
        user = User.objects.create_user('user1', 
                                        'user1@intellproject.com', 
                                        '1234pass')
        game = Game(scenario=Scenario.objects.all()[0], creator=user)
        game.save()
        self.client.force_login(user)
        game.add_player(user)
        game.start()

    def test_submit_action(self):
        player = Game.objects.all()[0].player_set.all()[0]
        agent = player.agent_set.all()[0]
        response = self.client.post("/game/play/1/submit_action/",
                                    content_type="application/json",
                                    data=json.dumps({"action":"research",
                                                     "agent":agent.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "research")
        response = self.client.get("/game/play/1/submit_action/")
        self.assertEqual(response.status_code, 200)

    def test_play(self):
        response = self.client.get("/game/play/1/")
        self.assertEqual(response.status_code, 200)

    def test_get_status(self):
        response = self.client.get("/game/play/1/get_status/")
        self.assertEqual(response.status_code, 200)

    def test_get_snippets(self):
        response = self.client.get("/game/play/1/get_snippets/")
        self.assertEqual(response.status_code, 200)

    def test_get_characters(self):
        response = self.client.get("/game/play/1/get_characters/")
        self.assertEqual(response.status_code, 200)

    def test_get_locations(self):
        response = self.client.get("/game/play/1/get_locations/")
        self.assertEqual(response.status_code, 200)

    def test_get_agents(self):
        response = self.client.get("/game/play/1/get_agents/")
        self.assertEqual(response.status_code, 200)

    def test_get_own_agents(self):
        response = self.client.get("/game/play/1/get_own_agents/")
        self.assertEqual(response.status_code, 200)
    
    def test_end(self):
        response = self.client.get("/game/play/1/end/")

class ActionsTestCase(CasperTestCase):
    def setUp(self):
        #make game
        file_in = open("editor/static/editor/fixture.json", 'r')
        body = file_in.read()
        file_in.close()
        response = self.client.post("/editor/accept_ajax_scenario/",
                          content_type="application/json",
                          data=body)
        user = User.objects.create_user('user1', 
                                        'user1@intellproject.com', 
                                        '1234pass')
        game = Game(scenario=Scenario.objects.all()[0], creator=user)
        game.save()
        self.client.force_login(user)
        game.add_player(user)
        game.start()
        game.start_next_turn()
        game.start_next_turn()
        game.start_next_turn()
        game.start_next_turn()
        game.start_next_turn()
        game.start_next_turn()
        game.start_next_turn()

    def test_actions(self):
        self.assertTrue(self.casper(os.path.join(os.path.dirname(__file__),
            'tests/test-actions.js')))
