import numpy as np
import random

class Player:
    def __init__(self, id, role):
        self.id = id
        self.role = role # "wolf" or "villager"
        self.alive = True
        self.convince = np.random.normal(0, 1) # personality traits

    def vote(self, players, suspicion_row):
        candidates = [p for p in players if p.alive and p.id != self.id]
  
  		# score = player's suspicion toward the other player + random noise to introduce variability in voting behavior
    
        scores = []
        for p in candidates:
            score = suspicion_row[p.id] + random.random() #
            scores.append((score, p.id))

        return max(scores)[1]