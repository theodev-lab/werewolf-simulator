import numpy as np
import random
from config import VOTE_NOISE

class Player:
    def __init__(self, id, role):
        self.id = id
        self.role = role
        self.alive = True
        self.convince = np.random.normal(0, 1) # personality traits

    def vote(self, players, suspicion_row):
        if self.role.camp == "loups-garous":
            candidates = [p for p in players if p.alive and p.id != self.id and p.role.camp != "loups-garous"]
        else:
            candidates = [p for p in players if p.alive and p.id != self.id]
  
  		# score = player's suspicion toward the other player + random noise to introduce variability in voting behavior
    
        scores = []
        for p in candidates:
            score = suspicion_row[p.id] + (random.random() * VOTE_NOISE)
            scores.append((score, p.id))

        return max(scores)[1]