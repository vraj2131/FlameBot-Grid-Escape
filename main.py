# from environment import ShipEnvironment

# def main():
#     env = ShipEnvironment(grid_size=40)
    
#     env.create_environment()

# if _name_ == "_main_":
#     main()
import time
from environment import ShipEnvironment
from bots import Bot1
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

def visualize(environment, fire_spread, bot, title):
    """Visualize the environment with the bot, fire, and button using specified colors."""
    grid = np.copy(environment.grid)
    fire = fire_spread.fire_grid
    bot_pos = bot.bot_position
    button_pos = bot.button_position

    # Update grid with fire, bot, and button positions
    for x in range(environment.grid_size):
        for y in range(environment.grid_size):
            if fire[x, y] == 1:
                grid[x, y] = 2  # Fire represented as 2 (Red)
            if (x, y) == bot_pos:
                grid[x, y] = 3  # Bot represented as 3 (Blue)
            if (x, y) == button_pos:
                grid[x, y] = 4  # Button represented as 4 (Green)

    # Custom colormap: 0 = blocked (black), 1 = open (white), 2 = fire (red), 3 = bot (blue), 4 = button (green)
    cmap = colors.ListedColormap(['black', 'white', 'red', 'blue', 'green'])
    bounds = [0, 1, 2, 3, 4, 5]  # Boundaries for the color values
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Plot the grid
    plt.imshow(grid, cmap=cmap, norm=norm)
    plt.title(title)
    plt.colorbar(ticks=[0, 1, 2, 3, 4], label='Cell State')
    plt.show()

def main():
    # Create the environment
    env = ShipEnvironment()
    env.create_environment()

    # Initialize Bot1 with flammability parameter q
    bot = Bot1(env, q=0.5)
    bot.initialize()  # Initialize fire, bot, and button

    # Start the visualization
    visualize(env, bot.fire_spread, bot, title="Initial State")

    # Plan the bot's initial path to the button
    bot.plan_path()

    # Simulate time steps
    for t in range(1, 21):  # Simulate 20 time steps (can be adjusted)
        print(f"Time step {t}:")
        
        # Check if bot has reached the button
        if bot.bot_position == bot.button_position:
            print("Bot reached the button! Success!")
            visualize(env, bot.fire_spread, bot, title=f"Success at Time Step {t}")
            break
        
        # Check for failure (bot steps into fire)
        if bot.check_failure():
            print("Bot caught on fire! Failure!")
            visualize(env, bot.fire_spread, bot, title=f"Failure at Time Step {t}")
            break

        # Move the bot along its path
        bot.move_bot()

        # Spread the fire
        bot.fire_spread.spread_fire()

        # Re-visualize the state
        visualize(env, bot.fire_spread, bot, title=f"Time Step {t}")

        # Wait for a moment to better visualize the time steps
        time.sleep(1)
    
    else:
        print("Bot did not reach the button within the time limit.")

if __name__ == "_main_":
    main()