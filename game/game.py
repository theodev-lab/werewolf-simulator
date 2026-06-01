import random
from game.player import Player
from game.suspicion import SuspicionManager
from game.phases import night_phase, day_phase
from roles import ROLE_MAP

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
		
		random.shuffle(roles_deck)
  
		return [Player(i, role) for i, role in enumerate(roles_deck)]

	def alive_players(self):
		return [p for p in self.players if p.alive]

	def kill_player(self, player):
		if player.alive:
			player.alive = False
			self.dead_this_night.append(player)
	
	def is_over(self):
		wolves = [p for p in self.players if p.role.camp == "loups-garous" and p.alive]
		villagers = [p for p in self.players if p.role.camp == "villageois" and p.alive]
		
		if not wolves:
			return True, "villageois"
		elif len(wolves) >= len(villagers): # we assume that there are only 2 camps : villagers and wolves 
			return True, "loups-garous"
		else:
			return False, None
		
	def play(self):
		self.log("🎮 La partie vient de commencer !")

		while True:
			self.current_day += 1
			night_phase(self)
   
			over, winner = self.is_over()
   
			if over:
				break

			day_phase(self)
   
			over, winner = self.is_over()
   
			if over:
				break

		self.log(f"\n🏆 La partie est terminée ! Les {winner} ont gagné !")
		return winner