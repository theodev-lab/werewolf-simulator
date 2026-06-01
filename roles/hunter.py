from roles.base import Role

class Hunter(Role):
    camp = "villageois"

    def on_death(self, game, player):
        candidates = [p for p in game.players if p.alive and p.id != player.id]
        
        if candidates:
            suspicion_row = game.suspicion.get_accusation_scores(player.id)
            target = max(candidates, key=lambda p: suspicion_row[p.id])
            game.log(f"🎯 PAN ! Le chasseur tire une dernière balle sur le joueur {target.id} ({target.role.__class__.__name__})")
            game.kill_player(target)