TEXTS = {
    "game_start": "🎮 La partie vient de commencer !",
    "game_over": "\n🏆 La partie est terminée ! Les {winner} ont gagné !",
    "wolves_turn": "🐺 Les loups-garous vont décider d'une victime à dévorer.",
    "vote_elimination": "🗳️  Le village a décidé d'éliminer le joueur {target_id} ({role_name}).",
    "night_start": "\n🌙 La nuit tombe sur le village de Thiercelieux...",
    "day_no_death": "☀️  Le village se réveille et personne n'est mort pendant la nuit !",
    "dead_player": "le joueur {player_id} ({role_name})",
    "dead_players_join": "{players} et {last_player}",
    "day_deaths": "☀️  Le village se réveille sans... {dead_players}.",
    "hunter_shot": "🎯 PAN ! Le chasseur tire une dernière balle sur le joueur {target_id} ({role_name})",
}

def get(key, **kwargs):
    return TEXTS[key].format(**kwargs)
