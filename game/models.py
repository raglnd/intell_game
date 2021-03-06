'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

        game/models.py
            Django models for game app
                Player
                Game
                Agent
                Action
                Knowledge
'''

from django.db import models
from editor.models import *
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import datetime, make_aware
from random import random, choice
import json
from django.db.models import Q

# Create your models here.
'''
Player
    used to represent a particular user in a game

    id      -   auto gen primary key
    user    -   user being represented
    points  -   number of intell points left
'''
class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    names = ["Smith", "Brown", "Jones", "Bond", "Bourne", "Elam", "O'Kane",
             "Wright", "Campbell", "Fullington", "Washington", "Piwowarski"]
    researchedThisTurn = models.BooleanField(default=False)	#tracks if a research has been done yet for the given turn or not
    caughtKeyCharacter = models.BooleanField(default=False) #tracks if this player caught the key character, used to determine how many players won when the key character was caught
    numOfLivingAgents = models.IntegerField(default=0) #tracks how many agents the player has left. Increased by one when adding an agent, decreased by one when an agent is assassinated

    def __str__(self):
        return "player controlled by %s"%(self.user.username)

    def add_agent(self):
        action = Action()
        action.save()

        curr_agent_names = [agent.name for agent in self.agent_set.all()]
        
        if len(curr_agent_names) == len(self.names):
            name = "X"
        else:
            name = choice(self.names)
            while name in curr_agent_names:
                name = choice(self.names)

        agent = Agent(name=name,
                      alive=True, 
                      action=action, 
                      player=self)
        agent.save()
        self.numOfLivingAgents += 1
        self.save()

    '''
    get_knowledge
        returns the QuerySet of all Knowledge objects associated with
        the player
    '''
    def get_knowledge(self):
        return Knowledge.objects.filter(player=self).all()

    '''
    get_messages
        returns QuerySet of all Message objects associated with
        the player
    '''
    def get_messages(self):
        return Message.objects.filter(player=self).all()

'''
Game
    used to represent a particular game.

    id -    auto gen primary key
    scenario - scenario being used by the game. Used to determine
                which snippets are presented and win conditions
    started - indicates if the game has started or not. Used to
                determine if players may join and where to put
                the game in the game list view
	gameOver - Flags when the game should delete itself on the next
				turn after either a player has won or all players have
				lost
    creator - User who configured the game. They should have the
                ability to manage it (down the line. at this point
                they will not)
    turn - current turn
    next_turn - datetime of the next turn. When this time is reached
                the game should generate the next round of snippets
                and allow players to access them. Also proccess any
                player actions and determine side effects
    turn-length - dimedelta which determines when the next turn will
                    be. When the turn changes the next_turn field will
                    get this delta added to it
methods
    detail_html - temp used for prototype page
    add_player  - add player to players
    time_till - till next turn. used for nice countdown page
    start - sets started and inits next_turn
    start_next_turn - does turn proccessing
