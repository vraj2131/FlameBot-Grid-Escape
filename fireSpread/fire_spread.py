import random
import numpy as np

class FireSpread:
    def __init__(self, environment, q=0.5):
        self.environment = environment  
        self.q = q  
        self.fire_grid = np.zeros_like(self.environment.grid)  

    def initialize_fire(self):
        """Start fire at a random open cell."""
        open_cells = [(x, y) for x in range(self.environment.grid_size)
                      for y in range(self.environment.grid_size)
                      if self.environment.grid[x, y] == 1]  
        fire_start = random.choice(open_cells)
        # 1 is fire, 0 is  not fire
        self.fire_grid[fire_start[0], fire_start[1]] = 1  
        return fire_start

    def spread_fire(self):
        """Spread the fire as per given in docs."""
        # updating on a copy and then setting it as the actual grid
        new_fire_grid = np.copy(self.fire_grid)  

        for x in range(1, self.environment.grid_size - 1):
            for y in range(1, self.environment.grid_size - 1):
                if self.environment.grid[x, y] == 1 and self.fire_grid[x, y] == 0:  
                    burning_neighbors = self.count_burning_neighbors(x, y)
                    if burning_neighbors > 0:
                        # Compute the probability 
                        fire_probability = 1 - (1 - self.q) ** burning_neighbors
                        if random.random() < fire_probability:
                            new_fire_grid[x, y] = 1  # Set the cell on fire

        self.fire_grid = new_fire_grid  

    def count_burning_neighbors(self, x, y):
        """Count burning neighbors."""
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] 
        burning_neighbors = 0
        for res_x, res_y in neighbors:
            if 0 <= res_x < self.environment.grid_size and 0 <= res_y < self.environment.grid_size:
                if self.fire_grid[res_x, res_y] == 1:  
                    burning_neighbors += 1
        return burning_neighbors
