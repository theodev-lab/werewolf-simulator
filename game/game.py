import random
import numpy as np
from game.player import Player
from game.roles import Role

class Game:
	def __init__(self, n_players, n_wolves):
		self.n_players = n_players
		self.n_wolves = n_wolves
		
		self.players = self._init_players()
		self.suspicion = np.zeros((self.n_players, self.n_players))  # player's suspicion toward each other player
		
	def _init_players(self):
		roles = [Role.WOLF] * self.n_wolves + [Role.VILLAGER] * (self.n_players - self.n_wolves)
		random.shuffle(roles)
		return [Player(i, role) for i, role in enumerate(roles)]
	
	def alive_players(self):
		return [p for p in self.players if p.alive]

	def night_phase(self):
		villagers = [p for p in self.players if p.role == Role.VILLAGER and p.alive]
		
		if villagers:
			target = random.choice(villagers)
			target.alive = False

	def day_phase(self):
		votes = {}
		
		for p in self.alive_players():
			vote = p.vote(self.players, self.suspicion[p.id])
			votes[vote] = votes.get(vote, 0) + 1
		
		if votes:
			target_id = max(votes, key=votes.get)
			self.players[target_id].alive = False
	
	def is_over(self):
		wolves = [p for p in self.players if p.role == Role.WOLF and p.alive]
		villagers = [p for p in self.players if p.role == Role.VILLAGER and p.alive]
		
		if not wolves:
			return True, "villagers"
		elif len(wolves) >= len(villagers): # we assume that there is only 2 camps : villagers and wolves
			return True, "wolves"
		else:
			return False, None

	def play(self):
		while True:
			self.night_phase()
			self.day_phase()
			
			over, winner = self.is_over()
			if over:
				return winner