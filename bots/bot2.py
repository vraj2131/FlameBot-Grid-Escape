from fireSpread import FireSpread
import heapq
import random

class Bot2:
    def __init__(self, environment, q=0.5):
        """Initialize Bot2 with the environment and flammability parameter q."""
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

    def manhattan_heuristic(self, a, b):
        """Calculate the Manhattan distance between points a and b."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self, start, goal):
        """Perform A* to find the shortest path from start to goal avoiding fire and blocked cells."""
        open_set = []
        heapq.heappush(open_set, (0, start))  # (priority, node)

        came_from = {}  # To reconstruct the path later
        g_score = {start: 0}
        f_score = {start: self.manhattan_heuristic(start, goal)}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            # If goal is reached, reconstruct and return the path
            if current == goal:
                return self.reconstruct_path(came_from, current)

            visited.add(current)

            # Explore neighbors
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.manhattan_heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Return an empty path if no valid path is found
        return []

    def get_neighbors(self, current):
        """Get valid neighbors of the current position (open, not on fire, and within bounds)."""
        neighbors = []
        x, y = current
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
                if self.environment.grid[nx, ny] == 1 and self.fire_spread.fire_grid[nx, ny] == 0:
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
        """Move the bot one step along the path if a path exists and it's safe."""
        if self.path:
            # Check if the next step in the path is safe
            next_step = self.path[0]
            if self.fire_spread.fire_grid[next_step[0], next_step[1]] == 0:  # Next step is not on fire
                self.bot_position = self.path.pop(0)  # Move to the next step in the path
            else:
                # Fire has spread to the path, recalculate a new path
                self.plan_path()
        else:
            # No path exists or the path was blocked, recalculate
            self.plan_path()

    def plan_path(self):
        """Plan the path from bot to button, ignoring the initial fire position."""
        self.path = self.astar(self.bot_position, self.button_position)

    def check_failure(self):
        """Check if the bot failed by stepping into a fire cell."""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False
