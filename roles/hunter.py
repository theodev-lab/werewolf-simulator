from roles.base import Role
from game import texts

class Hunter(Role):
    camp = "villageois"

    def on_death(self, game, player):
        candidates = [p for p in game.players if p.alive and p.id != player.id]
        
        if candidates:
            suspicion_row = game.suspicion.get_accusation_scores(player.id)
            target = max(candidates, key=lambda p: suspicion_row[p.id])
            game.log(texts.get("hunter_shot", target_id=target.id, role_name=target.role.__class__.__name__))
            game.kill_player(target)
