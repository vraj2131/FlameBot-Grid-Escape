import random
import numpy as np
import tkinter as tk
import time

class ShipEnvironment:
    def __init__(self, grid_size=40):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))  # Start with all cells blocked (0 represents blocked)
        self.open_cells = []
        self.cell_size = 15  # Size of each cell for Tkinter visualization
        self.window = tk.Tk()
        self.window.title("Ship Environment")
        self.canvas = tk.Canvas(self.window, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size)
        self.canvas.pack()

    def initialize_grid(self):
        """Randomly choose an interior cell to open."""
        start_x = random.randint(1, self.grid_size - 2)
        start_y = random.randint(1, self.grid_size - 2)
        self.grid[start_x, start_y] = 1  # Open the cell (1 represents open)
        self.open_cells.append((start_x, start_y))
        self.visualize_grid()  # Update visualization after opening the first cell
        self.window.update()
        # time.sleep(0.1)  # Add delay to visualize the first step

    def open_cells_with_neighbors(self):
        """Gradually open cells with visible steps."""
        while True:
            # Identify blocked cells with exactly one open neighbor
            candidates = []
            for x in range(1, self.grid_size - 1):
                for y in range(1, self.grid_size - 1):
                    if self.grid[x, y] == 0 and self.count_open_neighbors(x, y) == 1:
                        candidates.append((x, y))
            
            if not candidates:
                break  # Stop if no candidates are found
            
            # Randomly select one of the candidates and open it
            cell_to_open = random.choice(candidates)
            self.grid[cell_to_open[0], cell_to_open[1]] = 1
            self.open_cells.append(cell_to_open)

            # Visualize and update window step by step
            self.visualize_grid()
            self.window.update()
            # time.sleep(0.05)  # Short delay to see the progress gradually

    def count_open_neighbors(self, x, y):
        """Count how many open neighbors the cell (x, y) has."""
        open_neighbors = 0
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # Only up/down/left/right neighbors
        for nx, ny in neighbors:
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                if self.grid[nx, ny] == 1:
                    open_neighbors += 1
        return open_neighbors

    def identify_and_open_dead_ends(self):
        """Identify dead ends and open neighbors for approximately half of them."""
        dead_ends = []
        # Identify dead ends: open cells with exactly one open neighbor
        for (x, y) in self.open_cells:
            if self.count_open_neighbors(x, y) == 1:
                dead_ends.append((x, y))

        # Randomly open neighbors of approximately half of the dead ends
        num_to_open = len(dead_ends) // 2
        for (x, y) in random.sample(dead_ends, num_to_open):
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            closed_neighbors = [(nx, ny) for (nx, ny) in neighbors if self.grid[nx, ny] == 0]
            if closed_neighbors:
                cell_to_open = random.choice(closed_neighbors)
                self.grid[cell_to_open[0], cell_to_open[1]] = 1
                self.open_cells.append(cell_to_open)

                # Visualize and update window
                self.visualize_grid()
                self.window.update()
                # time.sleep(0.05)

    def visualize_grid(self):
        """Visualize the grid in Tkinter window."""
        self.canvas.delete("all")  # Clear the canvas before each redraw

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.grid[x, y] == 0:
                    color = "black"  # Blocked cell
                elif self.grid[x, y] == 1:
                    color = "white"  # Open cell
                else:
                    color = "gray"  # Default

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def create_environment(self):
        """Create the ship environment by opening cells and visualizing the grid."""
        self.initialize_grid()
        self.open_cells_with_neighbors()
        self.identify_and_open_dead_ends()

        # Keep the Tkinter window open after creating the environment
        self.window.mainloop()

# Example usage
if __name__ == "__main__":
    env = ShipEnvironment()
    env.create_environment()
