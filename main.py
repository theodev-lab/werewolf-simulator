from config import ROLE_COUNTS, N_GAMES
from simulation.simulator import Simulator
from utils.stats import print_results

def main():
	simulator = Simulator(ROLE_COUNTS, N_GAMES)
	results = simulator.run()
    
	if N_GAMES > 1:
		print_results(results)
 
if __name__ == "__main__":
	main()