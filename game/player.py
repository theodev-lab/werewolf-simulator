import numpy as np
import random
from config import VOTE_NOISE

class Player:
    def __init__(self, id, role):
        self.id = id
        self.role = role
        self.alive = True
        
        # personality traits that influence behavior during the game
        self.convince = np.random.normal(0, 1)
        self.paranoia = np.random.beta(2, 3)
        self.memory = {}

    def vote(self, players, suspicion_row):
        candidates = [p for p in players if p.alive and p.id != self.id]
  
        # score = player's suspicion toward the other player + random noise to introduce variability in voting behavior
        scores = [(suspicion_row[p.id] + (random.random() * VOTE_NOISE), p.id) for p in candidates]
        
        return max(scores)[1]