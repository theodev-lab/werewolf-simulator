import config
from simulation.simulator import Simulator
from utils.stats import print_results

def main():
	simulator = Simulator(config.ROLE_COUNTS, config.N_GAMES)
	results = simulator.run()
    
	if config.N_GAMES > 1:
		print_results(results)
 
if __name__ == "__main__":
	main()