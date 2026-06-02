from game.game import Game
from game import texts

class Simulator:
    def __init__(self, role_counts, n_games):
        self.role_counts = role_counts
        self.n_games = n_games

    def run(self):
        results = {texts.VILLAGERS: 0, texts.WOLVES: 0}

        if self.role_counts.get("cupid", 0) > 0:
            results[texts.LOVERS] = 0
        
        for _ in range(self.n_games):
            game = Game(self.role_counts)
            winner = game.play()
            results[winner] += 1
            
            if self.n_games == 1:
                for line in game.history:
                    print(line)
        
        return results
