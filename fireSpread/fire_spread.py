import random
import numpy as np

class FireSpread:
    def __init__(self, environment, q=0.5):
        self.environment = environment  # Ship environment grid
        self.q = q  # Flammability parameter
        self.fire_grid = np.zeros_like(self.environment.grid)  # Fire status grid (0 = not on fire, 1 = on fire)

    def initialize_fire(self):
        """Initialize the fire at a random open cell."""
        open_cells = [(x, y) for x in range(self.environment.grid_size)
                      for y in range(self.environment.grid_size)
                      if self.environment.grid[x, y] == 1]  # Only open cells
        fire_start = random.choice(open_cells)
        self.fire_grid[fire_start[0], fire_start[1]] = 1  # Set the chosen cell on fire
        return fire_start

    def spread_fire(self):
        """Spread the fire based on the rules."""
        new_fire_grid = np.copy(self.fire_grid)  # Create a copy of the fire grid to apply updates simultaneously

        for x in range(1, self.environment.grid_size - 1):
            for y in range(1, self.environment.grid_size - 1):
                if self.environment.grid[x, y] == 1 and self.fire_grid[x, y] == 0:  # Open and not on fire
                    # Count the number of neighboring cells that are on fire
                    burning_neighbors = self.count_burning_neighbors(x, y)
                    if burning_neighbors > 0:
                        # Compute the probability that this cell catches fire
                        fire_probability = 1 - (1 - self.q) ** burning_neighbors
                        if random.random() < fire_probability:
                            new_fire_grid[x, y] = 1  # Set the cell on fire in the new grid

        self.fire_grid = new_fire_grid  # Update the fire grid

    def count_burning_neighbors(self, x, y):
        """Count how many neighboring cells of (x, y) are on fire."""
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # Only up/down/left/right neighbors
        burning_neighbors = 0
        for nx, ny in neighbors:
            if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
                if self.fire_grid[nx, ny] == 1:  # Neighbor is on fire
                    burning_neighbors += 1
        return burning_neighbors
