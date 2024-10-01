import time
import tkinter as tk
from environment import ShipEnvironment
from bots import Bot1


class GridVisualizer:
    def __init__(self, master, environment, fire_spread, bot, cell_size=15):
        self.master = master
        self.environment = environment
        self.fire_spread = fire_spread
        self.bot = bot
        self.cell_size = cell_size
        self.canvas_size = environment.grid_size * cell_size
        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

    def draw_grid(self):
        """Draw the entire grid based on the environment, fire, bot, and button."""
        self.canvas.delete("all")  # Clear the canvas for redrawing

        for x in range(self.environment.grid_size):
            for y in range(self.environment.grid_size):
                # Determine the color of the cell based on its state
                if self.fire_spread.fire_grid[x, y] == 1:
                    color = "red"  # Fire
                elif (x, y) == self.bot.bot_position:
                    color = "blue"  # Bot
                elif (x, y) == self.bot.button_position:
                    color = "green"  # Button
                elif self.environment.grid[x, y] == 1:
                    color = "white"  # Open space
                else:
                    color = "black"  # Blocked

                # Draw the rectangle on the canvas
                self.canvas.create_rectangle(
                    y * self.cell_size, x * self.cell_size,
                    (y + 1) * self.cell_size, (x + 1) * self.cell_size,
                    fill=color, outline="gray"
                )

    def update(self):
        """Update the visualization of the grid."""
        self.draw_grid()
        self.master.update_idletasks()


def main():
    # Create the environment
    env = ShipEnvironment()
    env.create_environment()

    # Initialize Bot1 with flammability parameter q
    bot = Bot1(env, q=0.5)
    bot.initialize()  # Initialize fire, bot, and button

    # Create the Tkinter window and visualizer
    root = tk.Tk()
    root.title("Live Grid Simulation")
    visualizer = GridVisualizer(root, env, bot.fire_spread, bot)

    # Plan the bot's initial path to the button
    bot.plan_path()

    # Simulate time steps
    for t in range(1, 21):  # Simulate 20 time steps (can be adjusted)
        print(f"Time step {t}:")
        
        # Update visualization
        visualizer.update()

        # Check if bot has reached the button
        if bot.bot_position == bot.button_position:
            print("Bot reached the button! Success!")
            break
        
        # Check for failure (bot steps into fire)
        if bot.check_failure():
            print("Bot caught on fire! Failure!")
            break

        # Move the bot along its path
        bot.move_bot()

        # Spread the fire
        bot.fire_spread.spread_fire()

        # Update visualization again after moving and fire spreading
        visualizer.update()

        # Wait for a moment to better visualize the time steps
        time.sleep(0.5)

    root.mainloop()


if __name__ == "__main__":
    main()
