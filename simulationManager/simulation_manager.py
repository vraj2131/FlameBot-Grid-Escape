import time
import tkinter as tk
import csv
from environment import ShipEnvironment
from bots import Bot1, Bot2, Bot3, Bot4
from utils.grid_visualizer import GridVisualizer

def run_single_simulation(bot_class, q=0.5):
    """Run single simulation with specific q and specific bot."""
    
    # initialize the environment and bot
    env = ShipEnvironment()
    env.create_environment()

    bot = bot_class(env, q)
    bot.initialize()  
    
    # initialize the tkinter window for visualization 
    root = tk.Tk()
    root.title("Live Grid Simulation")
    visualizer = GridVisualizer(root, env, bot.fire_spread, bot)

    # Plan path wont be called for Bot 4
    if hasattr(bot, 'plan_path'):
        bot.plan_path()  

    # Simulate time steps
    for t in range(1, 500):  
        visualizer.simulate_step()
        
        # if bot reached button
        if bot.bot_position == bot.button_position:
            print("Bot reached the button! Success!")
            return "Success"

        # if bot on fire
        if bot.check_failure():
            print("Bot caught on fire! Failure!")
            return "Failure"

        # fire reached button
        button_x, button_y = bot.button_position
        if bot.fire_spread.fire_grid[button_x, button_y] == 1:
            print("Fire reached the button! Failure!")
            return "Failure"

        # Move the bot to next cell
        bot.move_bot()

        # Spread the fire
        bot.fire_spread.spread_fire()
        
        visualizer.simulate_step()
        
        time.sleep(0.01)
        
    root.mainloop()


    print("Timeout. Failure!")
    return "Failure"


def single_simulate(bot_class, q=0.5):
    """Single simulation without visualization"""

    env = ShipEnvironment()
    env.create_environment()

    bot = bot_class(env, q)
    bot.initialize()  


    if hasattr(bot, 'plan_path'):
        bot.plan_path()  

    for t in range(1, 200):  
        if bot.bot_position == bot.button_position:
            print("Bot reached the button! Success!")
            return "Success"

        if bot.check_failure():
            print("Bot caught on fire! Failure!")
            return "Failure"

        button_x, button_y = bot.button_position
        if bot.fire_spread.fire_grid[button_x, button_y] == 1:
            print("Fire reached the button! Failure!")
            return "Failure"

        bot.move_bot()

        bot.fire_spread.spread_fire()

    print("Simulation Timeout. Failure!")
    return "Failure"

def run_multiple_simulations(bot_class, num_simulations = 100, q=0.5):
    """Run multiple simulations for the specified bot."""
    results = []
    for res in range(1, num_simulations + 1):
        outcome = single_simulate(bot_class, q)
        results.append([res, q, outcome])  
    
    # Write results to a CSV file
    filename = f'simulation_results_{bot_class.__name__}_q={q}.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Simulation No', 'q', 'Outcome'])  
        writer.writerows(results)  
    
    print(f"Simulations complete! Results saved to '{filename}'.")


# functions to call in main.py
def bot1_multiple(num_simulations = 100, q = 0.5):
    run_multiple_simulations(Bot1, num_simulations, q)

def bot2_multiple(num_simulations = 100, q = 0.5):
    run_multiple_simulations(Bot2, num_simulations, q)

def bot3_multiple(num_simulations = 100, q = 0.5):
    run_multiple_simulations(Bot3, num_simulations, q)

def bot4_multiple(num_simulations = 100, q=0.5):
    run_multiple_simulations(Bot4, num_simulations, q)
    
def bot1_single(q = 0.5):
    run_single_simulation(Bot1, q)

def bot2_single(q = 0.5):
    run_single_simulation(Bot2, q)

def bot3_single(q = 0.5):
    run_single_simulation(Bot3, q)

def bot4_single(q = 0.5):
    run_single_simulation(Bot4, q)
