from collections import deque
from fireSpread import FireSpread
import random

class Bot1:
    def __init__(self, environment, q=0.5):
        """Initialize Bot1 with the environment and flammability parameter q."""
        self.environment = environment
        self.q = q
        self.bot_position = None
        self.button_position = None
        self.path = []
        self.fire_spread = None  # Fire spread object will be initialized later

    def initialize(self):
        """Initialize fire, bot, and button ensuring they don't overlap."""
        open_cells = [(x, y) for x in range(self.environment.grid_size)
                      for y in range(self.environment.grid_size)
                      if self.environment.grid[x, y] == 1]  # Only open cells

        # Initialize fire spread
        self.fire_spread = FireSpread(self.environment, self.q)
        fire_start = random.choice(open_cells)
        self.fire_spread.fire_grid[fire_start[0], fire_start[1]] = 1  # Set the fire
        open_cells.remove(fire_start)  # Remove the fire-start cell from the available open cells

        # Initialize bot position (it can't be on the fire cell)
        self.bot_position = random.choice(open_cells)
        open_cells.remove(self.bot_position)  # Remove the bot's position from available spots

        # Initialize button position (it can't be on the fire or bot cell)
        self.button_position = random.choice(open_cells)

    def bfs(self, start, goal):
        """Perform BFS to find the shortest path from start to goal avoiding fire and blocked cells."""
        queue = deque([(start, [])])  # Queue holds (current_position, path_taken)
        visited = set()
        visited.add(start)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

        while queue:
            (x, y), path = queue.popleft()

            # If goal is reached, return the path
            if (x, y) == goal:
                return path + [(x, y)]

            # Explore neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Check if the neighbor is valid (open, not visited, and not on fire)
                if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
                    if (nx, ny) not in visited and self.environment.grid[nx, ny] == 1 and self.fire_spread.fire_grid[nx, ny] == 0:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(x, y)]))
        
        # If no path found, return an empty list
        return []

    def move_bot(self):
        """Move the bot one step along the path if a path exists."""
        if self.path:
            self.bot_position = self.path.pop(0)  # Move to the next step in the path

    def plan_path(self):
        """Plan the path from bot to button, ignoring the initial fire position."""
        self.path = self.bfs(self.bot_position, self.button_position)

    def check_failure(self):
        """Check if the bot failed by stepping into a fire cell."""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False
