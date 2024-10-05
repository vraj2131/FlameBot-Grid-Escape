# import random
# from collections import defaultdict, deque
# from fireSpread import FireSpread

# # class Bot4:
# #     def __init__(self, environment, q=0.5):
# #         """Initialize Bot4 with the environment and flammability parameter q."""
# #         self.environment = environment
# #         self.q = q
# #         self.bot_position = None
# #         self.button_position = None
# #         self.fire_spread = None  # Fire spread object will be initialized later
# #         self.simulation_count = 100  # Number of simulations per move
# #         self.visited_cells = deque(maxlen=5)  # Short-term memory to avoid oscillation

# #     def initialize(self):
# #         """Initialize fire, bot, and button ensuring they don't overlap."""
# #         open_cells = [(x, y) for x in range(self.environment.grid_size)
# #                       for y in range(self.environment.grid_size)
# #                       if self.environment.grid[x, y] == 1]  # Only open cells

# #         # Initialize fire spread
# #         self.fire_spread = FireSpread(self.environment, self.q)
# #         fire_start = random.choice(open_cells)
# #         self.fire_spread.fire_grid[fire_start[0], fire_start[1]] = 1  # Set the fire
# #         open_cells.remove(fire_start)

# #         # Initialize bot and button positions
# #         self.bot_position = random.choice(open_cells)
# #         open_cells.remove(self.bot_position)
# #         self.button_position = random.choice(open_cells)

# #     def get_neighbors(self, position):
# #         """Get valid neighbors of the current position (open, not on fire, and within bounds)."""
# #         x, y = position
# #         neighbors = []
# #         fire_adjacent_neighbors = []  # Track neighbors adjacent to fire
# #         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
# #         for dx, dy in directions:
# #             nx, ny = x + dx, y + dy
# #             if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
# #                 if self.environment.grid[nx, ny] == 1 and self.fire_spread.fire_grid[nx, ny] == 0:
# #                     if not self.is_adjacent_to_fire((nx, ny)):
# #                         neighbors.append((nx, ny))  # Safe neighbor (not adjacent to fire)
# #                     else:
# #                         fire_adjacent_neighbors.append((nx, ny))  # Adjacent to fire
        
# #         # If no safe neighbors, use fire-adjacent ones
# #         return neighbors if neighbors else fire_adjacent_neighbors

# #     def is_adjacent_to_fire(self, cell):
# #         """Check if the given cell is adjacent to a fire cell."""
# #         x, y = cell
# #         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# #         for dx, dy in directions:
# #             nx, ny = x + dx, y + dy
# #             if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
# #                 if self.fire_spread.fire_grid[nx, ny] == 1:  # Adjacent cell is on fire
# #                     return True
# #         return False

# #     def greedy_selection(self, position):
# #         """Select the next move based on immediate reward (greedy policy)."""
# #         neighbors = self.get_neighbors(position)

# #         # Apply penalty to recently visited cells
# #         neighbors_with_penalty = [(n, self.manhattan_distance(n, self.button_position) +
# #                                    (5 if n in self.visited_cells else 0)) for n in neighbors]

# #         # Greedily select the neighbor closest to the button, considering penalties
# #         best_move = min(neighbors_with_penalty, key=lambda item: item[1])[0]

# #         return best_move

# #     def manhattan_distance(self, a, b):
# #         """Calculate the Manhattan distance between points a and b."""
# #         return abs(a[0] - b[0]) + abs(a[1] - b[1])

# #     def simulate(self, position):
# #         """Simulate greedy path to the button."""
# #         current_position = position
# #         for _ in range(100):  # Simulate 100 steps
# #             current_position = self.greedy_selection(current_position)
# #             if current_position == self.button_position:
# #                 return 1  # Successful path
# #             if self.fire_spread.fire_grid[current_position[0], current_position[1]] == 1:
# #                 return 0  # Failure
# #         return 0  # Simulation ended without success

# #     def move_bot(self):
# #         """Perform Greedy MCTS to select the next move."""
# #         best_move = None
# #         best_score = -1

# #         # Simulate all possible moves and pick the one with the highest score
# #         for _ in range(self.simulation_count):
# #             current_move = self.greedy_selection(self.bot_position)
# #             score = self.simulate(current_move)
# #             if score > best_score:
# #                 best_score = score
# #                 best_move = current_move

