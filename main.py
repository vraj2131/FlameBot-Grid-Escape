from simulationManager.simulation_manager import *

def main():
    """Run simulation for different bots
    uncomment the bot you want to run, if want to run multiple simulations, enter the number,
    Specify the q value and execute it"""
    bot1_single(q = 0.1)
    # bot1_multiple(num_simulations = 100, q = 0.5)
    # bot2_single(q = 0.2)
    # bot2_multiple(num_simulations = 5, q = 0.6)
    # bot3_single(q = 0.3)
    # bot3_multiple(num_simulations = 3, q = 0.7)
    # bot4_single(q = 1.0)
    # bot4_multiple(num_simulations = 5, q = 0.4)
    
if __name__ == "__main__":
    main()
