import numpy as np
import math
import random
import argparse
import optuna

from config import SimulationParameters
from game import texts
from roles import ROLE_MAP, Sheriff
from simulation.simulator import Simulator

PARAMETER_BOUNDS = {
    "alpha": (0.01, 0.5),
    "vote_noise": (0.0, 1.0),
    "grudge_immediate_weight": (0.0, 1.0),
    "co_vote_beta": (0.0, 1.0),
    "co_vote_association_threshold": (0.0, 1.0),
    "co_vote_association_weight": (0.0, 1.0),
    "convince_role_value_weight": (0.0, 0.5),
    "suspicion_role_value_weight": (0.0, 0.5),
    "wolf_to_wolf_suspicion_resistance": (0.0, 1.0),
    "hunter_shot_threshold": (0.0, 1.0),
    "witch_kill_threshold": (0.0, 1.0),
}

TRAINING_CONFIGS = [
    # Score = +7 | Advantage: Villagers
    {"wolf": 3, "villager": 7, "seer": 1, "witch": 1, "hunter": 1, "little_girl": 1, "cupid": 1, "thief": 0},

    # Score = +5 | Advantage: Villagers
    {"wolf": 2, "villager": 5, "seer": 1, "witch": 0, "hunter": 1, "little_girl": 0, "cupid": 0, "thief": 0},

    # Score = +4 | Advantage: Villagers
    {"wolf": 3, "villager": 5, "seer": 1, "witch": 1, "hunter": 1, "little_girl": 0, "cupid": 0, "thief": 0},

    # Score = +3 | Advantage: Villagers
    {"wolf": 3, "villager": 6, "seer": 1, "witch": 0, "hunter": 1, "little_girl": 1, "cupid": 0, "thief": 0},

    # Score = +2 | Advantage: Villagers
    {"wolf": 2, "villager": 4, "seer": 0, "witch": 1, "hunter": 0, "little_girl": 1, "cupid": 0, "thief": 0},

    # Score = +1 | Advantage: Villagers
    {"wolf": 2, "villager": 6, "seer": 0, "witch": 1, "hunter": 0, "little_girl": 0, "cupid": 0, "thief": 0},

    # Score = 0 | Advantage: Perfect Balance
    {"wolf": 2, "villager": 3, "seer": 1, "witch": 0, "hunter": 0, "little_girl": 0, "cupid": 0, "thief": 0},

    # Score = 0 | Advantage: Perfect Balance
    {"wolf": 2, "villager": 4, "seer": 0, "witch": 0, "hunter": 1, "little_girl": 1, "cupid": 0, "thief": 0},

    # Score = 0 | Perfect Balance
    {"wolf": 3, "villager": 6, "seer": 1, "witch": 0, "hunter": 0, "little_girl": 1, "cupid": 0, "thief": 0},

    # Score = 0 | Perfect Balance
    {"wolf": 2, "villager": 5, "seer": 0, "witch": 1, "hunter": 0, "little_girl": 0, "cupid": 0, "thief": 0},

    # Score = 0 | Advantage: Perfect Balance
    {"wolf": 3, "villager": 3, "seer": 1, "witch": 1, "hunter": 1, "little_girl": 0, "cupid": 1, "thief": 0},

    # Score = -2 | Advantage: Wolves
    {"wolf": 3, "villager": 6, "seer": 0, "witch": 1, "hunter": 1, "little_girl": 0, "cupid": 0, "thief": 0},

    # Score = -2 | Advantage: Wolves
    {"wolf": 5, "villager": 10, "seer": 1, "witch": 1, "hunter": 1, "little_girl": 1, "cupid": 1, "thief": 0},

    # Score = -4 | Advantage: Wolves
    {"wolf": 4, "villager": 7, "seer": 0, "witch": 1, "hunter": 1, "little_girl": 1, "cupid": 0, "thief": 0},

    # Score = -6 | Advantage: Wolves
    {"wolf": 4, "villager": 10, "seer": 0, "witch": 1, "hunter": 1, "little_girl": 0, "cupid": 1, "thief": 0},

    # Score = -7 | Advantage: Wolves
    {"wolf": 3, "villager": 4, "seer": 0, "witch": 1, "hunter": 0, "little_girl": 0, "cupid": 0, "thief": 0},

    # Score = -10 | Advantage: Wolves
    {"wolf": 3, "villager": 3, "seer": 0, "witch": 1, "hunter": 0, "little_girl": 0, "cupid": 1, "thief": 0},
]

def complete_role_counts(role_counts):
    return {role_name: role_counts.get(role_name, 0) for role_name in ROLE_MAP}

def theoretical_score(role_counts, use_sheriff=True):
    score = 0

    for role_name, count in complete_role_counts(role_counts).items():
        score += ROLE_MAP[role_name].character_value * count

    if use_sheriff:
        score += Sheriff.character_value

    return score

def target_advantage(role_counts, score_scale):
    return math.tanh(theoretical_score(role_counts) * score_scale)

def simulated_advantage(role_counts, params, n_games, seed):
    random.seed(seed)
    np.random.seed(seed)

    results = Simulator(complete_role_counts(role_counts), n_games, params).run()
    villagers = results.get(texts.VILLAGERS, 0)
    wolves = results.get(texts.WOLVES, 0)

    decisive_games = villagers + wolves

    if decisive_games == 0:
        return 0

    return (villagers - wolves) / decisive_games

def evaluate_params(params, configs, n_games, score_scale, seed):
    errors = []

    for index, role_counts in enumerate(configs):
        observed = simulated_advantage(role_counts, params, n_games, seed + index)
        target = target_advantage(role_counts, score_scale)
        errors.append((observed - target) ** 2)

    return sum(errors) / len(errors)

def params_from_trial(trial):
    values = {
        name: trial.suggest_float(name, lower, upper)
        for name, (lower, upper) in PARAMETER_BOUNDS.items()
    }

    return SimulationParameters(**values)

def format_params(params):
    lines = []

    for name in PARAMETER_BOUNDS:
        lines.append(f"{name}: {getattr(params, name):.4f}")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Tune werewolf simulator behavioral constants with Optuna.")
    parser.add_argument("--trials", type=int, default=50)
    parser.add_argument("--games-per-config", type=int, default=300)
    parser.add_argument("--score-scale", type=float, default=0.08)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    def objective(trial):
        params = params_from_trial(trial)
            
        return evaluate_params(
            params=params,
            configs=TRAINING_CONFIGS,
            n_games=args.games_per_config,
            score_scale=args.score_scale,
            seed=args.seed,
        )

    sampler = optuna.samplers.TPESampler(seed=args.seed)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=args.trials)

    best_params = SimulationParameters(**study.best_params)

    print("\nBest objective value:")
    print(f"{study.best_value:.6f}")

    print("\nBest parameters:")
    print(format_params(best_params))


if __name__ == "__main__":
    main()