# #         # Move to the best position found
# #         if best_move:
# #             self.bot_position = best_move
# #             self.visited_cells.append(self.bot_position)  # Track the visited cell to prevent oscillation

# #     def check_failure(self):
# #         """Check if the bot stepped into a fire cell."""
# #         return self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1

# class Bot4:
#     def __init__(self, environment, q=0.5):
#         """Initialize Bot4 with the environment and flammability parameter q."""
#         self.environment = environment
#         self.q = q
#         self.bot_position = None
#         self.button_position = None
#         self.fire_spread = None  # Fire spread object will be initialized later
#         self.simulation_count = 100  # Number of simulations per move
#         self.visited_cells = deque(maxlen=5)  # Short-term memory to avoid oscillation
#         self.backtrack_stack = []  # Stack for backtracking in case of failure

#     def initialize(self):
#         """Initialize fire, bot, and button ensuring they don't overlap."""
#         open_cells = [(x, y) for x in range(self.environment.grid_size)
#                       for y in range(self.environment.grid_size)
#                       if self.environment.grid[x, y] == 1]  # Only open cells

#         # Initialize fire spread
#         self.fire_spread = FireSpread(self.environment, self.q)
#         fire_start = random.choice(open_cells)
#         self.fire_spread.fire_grid[fire_start[0], fire_start[1]] = 1  # Set the fire
#         open_cells.remove(fire_start)

#         # Initialize bot and button positions
#         self.bot_position = random.choice(open_cells)
#         open_cells.remove(self.bot_position)
#         self.button_position = random.choice(open_cells)

#     def get_neighbors(self, position):
#         """Get valid neighbors of the current position (open, not on fire, and within bounds)."""
#         x, y = position
#         neighbors = []
#         fire_adjacent_neighbors = []  # Track neighbors adjacent to fire
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
#                 if self.environment.grid[nx, ny] == 1 and self.fire_spread.fire_grid[nx, ny] == 0:
#                     if not self.is_adjacent_to_fire((nx, ny)):
#                         neighbors.append((nx, ny))  # Safe neighbor (not adjacent to fire)
#                     else:
#                         fire_adjacent_neighbors.append((nx, ny))  # Adjacent to fire
        
#         # If no safe neighbors, use fire-adjacent ones
#         return neighbors if neighbors else fire_adjacent_neighbors

#     def is_adjacent_to_fire(self, cell):
#         """Check if the given cell is adjacent to a fire cell."""
#         x, y = cell
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
#                 if self.fire_spread.fire_grid[nx, ny] == 1:  # Adjacent cell is on fire
#                     return True
#         return False

#     def fire_within_range(self, position, range_limit=3):
#         """Check if any fire is within a given range (Manhattan distance)."""
#         x, y = position
#         for dx in range(-range_limit, range_limit + 1):
#             for dy in range(-range_limit, range_limit + 1):
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
#                     if self.fire_spread.fire_grid[nx, ny] == 1:  # Fire within the range
#                         return True
#         return False

#     def greedy_selection(self, position):
#         """Select the next move based on immediate reward (greedy policy)."""
#         neighbors = self.get_neighbors(position)

#         # Apply penalty to recently visited cells
#         neighbors_with_penalty = [(n, self.manhattan_distance(n, self.button_position) +
#                                    (5 if n in self.visited_cells else 0)) for n in neighbors]

#         # Prioritize reaching the button unless fire is near
#         if self.fire_within_range(position):
#             # Consider fire avoidance logic if fire is within 3 cells
#             safe_neighbors = [n for n in neighbors_with_penalty if not self.is_adjacent_to_fire(n[0])]
#             if safe_neighbors:
#                 neighbors_with_penalty = safe_neighbors

#         # Greedily select the neighbor closest to the button, considering penalties
#         best_move = min(neighbors_with_penalty, key=lambda item: item[1])[0]
        
#         return best_move

#     def manhattan_distance(self, a, b):
#         """Calculate the Manhattan distance between points a and b."""
#         return abs(a[0] - b[0]) + abs(a[1] - b[1])

#     def simulate(self, position):
#         """Simulate greedy path to the button."""
#         current_position = position
#         for _ in range(100):  # Simulate 100 steps
#             current_position = self.greedy_selection(current_position)
#             if current_position == self.button_position:
#                 return 1  # Successful path
#             if self.fire_spread.fire_grid[current_position[0], current_position[1]] == 1:
#                 return 0  # Failure
#         return 0  # Simulation ended without success

