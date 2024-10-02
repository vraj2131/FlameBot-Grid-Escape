# import heapq
# from fireSpread import FireSpread
# import random

# class Bot3:
#     def __init__(self, environment, q=0.5):
#         """Initialize Bot3 with the environment and flammability parameter q."""
#         self.environment = environment
#         self.q = q
#         self.bot_position = None
#         self.button_position = None
#         self.path = []
#         self.fire_spread = None  # Fire spread object will be initialized later

#     def initialize(self):
#         """Initialize fire, bot, and button ensuring they don't overlap."""
#         open_cells = [(x, y) for x in range(self.environment.grid_size)
#                       for y in range(self.environment.grid_size)
#                       if self.environment.grid[x, y] == 1]  # Only open cells

#         # Initialize fire spread
#         self.fire_spread = FireSpread(self.environment, self.q)
#         fire_start = random.choice(open_cells)
#         self.fire_spread.fire_grid[fire_start[0], fire_start[1]] = 1  # Set the fire
#         open_cells.remove(fire_start)  # Remove the fire-start cell from the available open cells

#         # Initialize bot position (it can't be on the fire cell)
#         self.bot_position = random.choice(open_cells)
#         open_cells.remove(self.bot_position)  # Remove the bot's position from available spots

#         # Initialize button position (it can't be on the fire or bot cell)
#         self.button_position = random.choice(open_cells)

#     def manhattan_heuristic(self, a, b):
#         """Calculate the Manhattan distance between points a and b."""
#         return abs(a[0] - b[0]) + abs(a[1] - b[1])

#     def calculate_cell_weight(self, cell):
#         """Calculate the weight of a cell based on the number of burning neighbors."""
#         x, y = cell
#         burning_neighbors = 0
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
#                 if self.fire_spread.fire_grid[nx, ny] == 1:  # Neighbor is on fire
#                     burning_neighbors += 1
#         return burning_neighbors  # Weight is based on burning neighbors

#     def astar_with_weights(self, start, goal):
#         """Perform A* to find the shortest path considering cell weights due to fire proximity."""
#         open_set = []
#         heapq.heappush(open_set, (0, start))  # (priority, node)

#         came_from = {}  # To reconstruct the path later
#         g_score = {start: 0}
#         f_score = {start: self.manhattan_heuristic(start, goal)}

#         while open_set:
#             _, current = heapq.heappop(open_set)

#             if current == goal:
#                 return self.reconstruct_path(came_from, current)

#             # Explore neighbors
#             for neighbor in self.get_neighbors(current):
#                 cell_weight = self.calculate_cell_weight(neighbor)  # Recalculate weight at every step
#                 tentative_g_score = g_score[current] + 1 + cell_weight  # Add cell weight to the score

#                 if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
#                     came_from[neighbor] = current
#                     g_score[neighbor] = tentative_g_score
#                     f_score[neighbor] = tentative_g_score + self.manhattan_heuristic(neighbor, goal)
#                     heapq.heappush(open_set, (f_score[neighbor], neighbor))
#         return []  # No valid path found

#     def get_neighbors(self, current):
#         """Get valid neighbors of the current position (open, not on fire, and within bounds)."""
#         neighbors = []
#         x, y = current
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
#                 if self.environment.grid[nx, ny] == 1 and self.fire_spread.fire_grid[nx, ny] == 0:  # Cell is open and not on fire
#                     neighbors.append((nx, ny))

#         return neighbors

#     def reconstruct_path(self, came_from, current):
#         """Reconstruct the path from start to goal by backtracking."""
#         total_path = [current]
#         while current in came_from:
#             current = came_from[current]
#             total_path.append(current)
#         total_path.reverse()
#         return total_path

#     def move_bot(self):
#         """Move the bot one step along the path if a path exists."""
#         if self.path:
#             self.bot_position = self.path.pop(0)  # Move to the next step in the path

#     def plan_path(self):
#         """Plan the path from bot to button, considering fire and proximity to fire."""
#         self.path = self.astar_with_weights(self.bot_position, self.button_position)

#     def check_failure(self):
#         """Check if the bot failed by stepping into a fire cell."""
#         if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
#             return True
#         return False


import heapq
from fireSpread import FireSpread
import random

class Bot3:
    def __init__(self, environment, q=0.5):
        """Initialize Bot3 with the environment and flammability parameter q."""
        self.environment = environment
        self.q = q
        self.bot_position = None
        self.button_position = None
        self.path = []
        self.fire_spread = None  # Fire spread object will be initialized later
        self.visited_nodes = set()  # Keep track of visited nodes for backtracking

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

    def manhattan_heuristic(self, a, b):
        """Calculate the Manhattan distance between points a and b."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def calculate_cell_weight(self, cell):
        """Calculate the weight of a cell based on the number of burning neighbors."""
        x, y = cell
        burning_neighbors = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
                if self.fire_spread.fire_grid[nx, ny] == 1:  # Neighbor is on fire
                    burning_neighbors += 1
        return burning_neighbors  # Weight is based on burning neighbors

    def astar_with_backtracking(self, start, goal):
        """Perform A* to find the shortest path considering cell weights due to fire proximity."""
        open_set = []
        heapq.heappush(open_set, (0, start))  # (priority, node)

        came_from = {}  # To reconstruct the path later
        g_score = {start: 0}
        f_score = {start: self.manhattan_heuristic(start, goal)}

        self.visited_nodes.clear()  # Clear visited nodes to allow backtracking

        while open_set:
            _, current = heapq.heappop(open_set)

            # If the goal is reached, reconstruct and return the path
            if current == goal:
                return self.reconstruct_path(came_from, current)

            self.visited_nodes.add(current)

            # Explore neighbors
            for neighbor in self.get_neighbors(current):
                cell_weight = self.calculate_cell_weight(neighbor)  # Recalculate weight at every step
                tentative_g_score = g_score[current] + 1 + cell_weight  # Add cell weight to the score

                # Allow backtracking by considering nodes even if they are already visited,
                # but only if the new path to the neighbor is less costly than the previous one.
                if neighbor in self.visited_nodes and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue  # Skip if the neighbor has been visited and the new path is not better

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.manhattan_heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No valid path found

    def get_neighbors(self, current):
        """Get valid neighbors of the current position (open, not on fire, and within bounds)."""
        neighbors = []
        x, y = current
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
                if self.environment.grid[nx, ny] == 1 and self.fire_spread.fire_grid[nx, ny] == 0:  # Cell is open and not on fire
                    neighbors.append((nx, ny))

        return neighbors

    def reconstruct_path(self, came_from, current):
        """Reconstruct the path from start to goal by backtracking."""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def move_bot(self):
        """Move the bot one step along the path if a path exists."""
        if self.path:
            self.bot_position = self.path.pop(0)  # Move to the next step in the path

    def plan_path(self):
        """Plan the path from bot to button, considering fire and proximity to fire."""
        self.path = self.astar_with_backtracking(self.bot_position, self.button_position)

    def check_failure(self):
        """Check if the bot failed by stepping into a fire cell."""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False
