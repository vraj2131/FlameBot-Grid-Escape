from collections import deque
from fireSpread import FireSpread
import random

class Bot1:
    def __init__(self, environment, q=0.5):
        """Initialize Bot1."""
        self.environment = environment
        self.q = q
        self.bot_position = None
        self.button_position = None
        self.path = []
        self.fire_spread = None  

    def initialize(self):
        """Initialize fire, bot, and button cells."""
        open_cells = [(x, y) for x in range(self.environment.grid_size)
                      for y in range(self.environment.grid_size)
                      if self.environment.grid[x, y] == 1]  

        # Fire spread
        self.fire_spread = FireSpread(self.environment, self.q)
        fire_start = random.choice(open_cells)
        self.fire_spread.fire_grid[fire_start[0], fire_start[1]] = 1  
        open_cells.remove(fire_start)  

        # Bot position
        self.bot_position = random.choice(open_cells)
        open_cells.remove(self.bot_position)  

        # Button Position
        self.button_position = random.choice(open_cells)

    def bfs(self, start, goal):
        """Perform BFS to find shortest path"""
        queue = deque([(start, [])])  
        visited = set()
        visited.add(start)

        # movement in 4 directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == goal:
                return path + [(x, y)]

            # Explore neighbors
            for dx, dy in directions:
                res_x, res_y = x + dx, y + dy

                # Check if the neighbor is valid 
                if 0 <= res_x < self.environment.grid_size and 0 <= res_y < self.environment.grid_size:
                    if (res_x, res_y) not in visited and self.environment.grid[res_x, res_y] == 1 and self.fire_spread.fire_grid[res_x, res_y] == 0:
                        visited.add((res_x, res_y))
                        queue.append(((res_x, res_y), path + [(x, y)]))
        
        # no path found
        return []

    def move_bot(self):
        """Move the bot to next step."""
        if self.path:
            self.bot_position = self.path.pop(0)  

    def plan_path(self):
        """Plan the path from bot to button"""
        self.path = self.bfs(self.bot_position, self.button_position)

    def check_failure(self):
        """Checking for failure"""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False
