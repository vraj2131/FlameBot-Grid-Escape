import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class ShipEnvironment:
    def __init__(self, grid_size=40):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))  # Start with all cells blocked (0 represents blocked)
        self.open_cells = []

    def initialize_grid(self):
        # Randomly choose an interior cell to open
        start_x = random.randint(1, self.grid_size - 2)
        start_y = random.randint(1, self.grid_size - 2)
        self.grid[start_x, start_y] = 1  # Open the cell (1 represents open)
        self.open_cells.append((start_x, start_y))

    def open_cells_with_neighbors(self):
        # Keep opening cells until no more candidates exist
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

    def visualize_grid(self):
        """Visualize the grid with visible cell boundaries."""
        fig, ax = plt.subplots()
        cmap = colors.ListedColormap(['black', 'white'])  # Black for blocked, white for open
        bounds = [0, 0.5, 1]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        # Display grid with boundaries
        ax.imshow(self.grid, cmap=cmap, norm=norm)

        # Draw grid lines
        ax.set_xticks(np.arange(-0.5, self.grid_size, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.grid_size, 1), minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=2)

        # Set the grid lines to cover the cells
        ax.tick_params(which="minor", size=0)

        plt.title(f'{self.grid_size}x{self.grid_size} Grid Layout with Boundaries')
        plt.show()

    def create_environment(self):
        """Create the ship environment by opening cells and visualizing the grid."""
        self.initialize_grid()
        self.open_cells_with_neighbors()
        self.identify_and_open_dead_ends()
        self.visualize_grid()


