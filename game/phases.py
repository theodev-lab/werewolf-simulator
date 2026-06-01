import random
from config import ALPHA
from game import texts

def wolves_turn(game):
    game.log(texts.get("wolves_turn"))
  
    villagers = [p for p in game.players if p.role.camp == "villageois" and p.alive]
  
    if villagers:
        sorted_villagers = sorted(villagers, key=lambda p: p.convince, reverse=True)
        target = random.choice(sorted_villagers[:3])
        game.kill_player(target)
                
def update_memory(game, votes):
    for voter_id, target_id in votes.items():
        if voter_id != target_id:
            target = game.players[target_id]
            
            if voter_id not in target.memory:
                target.memory[voter_id] = []
                
            target.memory[voter_id].append(game.current_day)
            
def voting_process(game):
    # 1) Intention phase: players share their suspicions
    intentions = {p.id: p.vote(game.players, game.suspicion.get_accusation_scores(p.id)) for p in game.alive_players()}
    
    # 2) Debate phase: players try to convince each other (this will influence their votes)
    for speaker in game.alive_players():
        target_id = intentions[speaker.id]
        target = game.players[target_id]
        
        influence = (speaker.convince - target.convince) * ALPHA
        
        for listener in game.alive_players():
            if listener.id != speaker.id and listener.id != target_id:
                game.suspicion.apply_influence(listener.id, target_id, influence)

    # 3) Voting phase: players vote to eliminate someone
    vote_counts = {}
    votes = {}
    
    for p in game.alive_players():
        vote = p.vote(game.players, game.suspicion.get_accusation_scores(p.id))
        vote_counts[vote] = vote_counts.get(vote, 0) + 1
        votes[p.id] = vote 
    
    # 4) Update memory of players based on votes (who voted for whom) - this will influence future suspicion and voting behavior
    update_memory(game, votes)
    
    if vote_counts:
        target_id = max(vote_counts, key=vote_counts.get)
        game.log(texts.get("vote_elimination", target_id=target_id, role_name=game.players[target_id].role.__class__.__name__))
        game.kill_player(game.players[target_id])       
             
def night_phase(game):
    game.dead_this_night = []
    game.log(texts.get("night_start"))
    game.suspicion.apply_grudge(game.alive_players(), game.current_day)
    wolves_turn(game)

def day_phase(game):
    if not game.dead_this_night:
        game.log(texts.get("day_no_death"))
    else:
        dead_infos = [texts.get("dead_player", player_id=p.id, role_name=p.role.__class__.__name__) for p in game.dead_this_night]
        dead_str = dead_infos[0] if len(dead_infos) == 1 else texts.get("dead_players_join", players=", ".join(dead_infos[:-1]), last_player=dead_infos[-1])
        game.log(texts.get("day_deaths", dead_players=dead_str))
        
        for p in game.dead_this_night:      
            p.role.on_death(game, p)
    
    voting_process(game)
