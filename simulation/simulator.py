from game.game import Game

class Simulator:
	def __init__(self, n_players, n_wolves, n_games):
		self.n_players = n_players
		self.n_wolves = n_wolves
		self.n_games = n_games

	def run(self):
		results = {"villagers": 0, "wolves": 0}
		
		for _ in range(self.n_games):
			game = Game(self.n_players, self.n_wolves)
			winner = game.play()
			results[winner] += 1
		
		return results