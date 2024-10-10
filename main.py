# import time
# import tkinter as tk
# from environment import ShipEnvironment
# from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6
# from utils.grid_visualizer import GridVisualizer

# def main():
#     # Create the environment 
#     env = ShipEnvironment()
#     env.create_environment()

#     # Initialize Bot1 with flammability parameter q
#     # bot = Bot1(env, q=0.5)
#     bot = Bot4(env, q=0.5)
#     bot.initialize()  # Initialize fire, bot, and button

#     # Create the Tkinter window and visualizer
#     root = tk.Tk()
#     root.title("Live Grid Simulation")
#     visualizer = GridVisualizer(root, env, bot.fire_spread, bot)

#     # Plan the bot's initial path to the button
#     bot.plan_path()

#     # Simulate time steps
#     for t in range(1, 200):  # Simulate 20 time steps (can be adjusted)
#         print(f"Time step {t}:")
        
#         # Update visualization
#         visualizer.simulate_step()

#         # Check if bot has reached the button
#         if bot.bot_position == bot.button_position:
#             print("Bot reached the button! Success!")
#             break
        
#         # Check for failure (bot steps into fire)
#         if bot.check_failure():
#             print("Bot caught on fire! Failure!")
#             break
        
#         button_x, button_y = bot.button_position
#         if bot.fire_spread.fire_grid[button_x, button_y] == 1:
#             print("Fire reached the button! Failure!")
#             break
#         # Move the bot along its path
#         bot.move_bot()
#         # bot.move_towards_button()

#         # Spread the fire
#         bot.fire_spread.spread_fire()

#         # Update visualization again after moving and fire spreading
#         visualizer.simulate_step()

#         # Wait for a moment to better visualize the time steps
#         time.sleep(0.01)
        

#     root.mainloop()


# if __name__ == "__main__":
#     main()

import tkinter as tk
import csv
from environment import ShipEnvironment
from bots import Bot1, Bot2, Bot4
from utils.grid_visualizer import GridVisualizer

def run_simulation(simulation_no, q=1):
    """Run a single simulation of the bot and return the outcome."""
    # Create the environment
    env = ShipEnvironment()
    env.create_environment()

    # Initialize Bot1 with flammability parameter q
    bot = Bot4(env, q)
    bot.initialize()  # Initialize fire, bot, and button

    # Plan the bot's initial path to the button
    bot.plan_path()

    # Simulate time steps
    for t in range(1, 200):  # Simulate 20 time steps (can be adjusted)
        # Check if bot has reached the button
        if bot.bot_position == bot.button_position:
            print(f"Simulation {simulation_no}: Success!")
            return "Success"

        # Check for failure (bot steps into fire)
        if bot.check_failure():
            print(f"Simulation {simulation_no}: Failure! Bot caught on fire!")
            return "Failure"

        # Check if fire reached the button
        button_x, button_y = bot.button_position
        if bot.fire_spread.fire_grid[button_x, button_y] == 1:
            print(f"Simulation {simulation_no}: Failure! Fire reached the button!")
            return "Failure"

        # Move the bot along its path
        bot.move_bot()

        # Spread the fire
        bot.fire_spread.spread_fire()

    # If the loop ends without reaching the button, it's a failure
    print(f"Simulation {simulation_no}: Failure! Timeout.")
    return "Failure"

def main():
    results = []

    # Run the simulation 100 times
    for sim_no in range(1, 101):
        outcome = run_simulation(sim_no, q=1)
        results.append([sim_no, 1, outcome])  # Append (sr no, q, outcome)

    # Write results to a CSV file
    with open('Bot4_q=1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sr No', 'q', 'Outcome'])  # Write the header
        writer.writerows(results)  # Write all results

    print("Simulation complete! Results saved to 'simulation_results.csv'.")

if __name__ == "__main__":
    main()

# import time
# import tkinter as tk
# import csv
# from environment import ShipEnvironment
# from bots import Bot1
# from utils.grid_visualizer import GridVisualizer

# def run_simulation(simulation_no, q=0.5):
#     """Run a single simulation of the bot and return the outcome."""
#     # Create the environment
#     env = ShipEnvironment()
#     env.create_environment()

#     # Initialize Bot1 with flammability parameter q
#     bot = Bot1(env, q)
#     bot.initialize()  # Initialize fire, bot, and button

#     # Create the Tkinter window and visualizer
#     root = tk.Tk()
#     root.title(f"Live Grid Simulation {simulation_no}")
#     visualizer = GridVisualizer(root, env, bot.fire_spread, bot)

#     # Plan the bot's initial path to the button
#     bot.plan_path()

#     # Simulate time steps
#     for t in range(1, 200):  # Simulate 20 time steps (can be adjusted)
#         # Update visualization
#         visualizer.simulate_step()

#         # Check if bot has reached the button
#         if bot.bot_position == bot.button_position:
#             print(f"Simulation {simulation_no}: Success!")
#             root.destroy()  # Close the Tkinter window after success
#             return "Success"

#         # Check for failure (bot steps into fire)
#         if bot.check_failure():
#             print(f"Simulation {simulation_no}: Failure! Bot caught on fire!")
#             root.destroy()  # Close the Tkinter window after failure
#             return "Failure"

#         # Check if fire reached the button
#         button_x, button_y = bot.button_position
#         if bot.fire_spread.fire_grid[button_x, button_y] == 1:
#             print(f"Simulation {simulation_no}: Failure! Fire reached the button!")
#             root.destroy()  # Close the Tkinter window after failure
#             return "Failure"

#         # Move the bot along its path
#         bot.move_bot()

#         # Spread the fire
#         bot.fire_spread.spread_fire()

#         # Update visualization again after moving and fire spreading
#         visualizer.simulate_step()

#         # Wait for a moment to better visualize the time steps
#         root.update()  # Update the Tkinter window
#         time.sleep(0.05)  # Adjust the speed as needed (0.05 = 50ms delay per step)

#     # If the loop ends without reaching the button, it's a failure
#     print(f"Simulation {simulation_no}: Failure! Timeout.")
#     root.destroy()  # Close the Tkinter window after timeout
#     return "Failure"

# def main():
#     results = []

#     # Run the simulation 100 times
#     for sim_no in range(1, 101):
#         outcome = run_simulation(sim_no, q=0.5)
#         results.append([sim_no, 0.5, outcome])  # Append (sr no, q, outcome)

#     # Write results to a CSV file
#     with open('simulation_results.csv', mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Sr No', 'q', 'Outcome'])  # Write the header
#         writer.writerows(results)  # Write all results

#     print("Simulation complete! Results saved to 'simulation_results.csv'.")

# if __name__ == "__main__":
#     main()
