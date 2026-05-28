import random
import numpy as np
from game.player import Player
from roles import ROLE_MAP

class Game:
    def __init__(self, role_counts):
        self.role_counts = role_counts
        self.n_players = sum(role_counts.values())
        self.players = self._init_players()
        self.suspicion = np.zeros((self.n_players, self.n_players)) # Suspicion matrix: level of suspicion each player has towards every other player (used for voting behavior)
        
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
            player.role.on_death(self, player)

    def night_phase(self):
        villagers = [p for p in self.players if p.role.camp == "villagers" and p.alive]
        
        if villagers:
            target = random.choice(villagers)
            self.kill_player(target)

    def day_phase(self):
        votes = {}
        
        for p in self.alive_players():
            vote = p.vote(self.players, self.suspicion[p.id])
            votes[vote] = votes.get(vote, 0) + 1
        
        if votes:
            target_id = max(votes, key=votes.get)
            self.kill_player(self.players[target_id])
    
    def is_over(self):
        wolves = [p for p in self.players if p.role.camp == "wolves" and p.alive]
        villagers = [p for p in self.players if p.role.camp == "villagers" and p.alive]
        
        if not wolves:
            return True, "villagers"
        elif len(wolves) >= len(villagers): # we assume that there are only 2 camps : villagers and wolves
            return True, "wolves"
        else:
            return False, None

    def play(self):
        while True:
            self.night_phase()
            over, winner = self.is_over()
            if over:
                return winner
                
            self.day_phase()
            over, winner = self.is_over()
            if over:
                return winner