from tabulate import tabulate
from game import texts

def print_results(results):
    n_games = sum(results.values())

    table = []

    for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True):
        pct = (v / n_games) * 100
        table.append([k, v, f"{pct:.2f}%"])

    print(texts.STATS_TITLE, end="\n\n")

    print(tabulate(table, headers=[texts.STATS_FACTION, texts.STATS_WINS, texts.STATS_WIN_RATE], tablefmt="fancy_grid"), end="\n\n")

    print(texts.STATS_GAMES_RUN.format(n_games=n_games))
