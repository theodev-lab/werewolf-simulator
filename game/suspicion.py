import numpy as np
from config import DEFAULT_PARAMETERS
from game import texts

class SuspicionManager:
    def __init__(self, players, params=DEFAULT_PARAMETERS):
        self.players = players
        self.params = params
        n_players = len(players)
        self.suspicion = np.zeros((n_players, n_players)) # suspicion matrix: level of suspicion each player has towards every other player (used for voting behavior)
        self.grudge = np.zeros((n_players, n_players)) # grudge matrix: personal resentment towards other players used as a voting bias in addition to suspicion
        self.locked = np.zeros((n_players, n_players), dtype=bool) # locked matrix: whether a player's opinion about another player is fixed and no longer updated (used for special roles that reveal information)
        self.co_vote = np.zeros((n_players, n_players)) # co-vote matrix: how often two players have recently voted for the same target
        
    def get_accusation_scores(self, player_id):
        return np.clip(self.suspicion[player_id] + self.grudge[player_id], 0, 1)

    def lock_cell(self, observer_id, target_id, value):
        self.suspicion[observer_id][target_id] = value
        self.grudge[observer_id][target_id] = 0
        self.locked[observer_id][target_id] = True

    def apply_influence(self, listener_id, target_id, influence):
        if self.locked[listener_id][target_id]:
            return

        if influence > 0 and self.players[listener_id].role.camp == texts.WOLVES and self.players[target_id].role.camp == texts.WOLVES:
            influence *= self.params.wolf_to_wolf_suspicion_resistance

        self.suspicion[listener_id][target_id] += influence
        self.suspicion[listener_id][target_id] = max(0, min(1, self.suspicion[listener_id][target_id]))
        
    def apply_grudge(self, alive_players, current_day):
        self.grudge.fill(0)
        
        for p in alive_players:
            for attacker_id, days in p.memory.items():
                if self.locked[p.id][attacker_id]:
                    continue

                for day in days:
                    d = current_day - day

                    if d >= 0:
                        decay = self.params.grudge_immediate_weight if d == 0 else 0.5 ** d
                        self.grudge[p.id][attacker_id] += p.paranoia * decay
                
                self.grudge[p.id][attacker_id] = min(1, self.grudge[p.id][attacker_id])

    def update_co_vote(self, votes):
        voter_ids = list(votes.keys())

        for first_id in voter_ids:
            for second_id in voter_ids:
                if first_id == second_id:
                    continue

                same_target = 1 if votes[first_id] == votes[second_id] else 0
                beta = self.params.co_vote_beta
                self.co_vote[first_id][second_id] = ((1 - beta) * self.co_vote[first_id][second_id]) + (beta * same_target)

    def apply_wolf_association(self, dead_wolf_id, alive_players):
        for associated_player in alive_players:
            link = self.co_vote[dead_wolf_id][associated_player.id]

            if link <= self.params.co_vote_association_threshold:
                continue

            influence = (link - self.params.co_vote_association_threshold) * self.params.co_vote_association_weight

            for observer in alive_players:
                if observer.id != associated_player.id:
                    self.apply_influence(observer.id, associated_player.id, influence)
