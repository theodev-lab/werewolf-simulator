from game import texts
from roles.base import Role

class Thief(Role):
    camp = texts.VILLAGERS

    def on_night(self, game, player):
        if game.current_day != 1:
            return

        pass
