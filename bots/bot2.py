from fireSpread import FireSpread
import heapq
import random

class Bot2:
    def __init__(self, environment, q=0.5):
        """Initialize Bot2"""
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

        # Bot Position
        self.bot_position = random.choice(open_cells)
        open_cells.remove(self.bot_position)  

        # Button position
        self.button_position = random.choice(open_cells)

    def manhattan_heuristic(self, a, b):
        """Manhattan distance between points a and b."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self, start, goal):
        """Use A* to find the path, ignore fire cells"""
        open_set = []
        heapq.heappush(open_set, (0, start))  

        came_from = {}  
        g_score = {start: 0}
        f_score = {start: self.manhattan_heuristic(start, goal)}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

           
            if current == goal:
                return self.reconstruct_path(came_from, current)

            visited.add(current)

            # Explore neighbors
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue

                temp_g_score = g_score[current] + 1

                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.manhattan_heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # No path found
        return []

    def get_neighbors(self, current):
        """Get neighbors."""
        neighbors = []
        x, y = current
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

        for dx, dy in directions:
            res_x, res_y = x + dx, y + dy
            if 0 <= res_x < self.environment.grid_size and 0 <= res_y < self.environment.grid_size:
                if self.environment.grid[res_x, res_y] == 1 and self.fire_spread.fire_grid[res_x, res_y] == 0:
                    neighbors.append((res_x, res_y))

        return neighbors

    def reconstruct_path(self, came_from, current):
        """Get the path"""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path
    
    def move_bot(self):
        """Move the bot to next step"""
        if self.path:
            # next step safe or not
            next_step = self.path[0]
            if self.fire_spread.fire_grid[next_step[0], next_step[1]] == 0: 
                self.bot_position = self.path.pop(0)  
            else:
                # replan the path
                self.plan_path()
        else:
            # replan the path
            self.plan_path()

    def plan_path(self):
        """Plan the path from bot to button"""
        self.path = self.astar(self.bot_position, self.button_position)

    def check_failure(self):
        """Checking for failure"""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False
