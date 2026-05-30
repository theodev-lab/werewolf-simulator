import random
import numpy as np
from game.player import Player
from roles import ROLE_MAP
from config import ALPHA

class Game:
	def __init__(self, role_counts):
		self.role_counts = role_counts
		self.n_players = sum(role_counts.values())
		self.players = self._init_players()
		self.suspicion = np.zeros((self.n_players, self.n_players)) # suspicion matrix: level of suspicion each player has towards every other player (used for voting behavior) 
		self.history = []
		self.dead_this_night = []
		
	def log(self, message):
		self.history.append(message)
	
	def _init_players(self):
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

	def night_phase(self):
		self.dead_this_night = []
		self.log("\n🌙 La nuit tombe sur le village de Thiercelieux...")
		
		self.log("🐺 Les loups-garous vont décider d'une victime à dévorer.")
  
		villagers = [p for p in self.players if p.role.camp == "villageois" and p.alive]
  
		if villagers:
			target = random.choice(villagers)
			self.kill_player(target)
   
	def voting_process(self):
		# 1) Intention phase: players share their suspicions
		intentions = {}
		
		for p in self.alive_players():
			intentions[p.id] = p.vote(self.players, self.suspicion[p.id])
			
		# 2) Debate phase: players try to convince each other (this will influence their votes)
		for speaker in self.alive_players():
			target_id = intentions[speaker.id]
			target = self.players[target_id]
			
			influence = (speaker.convince - target.convince) * ALPHA
			
			for listener in self.alive_players():
				if listener.id != speaker.id and listener.id != target_id:
					self.suspicion[listener.id][target_id] += influence
					self.suspicion[listener.id][target_id] = max(0, min(1, self.suspicion[listener.id][target_id]))
  
		# 3) Voting phase: players vote to eliminate someone
		votes = {}
  
		for p in self.alive_players():
			vote = p.vote(self.players, self.suspicion[p.id])
			votes[vote] = votes.get(vote, 0) + 1
		
		if votes:
			target_id = max(votes, key=votes.get)
			self.log(f"🗳️  Le village a décidé d'éliminer le joueur {target_id} ({self.players[target_id].role.__class__.__name__}).")
			self.kill_player(self.players[target_id])

	def day_phase(self):
		if not self.dead_this_night:
			self.log("☀️  Le village se réveille et personne n'est mort pendant la nuit !")
		else:
			dead_infos = [f"le joueur {p.id} ({p.role.__class__.__name__})" for p in self.dead_this_night]
			
			if len(dead_infos) == 1:
				dead_str = dead_infos[0]
			else:
				dead_str = f"{', '.join(dead_infos[:-1])} et {dead_infos[-1]}"
				
			self.log(f"☀️  Le village se réveille sans... {dead_str}.")

			for p in self.dead_this_night:		
				p.role.on_death(self, p)
		
		self.voting_process()
	
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
			self.night_phase()
			over, winner = self.is_over()
			if over:
				break

			self.day_phase()
			over, winner = self.is_over()
			if over:
				break

		self.log(f"\n🏆 La partie est terminée ! Les {winner} ont gagné !")
		return winner