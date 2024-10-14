import tkinter as tk
import time

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
        """Visualize the entire grid with the environment, fire, bot, and button."""
        self.canvas.delete("all") 

        for x in range(self.environment.grid_size):
            for y in range(self.environment.grid_size):
                if self.fire_spread.fire_grid[x, y] == 1:
                    color = "red"  # Fire
                elif self.bot.bot_position == (x, y):
                    color = "blue"  # Bot
                elif self.bot.button_position == (x, y):
                    color = "green"  # Button
                elif self.environment.grid[x, y] == 1:
                    color = "white"  # Open cell
                else:
                    color = "black"  # Blocked cell

                self.canvas.create_rectangle(
                    y * self.cell_size, x * self.cell_size, 
                    (y + 1) * self.cell_size, (x + 1) * self.cell_size, 
                    fill=color, outline="gray"
                )
        self.master.update()

    def simulate_step(self):
        time.sleep(0.1)  
        self.draw_grid()
