from roles.base import Role

class Hunter(Role):
    camp = "villagers"

    def on_death(self, game, player):
        candidates = [p for p in game.players if p.alive and p.id != player.id]
        
        if candidates:
            suspicion_row = game.suspicion[player.id]
            target = max(candidates, key=lambda p: suspicion_row[p.id])
            game.kill_player(target)