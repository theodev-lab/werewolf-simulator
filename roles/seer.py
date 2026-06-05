from game import texts
from roles.base import Role

class Seer(Role):
    camp = texts.VILLAGERS
    character_value = 7

    def on_night(self, game, player):
        game.log(texts.SEER_TURN)

        candidates = [target for target in game.alive_players() if target.id != player.id and not game.suspicion.locked[player.id][target.id]]

        if candidates:
            accusation_scores = game.suspicion.get_accusation_scores(player.id)
            target = max(candidates, key=lambda candidate: accusation_scores[candidate.id])
            suspicion = 1 if target.role.camp == texts.WOLVES else 0
            game.suspicion.lock_cell(player.id, target.id, suspicion)
