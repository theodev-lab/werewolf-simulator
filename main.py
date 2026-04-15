import config
import argparse
from simulation.simulator import Simulator
from utils.stats import print_results

def get_args():
	parser = argparse.ArgumentParser(description="Simulate a game of Werewolf")
	parser.add_argument("--n_players", type=int, default=config.N_PLAYERS)
	parser.add_argument("--n_wolves", type=int, default=config.N_WOLVES)
	parser.add_argument("--n_games", type=int, default=config.N_GAMES)
	
	return parser.parse_args()

def main():
	args = get_args()
	simulator = Simulator(args.n_players, args.n_wolves, args.n_games)
	results = simulator.run()
	print_results(results, args.n_games)
 
if __name__ == "__main__":
    main()