#     def move_bot(self):
#         """Perform Greedy MCTS to select the next move."""
#         best_move = None
#         best_score = -1
#         current_move = self.greedy_selection(self.bot_position)
        
#         # Simulate all possible moves and pick the one with the highest score
#         for _ in range(self.simulation_count):
#             score = self.simulate(current_move)
#             if score > best_score:
#                 best_score = score
#                 best_move = current_move

#         # Move to the best position found and track for backpropagation
#         if best_move:
#             self.backtrack_stack.append(self.bot_position)  # Save the position before moving
#             self.bot_position = best_move
#             self.visited_cells.append(self.bot_position)  # Track the visited cell to prevent oscillation

#     def backpropagate(self):
#         """Backtrack to previous positions if a better path is found or failure occurs."""
#         if self.backtrack_stack:
#             # Move back to a previous position in case of failure or suboptimal choice
#             self.bot_position = self.backtrack_stack.pop()

#     def check_failure(self):
#         """Check if the bot stepped into a fire cell."""
#         return self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1

import heapq
import random
from fireSpread import FireSpread

class Bot4:
    def __init__(self, environment, q=0.5, alpha=2):
        """Initialize Bot4 with the environment, flammability parameter q, and risk factor alpha."""
        self.environment = environment
        self.q = q
        self.alpha = alpha  # Weighting factor for risk vs reward
        self.bot_position = None
        self.button_position = None
        self.path = []
        self.fire_spread = None  # Fire spread object will be initialized later
        self.visited_nodes = set()

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

    def calculate_fire_risk(self, cell):
        """Calculate the risk score of a cell based on the fire spread probability."""
        x, y = cell
        burning_neighbors = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
                if self.fire_spread.fire_grid[nx, ny] == 1:  # Neighbor is on fire
                    burning_neighbors += 1
        # Calculate the probability of the cell catching fire in the next step
        fire_probability = 1 - (1 - self.q) ** burning_neighbors
        return fire_probability

    def combined_score(self, current, goal):
        """Calculate the combined score of a cell based on risk and reward (distance to button)."""
        distance_to_goal = self.manhattan_heuristic(current, goal)
        fire_risk = self.calculate_fire_risk(current)
        
        # Prioritize safety heavily if near fire
        if fire_risk > 0:
            fire_risk *= 10  # Increase weight of fire risk in the score
            
        # The combined score considers both the distance (reward) and the fire risk
        return distance_to_goal - self.alpha * fire_risk

    def greedy_best_first_search(self, start, goal):
        """Greedy Best-First Search: Chooses paths based on distance to goal and fire risk."""
        open_set = []
        heapq.heappush(open_set, (0, start))  # (priority, node)

        came_from = {}  # To reconstruct the path later
        self.visited_nodes.clear()  # Clear visited nodes

        while open_set:
            _, current = heapq.heappop(open_set)

            # If the goal is reached, reconstruct and return the path
            if current == goal:
                return self.reconstruct_path(came_from, current)

            self.visited_nodes.add(current)

            # Explore neighbors
            for neighbor in self.get_neighbors(current):
                # Calculate the combined score for the neighbor
                score = self.combined_score(neighbor, goal)

                if neighbor not in self.visited_nodes:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (score, neighbor))

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
        """Move the bot one step along the path if a path exists, and check for fire risk."""
        if self.path:
            next_position = self.path[0]
            # Check if the next position is on fire
            if self.fire_spread.fire_grid[next_position[0], next_position[1]] == 1:
                print("Next position is on fire. Checking alternative paths...")
                self.path = self.greedy_best_first_search(self.bot_position, self.button_position)  # Replan if next move is invalid

            if self.path and self.path[0] != next_position:  # If path changed
                print(f"Replanned path: {self.path}")

            if self.path:
                self.bot_position = self.path.pop(0)  # Move to the next step in the path
                print(f"Bot moved to: {self.bot_position}")

    def plan_path(self):
        """Plan the path from bot to button, considering fire and proximity to fire."""
        self.path = self.greedy_best_first_search(self.bot_position, self.button_position)

    def check_failure(self):
        """Check if the bot failed by stepping into a fire cell."""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False


