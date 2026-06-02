import random
from game.player import Player
from game.suspicion import SuspicionManager
from game.phases import night_phase, day_phase
from game import texts
from roles import ROLE_MAP, Villager

class Game:
	def __init__(self, role_counts):
		self.role_counts = role_counts
		self.n_players = sum(role_counts.values())
		self.players = self.init_players()
		
		self.suspicion = SuspicionManager(self.n_players)
		
		self.history = []
		self.dead_this_night = []
		self.current_day = 0
		
	def log(self, message):
		self.history.append(message)
	
	def init_players(self):
		roles_deck = []
  
		for role_name, count in self.role_counts.items():
			RoleClass = ROLE_MAP[role_name]
			roles_deck.extend([RoleClass() for _ in range(count)])

		if self.role_counts.get("thief", 0) > 0:
			roles_deck.extend([Villager() for _ in range(2)])
		
		random.shuffle(roles_deck)

		dealt_roles = roles_deck[:self.n_players]
		self.remaining_roles = roles_deck[self.n_players:]
  
		return [Player(i, role) for i, role in enumerate(dealt_roles)]

	def alive_players(self):
		return [p for p in self.players if p.alive]

	def kill_player(self, player):
		if player.alive:
			player.alive = False
			self.dead_this_night.append(player)

			if player.lover is not None and player.lover.alive:
				game_lover = player.lover
				self.log(texts.LOVER_GRIEF.format(lover_id=game_lover.id, role_name=game_lover.role.__class__.__name__, dead_id=player.id))
				self.kill_player(game_lover)
	
	def is_over(self):
		alive_players = self.alive_players()
		n_wolves = sum(p.role.camp == texts.WOLVES and p.alive for p in self.players)
		n_villagers = sum(p.role.camp == texts.VILLAGERS and p.alive for p in self.players)
		
		if len(alive_players) == 2 and alive_players[0].lover is alive_players[1] and alive_players[1].lover is alive_players[0]:
			return True, texts.LOVERS
		elif n_wolves == 0:
			return True, texts.VILLAGERS
		elif n_wolves >= n_villagers:
			return True, texts.WOLVES
		else:
			return False, None
		
	def play(self):
		self.log(texts.GAME_START)

		while True:
			self.current_day += 1

			night_phase(self)
			day_phase(self)
   
			over, winner = self.is_over()
   
			if over:
				break

		self.log(f"\n{texts.GAME_OVER.format(winner=winner)}")

		return winner
