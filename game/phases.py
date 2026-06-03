import random
from config import ALPHA, USE_SHERIFF
from game import texts
from roles import Cupid, LittleGirl, Seer, Thief, Witch

def choose_most_convincing_candidate(candidates, top_n=3):
    preferred_candidates = sorted(candidates, key=lambda p: p.convince, reverse=True)[:top_n]
    return random.choice(preferred_candidates)

def role_turn(game, RoleClass):
    players = game.alive_players() + game.dead_this_night

    for player in players:
        if isinstance(player.role, RoleClass):
            player.role.on_night(game, player)

def wolves_turn(game):
    game.log(texts.WOLVES_TURN)
  
    villagers = [p for p in game.players if p.role.camp == texts.VILLAGERS and p.alive]
  
    if villagers:
        target = choose_most_convincing_candidate(villagers)
        game.kill_player(target)
                
def update_memory(game, votes):
    for voter_id, target_id in votes.items():
        if voter_id != target_id:
            target = game.players[target_id]
            
            if voter_id not in target.memory:
                target.memory[voter_id] = []
                
            target.memory[voter_id].append(game.current_day)

def resolve_death_effects(game):
    death_index = 0

    while death_index < len(game.dead_this_night):
        player = game.dead_this_night[death_index]
        death_index += 1
        player.role.on_death(game, player)

    game.dead_this_night = []

def elect_sheriff(game, candidates=None):
    candidates = candidates or game.alive_players()
    voters = game.alive_players()

    vote_counts = {}

    for _ in voters:
        vote = choose_most_convincing_candidate(candidates)
        vote_counts[vote.id] = vote_counts.get(vote.id, 0) + 1

    max_votes = max(vote_counts.values())
    tied_candidate_ids = [candidate_id for candidate_id, votes in vote_counts.items() if votes == max_votes]

    if len(tied_candidate_ids) > 1:
        tied_candidates = [game.players[candidate_id] for candidate_id in tied_candidate_ids]
        elect_sheriff(game, tied_candidates)
        return

    sheriff_id = tied_candidate_ids[0]
    game.sheriff = game.players[sheriff_id]
    game.log(texts.SHERIFF_ELECTED.format(sheriff_id=sheriff_id))
            
def voting_process(game):
    # 1) Intention phase: players share their suspicions
    intentions = {p.id: p.vote(game, game.suspicion.get_accusation_scores(p.id)) for p in game.alive_players()}
    
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
        vote = p.vote(game, game.suspicion.get_accusation_scores(p.id))
        vote_weight = 2 if game.sheriff is p else 1
        vote_counts[vote] = vote_counts.get(vote, 0) + vote_weight
        votes[p.id] = vote 
    
    # 4) Update memory of players based on votes (who voted for whom) - this will influence future suspicion and voting behavior
    update_memory(game, votes)
    
    if vote_counts:
        target_id = max(vote_counts, key=vote_counts.get)
        game.log(texts.VOTE_ELIMINATION.format(target_id=target_id, role_name=game.players[target_id].role.__class__.__name__))
        game.kill_player(game.players[target_id])
        resolve_death_effects(game)
             
def night_phase(game):
    game.log(f"\n{texts.NIGHT_START}")
    game.suspicion.apply_grudge(game.alive_players(), game.current_day)

    role_turn(game, Thief)
    role_turn(game, Cupid)
    role_turn(game, LittleGirl)
    role_turn(game, Seer)
    wolves_turn(game)
    role_turn(game, Witch)

def day_phase(game):
    if not game.dead_this_night:
        game.log(texts.DAY_NO_DEATH)
    else:
        dead_infos = [texts.DEAD_PLAYER.format(player_id=p.id, role_name=p.role.__class__.__name__) for p in game.dead_this_night]
        dead_str = dead_infos[0] if len(dead_infos) == 1 else texts.DEAD_PLAYERS_JOIN.format(players=", ".join(dead_infos[:-1]), last_player=dead_infos[-1])
        game.log(texts.DAY_DEATHS.format(dead_players=dead_str))
        
    resolve_death_effects(game)
    
    over, _ = game.is_over()
    
    if not over:
        if USE_SHERIFF == 1 and game.current_day == 1 and game.sheriff is None:
            game.log(texts.SHERIFF_TURN)
            elect_sheriff(game)

        voting_process(game)
