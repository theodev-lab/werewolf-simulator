from tabulate import tabulate

def print_results(results, n_games):
    total = sum(results.values())

    table = []

    for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True):
        pct = (v / total) * 100
        table.append([k, v, f"{pct:.2f}%"])

    print("📊 WERWOLF SIMULATION RESULTS\n")

    print(tabulate(
        table,
        headers=["Faction", "Wins", "Win rate"],
        tablefmt="fancy_grid"
    ))

    print(f"\nGames run: {n_games}")