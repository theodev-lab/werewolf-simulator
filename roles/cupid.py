import random

from game import texts
from roles.base import Role

class Cupid(Role):
    camp = texts.VILLAGERS

    def on_night(self, game, player):
        if game.current_day != 1:
            return

        game.log(texts.CUPID_TURN)

        lovers = random.sample(game.alive_players(), 2)
        lovers[0].lover = lovers[1]
        lovers[1].lover = lovers[0]

        game.suspicion.lock_cell(lovers[0].id, lovers[1].id, 0)
        game.suspicion.lock_cell(lovers[1].id, lovers[0].id, 0)
