import numpy as np
import random

class Player:
    def __init__(self, id, role):
        self.id = id
        self.role = role
        self.alive = True
        self.vote_weight = 1
        
        # personality traits that influence behavior during the game
        self.convince = np.random.normal(0, 1)
        self.paranoia = np.random.beta(2, 3)
        self.memory = {}

    def vote(self, game, suspicion_row):
        lover = game.get_lover(self)
        candidates = [p for p in game.players if p.alive and p.id != self.id and p is not lover]
  
        # score = player's suspicion toward the other player + random noise to introduce variability in voting behavior
        scores = [(suspicion_row[p.id] + (random.random() * game.params.vote_noise), p.id) for p in candidates]
        
        return max(scores)[1]
