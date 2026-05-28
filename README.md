# werewolf-simulator

A Monte Carlo simulation framework for the game Les Loups-garous de Thiercelieux (Werewolf), designed to model player behavior, voting dynamics, and role strategies.

## Idées

- Pour modéliser le système de vote, on fera plusieurs tours de vote, et à chaque tour ça va faire bouger la matrice de suspicion entre les joueurs. Si le joueur n'est pas sûr de sa décision, alors il s'abstiendra de voter, ou alors suivra la majorité. Si le joueur est sûr de sa décision, alors il votera pour le joueur qu'il pense être un loup-garou. On peut aussi modéliser les joueurs qui votent pour des raisons stratégiques, par exemple pour protéger un allié ou pour éliminer un rival.

* https://github.com/This-Game/monte-carlo-werewolf-simulation
* https://ejwagenmakers.com/2006/werewolves.pdf
* https://joeystanley.com/blog/simulating_werewolf/
* https://fomo.ai/ai-resources/werewolves-and-villagers-social-psychology-thought-experiment-ai-simulation-with-chatgpt/
