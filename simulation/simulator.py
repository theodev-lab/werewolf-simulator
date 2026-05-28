from game.game import Game

class Simulator:
    def __init__(self, role_counts, n_games):
        self.role_counts = role_counts
        self.n_games = n_games

    def run(self):
        results = {"villagers": 0, "wolves": 0}
        
        for _ in range(self.n_games):
            game = Game(self.role_counts)
            winner = game.play()
            results[winner] += 1
        
        return results