'''
class Game(models.Model):
	scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
	started = models.BooleanField(default=False)
	gameOver = models.BooleanField(default=False)
	creator = models.ForeignKey(User, null=True)
	turn = models.IntegerField(default=0)
	next_turn = models.DateTimeField(null=True)
	turn_length = models.DurationField(default=timedelta(days=1))

	# TODO: make these configured in game create?
	#       would require more fields default values are same
	ACTION_COSTS = {"tail": 1, "investigate": 1, "misInfo": 1, "check": 1,
					"recruit": 3, "apprehend": 5, "terminate": 5,
					"research": -2}
	ACTION_SUCC_RATE = {"tail": 1, "investigate": 1, "misInfo": 1, "check": 1,
						"recruit": 1, "apprehend": .85, "terminate": .7,
						"research": 1}

	def __str__(self):
		return "Game using scenario %s" % (self.scenario.name)

	def detail_html(self):
		return "scenario: "+str(self.scenario)

	def get_users(self):
		users = []
		for player in self.player_set.all():
			users += [player.user]
		return users
	'''
	add_player
		I: player - a user object
		O: player created and
			is added to the players field if the game has not started
			and the player is not in the game already
			otherwise no change
	'''
	def add_player(self, user):
		if user not in self.get_users():
			player = Player(user=user, 
							game=self, 
							points=self.scenario.point_num)
			player.save()

	'''
	time_till
		I:
		O:  if next_turn is defined then return the time till the first turn
			or the time till the next turn
	'''
	def time_till(self):
		now = make_aware(datetime.now())
		if self.next_turn is not None:
			# otherwise get large ugly number of seconds
			till = self.next_turn - now
			return till.seconds

	'''
	is_target_valid
		I:  an action
		O:  bool representing if the action is valid (acttarget exists in
			the appropriate table in the appropriate game
			If an invalid action is sent generate a Message object for
			the player
	'''
	def is_target_valid(self, action):
		acttype = action.acttype
		acttarget = action.acttarget
		player = action.agent_set.all()[0].player
		message = Message(player=player, turn=self.turn)

		# determine target table
		# this is evil TODO: change it to if/elif/else
		try:
			target_table = {"tail": Character,
							"investigate": Location,
							"check": Description,
							"misInfo": None,
							"recruit": None,
							"apprehend": Character,
							"research": None,
							"terminate": Agent}[acttype]
		except (KeyError):
			message.text = "bad action type"
			message.save()
			return False


		if target_table is not None:
			targets = target_table.objects.filter(pk=acttarget)
			# should only match one target
			if len(targets) == 1:
				target = targets[0]
				# is the target in the scenario for this game
				events = self.scenario.event_set.all()
				if target_table == Character:
					# find events involving the character in this game
					event_qset = events.filter(
						involved=Involved.objects.filter(
							character=target
						)
					)
				elif target_table == Location:
					# find events happenedat the location in this game
					event_qset = events.filter(
						happenedat=HappenedAt.objects.filter(
							location=target
						)
					)
				elif target_table == Description:
					# find events describedby the description in this game
					event_qset = events.filter(
						describedby=DescribedBy.objects.filter(
							description=target
							)
					)
				elif target_table == Agent:
					# find agents in this game
					agent_qset = Agent.objects.filter(
						player__in=self.player_set.all()
					)
					if target in agent_qset.all():
						return True
					else:
						message.text = "Agent not found"
						message.save()
						return False
				else:  # pragma: no cover
					message.text = "target table not found"
					messave.save()
					return False

				if len(event_qset) != 0:
					return True
				else:
					message.text = "Event not found"
					message.save()
					return False
			else:  # pragma: no cover
				message.text = "ambiguous target pk"
				message.save()
				return False
		else:
			if acttype == "misInfo":
				#Spring 2017 - Removed unncessary references to character and location.
				actdict = json.loads(action.actdict)
				text = actdict["description"]
				return True

			# any invalid acttype will throw a key error
			# so dont worry about bad acttype
			return True

	'''
	start_next_turn
		I:
		O:  increment turn counter, proccess actions, produce snippets,
			set next turn time
	'''
	def start_next_turn(self):
		#Spring 2017
		#Delete game if gameOver was set by the last turn
		if (self.gameOver == True):
			for player in self.player_set.all():
				message = Message(player=player, turn=self.turn,
									  text="The game has now ended. Please exit at your convenience.")
				message.save()
			self.delete()
			return
		
		# next turn
		self.turn += 1

		for player in self.player_set.all():
			# Spring 2017 - If the player has no living agents left, they must research until they have the points to recruit an agent.
			if (player.numOfLivingAgents == 0):
				if (player.points >= self.ACTION_COSTS["recruit"]):
					#Recruit a new agent for the player
					player.add_agent()
					#Subtract the cost for recruitment, but also take away points gained from a research, since this agent will automatically do a research as well.
					player.points -= (self.ACTION_COSTS["recruit"] - self.ACTION_COSTS["research"])
					message = Message(player=player, turn=self.turn,
									  text="Automatically recruiting an agent this turn.")
					message.save()
				else:
					#Research for the player
					player.points -= self.ACTION_COSTS["research"]
					message = Message(player=player, turn=self.turn,
									  text="Automatically researching this turn.")
					message.save()
				player.save()

		# process actions
		agents_to_proc = []
		check_for_assassinate = []
		for player in self.player_set.all():
			#Spring 2017 - Do assassinate here to avoid bug where only the first player's agents were killable. Also add agents to list for processing other actions.
			check_for_assassinate = Agent.objects.filter(player=player, alive=True)
			agents_to_proc += check_for_assassinate #Add agents to total group for processing later
			for agent in check_for_assassinate:
				acttype = agent.action.acttype
				if acttype == "terminate":
					if player.points >= self.ACTION_COSTS["terminate"]:
						message = Message()
						message.player = player
						message.turn = self.turn
						killedAgent = Agent.objects.get(pk=agent.action.acttarget)
						if (killedAgent.alive == True):						#Refund points if target is dead already.
							if (random() < self.ACTION_SUCC_RATE[agent.action.acttype]):
								message.text = "Opposing agent terminated"
								terminatePlayer = killedAgent.player
								killedAgent.kill()
								#Spring 2017 - Make it so that a player's number of agents is counted.
								terminatePlayer.numOfLivingAgents -= 1
								terminatePlayer.save()

								#Spring 2017
								#Alert the player of the terminated agent that their agent is dead. If they have no more agents,
								#they are told that they must research until they have the points to recruit an agent.
								if (terminatePlayer.numOfLivingAgents == 0):
										assassinateMessage = Message(player=killedAgent.player, turn=self.turn,
																		text="Your last agent was assassinated by another player! Until you have the points to recruit another agent, you will research every turn.")
								else:
										assassinateMessage = Message(player=killedAgent.player, turn=self.turn,
																		text="One of your agents was assassinated by an enemy player!")
								assassinateMessage.save()
							else:
								message.text = "Opposing agent not terminated"
						else:
							message.text = "The opposing agent was already killed. Refunding action points."
							player.points += self.ACTION_COSTS["terminate"]
							player.save()
						message.save()
					else:
						#Do nothing. The message will be handled below.
						pass

		#TODO: decide on order of agents?
		for agent in agents_to_proc:
			acttype = agent.action.acttype
			if acttype in self.ACTION_COSTS.keys():
				#can player afford it?
				#TODO: player with multiple agents - can they afford
				#       all actions? if not how to decide?
				#       first (agent) come first served?
				if agent.player.points >= self.ACTION_COSTS[acttype]:
					#is the target valid?
					if self.is_target_valid(agent.action):
						self.perform_action(agent.action)
					else:
						#action target invalid
						#message generated by is_target_valid
						pass
				else:
					#player has too few points, perform research instead
					message = Message(player=agent.player, turn=self.turn,
									  text="Too few points to perform %s, researching instead."%(agent.action))
					message.save()
					action = Action(acttype="research")
					action.save()
					agent.action = action
					agent.save()
					self.perform_action(agent.action)
			else:
				#Spring 2017
				#If the action doesn't exist, make it a research action.
				action = Action(acttype="research")
				action.save()
				agent.action = action
				agent.save()
				self.perform_action(agent.action)
			
			#After preforming the action, set the default action for next turn to research.
			action = Action(acttype="research")
			action.save()
			agent.action = action
			agent.save()

		#Spring 2017
		#reset all player's researchedThisTurn to false
		for player in self.player_set.all():
			player.researchedThisTurn = False
			player.save()
		
		#Spring 2017
		#If gameOver = True at this point, then that means that a player has caught the key character.
		#Loop over all players and tell those who caught the key character that they won. Everyone else lost.
		if self.gameOver:
			for player in self.player_set.all():
				if player.caughtKeyCharacter:
					pass
				else:
					loseMessage = Message(player=allPlayers, turn=self.turn,
											text="Another player has captured the key target. You lose. The game will end shortly.")
					loseMessage.save()

		#Spring 2017
		#determine if the game is over or not
		if ((self.turn > self.scenario.turn_num) and (self.gameOver == False)): #the players ran out of turns to catch the key character
			#display a message to all players informing them that they lost
			for player in self.player_set.all():
				loseMessage = Message(player=player, turn=self.turn,
									text="The game has exceeded the maximum number of turns. The target has succeeded in their goal. You lose. The game will end shortly.")
				loseMessage.save()
			self.gameOver = True
			
		self.next_turn = self.next_turn + self.turn_length

		#store in db
		self.save()

	'''
	perform_action
		I:  an action that has been verified
		O:  action performed, knowledge created,
			side effects effected

		If the action is valid (assumed) then the action will
		succeed (oh hello hubris)

		TODO: tail, investigate, checInfomisinf, apprehend, terminate
	'''
	def perform_action(self, action):
		player = action.agent_set.all()[0].player
		
		message = Message()
		message.player = player
		message.turn = self.turn
		if action.acttype == "tail":
			involveds = Involved.objects.filter(
				character__id=action.acttarget
			)
			for involved in involveds.all():
				if involved.event.turn <= self.turn:
					knowledge = Knowledge(player=player, turn=self.turn,
										  event=involved.event)
					knowledge.save()
					describedbys = DescribedBy.objects.filter(
						event=involved.event
					)
					for describedby in describedbys.all():
						if describedby.description.hidden:
							#TODO fix this
							message.text = "Tailing %s discovered that %s"%(
								Character.objects.get(pk=action.acttarget),
								describedby.description
							)
						else:
							message.text = "Tailing %s discovered nothing"%(
								Character.objects.get(pk=action.acttarget)
							)
						message.save()
		elif action.acttype == "investigate":
			happenedats = HappenedAt.objects.filter(
				location__id=action.acttarget
			)
			for happenedat in happenedats:
				if happenedat.event.turn <= self.turn:
					knowledge = Knowledge(player=player, turn=self.turn,
										  event=happenedat.event)
					knowledge.save()
					describedbys = DescribedBy.objects.filter(
						event=happenedat.event
					)
					for describedby in describedbys.all():
						if describedby.description.hidden:
							#TODO fix this
							message.text = "Investigation into %s discovered that %s"%(
								Location.objects.get(pk=action.acttarget),
								describedby.description
							)
						else:
							message.text = "Investigation into %s discovered nothing"%(
								Location.objects.get(pk=action.acttarget)
							)
						message.save()
		elif action.acttype == "check":
			describedby = DescribedBy.objects.get(
				description__id=action.acttarget
			)
			if describedby.event.turn <= self.turn:
				knowledge = Knowledge(player=player, turn=self.turn,
									  event=describedby.event)
				knowledge.save()
				if describedby.event.misinf:
					#TODO: fix this
					message.text = "The information that '%s' has been proven to be false"%(
						Description.objects.get(pk=action.acttarget)
					)
				else:
					message.text = "The information that '%s' has been proven to be true"%(
						Description.objects.get(pk=action.acttarget)
					)
				message.save()
		elif action.acttype == "misInfo":
			#Spring 2017 - Removed unnecessary references to character and location.
			target_dict = json.loads(action.actdict)
			description_text = target_dict["description"]

			## -1 fixes timing
			event = Event(turn=self.turn, misinf=True)
			event.scenario = self.scenario
			event.save()

			description = Description(text=description_text,
									  key=False,
									  hidden=False)
			description.save()

			describedby = DescribedBy(event=event,
									  description=description)
			describedby.save()
			
			knowledge = Knowledge(player=player, turn=self.turn,
								  event=event)
			knowledge.save()
			
			misinfo = Misinformation(game=self, event=event)
			misinfo.save()

			message.text = "Misinformation that '%s' succesfully disseminated"%(
				description_text
			)
			message.save()
		elif action.acttype == "recruit":
			#player gets another agent
			#TODO: test to ensure new agents cant act
			#       also that dummy action created has no side effects
			#       (should just be recorded as an invalid action by
			#        game.Game.start_next_turn)
			player.add_agent()
			message.text = "Agent recruited"
			message.save()
		elif action.acttype == "apprehend":
			character = Character.objects.get(pk=action.acttarget)
			if (random() < self.ACTION_SUCC_RATE[action.acttype]):
				if character.key:
					#Flag the player as having caught the key character. Check after all agents
					#have gone through this point to see how many winning players there are.
					message.text = "You captured %s! You win! The game will end shortly."%(character)
					player.caughtKeyCharacter = True
					self.gameOver = True
					self.save()
				else:
					message.text = "%s captured. They are not part of the plot, so they were released."%(
						character
					)
			else:
				message.text = "%s escaped capture attempt"%(character)
			message.save()
		elif action.acttype == "research":
			#only need to sub (negative) action cost from player if they haven't researched yet
			
			#Spring 2017
			if (player.researchedThisTurn):
				player.points += self.ACTION_COSTS[action.acttype]; #add back the points gained from researching
			else:
				player.researchedThisTurn = True
			player.save()
		elif action.acttype == "terminate":
			#Spring 2017 - Do this in the next_turn function instead of here to fix issues with only the first player who joins a game
			#being able to have their agents killed. Add back the points that are about to be lost, since they were subtracted earlier.
			#Spring 2017 - Termination seems to cause no loss of points.
			#player.points += self.ACTION_COSTS[action.acttype]
			#player.save()
			pass
		player.points -= self.ACTION_COSTS[action.acttype]
		player.save()

	'''
	start
		I:
		O:  started becomes true
			sideffects: players are initialized, start_next_turn used to
			make next turn environment (turn counter, actions, snippets)
			initial agents are created, max turns for the game is set
	'''
	def start(self):
		#init players
		for player in self.player_set.all():
			#all players get an agent
			player.add_agent()
			
			#Spring 2017
			#remove the number of points generated by research, as a research is
			#performed automatically at the start of the game
			player.points += self.ACTION_COSTS["research"]
			player.save()

		#init game
		self.started = True
		self.next_turn = make_aware(datetime.now())
		self.gameOver = False
		self.save()

		#init first turn 
		self.start_next_turn()

	'''
	get_snippets
	'''
	def get_snippets(self):
		events = Event.objects.filter(scenario=self.scenario,
									  turn__lt=self.turn+1)
		misinf = Misinformation.objects.filter(game=self)
		misinfevents = [mis.event for mis in misinf]
		##build presented events
		present = []
		for event in events:
			if event.misinf:
				if event in misinfevents:
					present.append(event)
			else:
				present.append(event)
		return present

	'''
	check_game
		I:
		O:
	'''
	def check_game(self):
		current_time = make_aware(datetime.now())
		if current_time > self.next_turn:
			if self.started:
				self.start_next_turn()
			else:
				self.start()


'''
Action
    model tracking an action's target(s)/info

    id          -   auto gen primary key
    acttype     -   type of action TODO: fix this
    acttarget   -   target of action
                    is the pk of the intended target game processing step
                    should determine if target is legal
'''
class Action(models.Model):
    acttype = models.CharField(max_length=64) #this is obviously not right
    acttarget = models.IntegerField(default=-1)
    #double text field length for safety
    actdict = models.CharField(max_length=1024, null=True)

    def __str__(self):
        return "Action %s"%(self.acttype)
'''
Agent
    model tracking an Agent's status

    id      -   auto gen primary key
    name    -   Agent name (meaningless but pretty)
    action  -   current action for agent to perform on turn proccessing
    alive   -   is the agent alive
    location-   where the agent is
    player  -   player controlling this agent
'''
class Agent(models.Model):
	name = models.CharField(max_length=64)
	action = models.ForeignKey(Action, on_delete=models.CASCADE)
	alive = models.BooleanField(default=True)
	location = models.ManyToManyField(Location)
	#a null player is an orphaned
	#   agent-they cant perform
	#   actions
	player = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return "Agent %s"%(str(self.name))
		
	def kill(self):
		self.alive = False
		self.save()

'''
Knowledge
    model relating Players to Events. issued when a player performs an
    investigation on an Event

    event   -   Event model investigated
    turn    -   turn investigation occoured on
'''
class Knowledge(models.Model):
    event = models.ForeignKey(Event, null=True)
    turn = models.IntegerField()
    player = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "result of investigation of %s on turn %s"%(
            str(self.event), str(self.turn)
        )

'''
Message
    model representing game status messages to be relayed to the player
    on a particular turn. Generated when turn is processed due to:
        errors in action sent
        sucessfull actions
        unsucessfull actions
        agent termination
        ... TODO:add more

    id      -   autogen primary key
    player  -   player owning message
    text    -   text of the message
    turn    -   turn messege was generated on
    ... TODO: add more
'''
class Message(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    text = models.CharField(max_length=512) # is .5KB enough? (hopefully)
    turn = models.IntegerField()

    def __str__(self):
        return self.text

'''
Misinformation
    model representing misinfo. needed to prevent scenarios from being
    corrupted by games

    id
    event
    game
'''
class Misinformation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return "misinfo event %i game %i" % (self.event.id, self.game.id)
