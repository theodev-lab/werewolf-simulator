# 🐺 werewolf-simulator

This project simulates Werewolf games without requiring human input. Each player receives a role and a randomly generated personality. During the game, players build suspicions, influence one another, vote during the day, and use their role-specific abilities at night.

The simulator can run either a single detailed game or many games in order to estimate each faction's win rate.

## 🧰 Requirements

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Run the simulator

Start the simulation from the repository root:

```bash
python3 main.py
```

The output depends on `N_GAMES` in `config.py`:

- With `N_GAMES = 1`, the simulator prints the history of a single game.
- With `N_GAMES > 1`, it prints a table containing the number of victories and win rate for each faction.

## ⚙️ Configuration

Simulation settings are defined in [`config.py`](config.py).

### 🃏 Role distribution

`ROLE_COUNTS` controls how many cards of each role are included in a game:

```python
ROLE_COUNTS = {
    "thief": 1,
    "cupid": 1,
    "seer": 1,
    "wolf": 3,
    "little_girl": 1,
    "witch": 1,
    "villager": 4,
    "hunter": 1
}
```

Set a role count to `0` to disable that role. When the Thief is enabled, two extra Villager cards are automatically added to the deck as the two undealt cards from which the Thief may choose.

### 🎛️ Simulation parameters

| Parameter | Description |
| --- | --- |
| `N_GAMES` | Number of games to simulate. Use `1` for a detailed game log and a larger value for aggregate statistics. |
| `ALPHA` | Strength of the influence exerted by players during the debate phase. |
| `VOTE_NOISE` | Random variation added to accusation scores when players vote. |
| `HUNTER_SHOT_THRESHOLD` | Minimum suspicion score required for the Hunter to shoot another player when dying. |
| `WITCH_KILL_THRESHOLD` | Minimum suspicion score required for the Witch to use her death potion. |
| `SEED` | Reserved random seed setting. It is currently declared but not applied by the simulator. |

## 🎭 Roles

| Player card | Faction | Role |
| --- | --- | --- |
| <img src="assets/cards/villager.png" alt="Villager card" width="100"> | Villagers | **Villager**: Their objective is to eliminate every Werewolf. They have no special power and must rely solely on their insight and powers of persuasion. |
| <img src="assets/cards/wolf.png" alt="Werewolf card" width="100"> | Werewolves | **Werewolf**: Their objective is to eliminate every innocent player, meaning anyone who is not a Werewolf. Each night, the Werewolves choose a victim to eliminate. |
| <img src="assets/cards/seer.png" alt="Seer card" width="100"> | Villagers | **Seer**: Her objective is to eliminate every Werewolf. Each night, she may inspect a player and discover their true identity. |
| <img src="assets/cards/little_girl.png" alt="Little Girl card" width="100"> | Villagers | **Little Girl**: Her objective is to eliminate every Werewolf. Each night, she may spy on the Werewolves. |
| <img src="assets/cards/witch.png" alt="Witch card" width="100"> | Villagers | **Witch**: Her objective is to eliminate every Werewolf. She has two potions: a life potion that can save the Werewolves' victim and a death potion that can eliminate another player. |
| <img src="assets/cards/hunter.png" alt="Hunter card" width="100"> | Villagers | **Hunter**: Their objective is to eliminate every Werewolf. When they die, they may eliminate another player with their final bullet. |
| <img src="assets/cards/cupid.png" alt="Cupid card" width="100"> | Villagers | **Cupid**: Their objective is to eliminate every Werewolf. At the beginning of the game, they create a couple. The two lovers must survive together: if one dies, the other dies of grief. |
| <img src="assets/cards/thief.png" alt="Thief card" width="100"> | Variable | **Thief**: Their objective is not fixed. At the beginning of the game, they may choose their role from the two cards that were not dealt. |

## 🗳️ Voting and behavior model

The simulator focuses mainly on voting dynamics. Each player has two psychological traits generated at the beginning of the game:

$$C \sim \mathcal{N}(0, 1)$$

$$P \sim \mathrm{Beta}(2, 3)$$

`C` is the player's persuasion score (`convince`). `P` is their paranoia score (`paranoia`), used to model how strongly they remember previous votes against them.

During the day, players first announce an intended target. Each speaker then influences the other players' suspicion toward that target:

$$I = (C_{speaker} - C_{target}) \times \alpha$$

The resulting influence is added to the listener's suspicion matrix and clamped between `0` and `1`:

$$S_{new} = \max(0, \min(1, S_{old} + I))$$

Players also remember who voted against them. This creates a grudge score that decays over time, so recent attacks matter more than old ones:

$$G_{new} = \min\left(1, \sum_{t_{attack} \in T} P \times 0.5^{(t_{current} - t_{attack})} \right)$$

The final accusation score combines rational suspicion and emotional grudge:

$$A = \max(0, \min(1, S + G))$$

When voting, the simulator adds a small amount of randomness to avoid fully deterministic decisions:

$$V = A + \epsilon \times N$$

`N` is `VOTE_NOISE`, and `epsilon` is a random value between `0` and `1`. Each player votes for the alive candidate with the highest accusation score. The player with the most votes is eliminated.

Special roles can also influence this model by introducing a notion of certainty. Unlike regular players, they can obtain reliable information that directly affects their voting behavior. For example, the Seer can lock a suspicion value after discovering a player's role.

## 📄 License

This project is licensed under the terms of the [`LICENSE`](LICENSE) file.
