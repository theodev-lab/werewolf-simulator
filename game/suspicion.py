import numpy as np

class SuspicionManager:
    def __init__(self, n_players):
        self.suspicion = np.zeros((n_players, n_players)) # suspicion matrix: level of suspicion each player has towards every other player (used for voting behavior)
        self.grudge = np.zeros((n_players, n_players)) # grudge matrix: personal resentment towards other players used as a voting bias in addition to suspicion
        
    def get_accusation_scores(self, player_id):
        return np.clip(self.suspicion[player_id] + self.grudge[player_id], 0, 1)
    
    def apply_influence(self, listener_id, target_id, influence):
        self.suspicion[listener_id][target_id] += influence
        self.suspicion[listener_id][target_id] = max(0, min(1, self.suspicion[listener_id][target_id]))
        
    def apply_grudge(self, alive_players, current_day):
        self.grudge.fill(0)
        
        for p in alive_players:
            for attacker_id, days in p.memory.items():
                for day in days:
                    d = current_day - day
                    if d > 0:
                        self.grudge[p.id][attacker_id] += p.paranoia * (0.5 ** d)
                
                self.grudge[p.id][attacker_id] = min(1.0, self.grudge[p.id][attacker_id])