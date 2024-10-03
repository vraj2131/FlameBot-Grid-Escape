import time
import tkinter as tk
from environment import ShipEnvironment
from bots import Bot1, Bot2, Bot3, Bot4
from utils.grid_visualizer import GridVisualizer

def main():
    # Create the environment 
    env = ShipEnvironment()
    env.create_environment()

    # Initialize Bot1 with flammability parameter q
    # bot = Bot1(env, q=0.5)
    bot = Bot4(env, q=0.5)
    bot.initialize()  # Initialize fire, bot, and button

    # Create the Tkinter window and visualizer
    root = tk.Tk()
    root.title("Live Grid Simulation")
    visualizer = GridVisualizer(root, env, bot.fire_spread, bot)

    # Plan the bot's initial path to the button
    bot.plan_path()

    # Simulate time steps
    for t in range(1, 200):  # Simulate 20 time steps (can be adjusted)
        print(f"Time step {t}:")
        
        # Update visualization
        visualizer.simulate_step()

        # Check if bot has reached the button
        if bot.bot_position == bot.button_position:
            print("Bot reached the button! Success!")
            break
        
        # Check for failure (bot steps into fire)
        if bot.check_failure():
            print("Bot caught on fire! Failure!")
            break
        
        button_x, button_y = bot.button_position
        if bot.fire_spread.fire_grid[button_x, button_y] == 1:
            print("Fire reached the button! Failure!")
            break
        # Move the bot along its path
        bot.move_bot()
        # bot.move_towards_button()

        # Spread the fire
        bot.fire_spread.spread_fire()

        # Update visualization again after moving and fire spreading
        visualizer.simulate_step()

        # Wait for a moment to better visualize the time steps
        time.sleep(0.5)

    root.mainloop()


if __name__ == "__main__":
    main()
