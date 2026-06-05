from game import texts
from roles.base import Role
from config import WITCH_KILL_THRESHOLD

class Witch(Role):
    camp = texts.VILLAGERS
    character_value = 5

    def __init__(self):
        self.life_potion_available = True
        self.death_potion_available = True

    def on_night(self, game, player):
        game.log(texts.WITCH_TURN)

        wolf_target = game.dead_this_night[0] if game.dead_this_night else None

        if self.life_potion_available and wolf_target is not None and (wolf_target is player or wolf_target is game.get_lover(player)):
            self.life_potion_available = False
            game.resurrect_player(wolf_target)

        if self.death_potion_available:
            candidates = [p for p in game.players if p.alive and p.id != player.id]

            if candidates:
                suspicion_row = game.suspicion.get_accusation_scores(player.id)
                target = max(candidates, key=lambda p: suspicion_row[p.id])

                if suspicion_row[target.id] >= WITCH_KILL_THRESHOLD:
                    self.death_potion_available = False
                    game.kill_player(target)
