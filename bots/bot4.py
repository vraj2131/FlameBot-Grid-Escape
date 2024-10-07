import heapq
import random
from fireSpread import FireSpread

class Bot4:
    def __init__(self, environment, q=0.5, alpha=2):
        """Initialize Bot with the environment, flammability parameter q, and risk factor alpha."""
        self.environment = environment
        self.q = q
        self.alpha = alpha  # Weighting factor for risk vs reward
        self.bot_position = None
        self.button_position = None
        self.fire_spread = None  # Fire spread object will be initialized later
        self.g = {}
        self.rhs = {}
        self.queue = []
        self.km = 0
        self.last_bot_position = None

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

        # Initialize D* Lite variables
        self.g = {}
        self.rhs = {}
        for x in range(self.environment.grid_size):
            for y in range(self.environment.grid_size):
                self.g[(x, y)] = float('inf')
                self.rhs[(x, y)] = float('inf')

        self.rhs[self.button_position] = 0
        self.queue = []
        self.km = 0
        self.last_bot_position = self.bot_position

        # Push the goal (button position) to the queue
        heapq.heappush(self.queue, (self.calculate_key(self.button_position), self.button_position))

    def manhattan_heuristic(self, a, b):
        """Calculate the Manhattan distance between points a and b."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def calculate_key(self, s):
        """Calculate the priority queue key for node s."""
        g_rhs_min = min(self.g[s], self.rhs[s])
        return (g_rhs_min + self.manhattan_heuristic(self.bot_position, s) + self.km, g_rhs_min)

    def update_vertex(self, u):
        """Update a vertex in the queue."""
        if u != self.button_position:
            min_rhs = float('inf')
            for neighbor in self.get_neighbors(u):
                min_rhs = min(min_rhs, self.g[neighbor] + 1)  # Assume uniform cost (1)
            self.rhs[u] = min_rhs

        # Remove u from the queue if it's already in
        if (self.calculate_key(u), u) in self.queue:
            self.queue.remove((self.calculate_key(u), u))
            heapq.heapify(self.queue)

        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.queue, (self.calculate_key(u), u))

    def compute_shortest_path(self):
        """Compute the shortest path incrementally using D* Lite."""
        while self.queue and (self.queue[0][0] < self.calculate_key(self.bot_position) or self.rhs[self.bot_position] != self.g[self.bot_position]):
            k_old, u = heapq.heappop(self.queue)
            k_new = self.calculate_key(u)

            if k_old < k_new:
                heapq.heappush(self.queue, (k_new, u))
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for neighbor in self.get_neighbors(u):
                    self.update_vertex(neighbor)
            else:
                g_old = self.g[u]
                self.g[u] = float('inf')
                for neighbor in self.get_neighbors(u) + [u]:
                    self.update_vertex(neighbor)

    def move_bot(self):
        """Move the bot one step along the path if possible, and replan if necessary."""
        if self.bot_position == self.button_position:
            return  # Bot has reached the goal

        # Check if the bot position has changed and update the heuristic
        if self.bot_position != self.last_bot_position:
            self.km += self.manhattan_heuristic(self.last_bot_position, self.bot_position)
            self.last_bot_position = self.bot_position

        self.compute_shortest_path()

        # Move to the best neighbor
        min_cost = float('inf')
        next_position = self.bot_position

        for neighbor in self.get_neighbors(self.bot_position):
            cost = self.g[neighbor] + 1  # Cost is the g-value of the neighbor plus the step cost (1)
            if cost < min_cost:
                min_cost = cost
                next_position = neighbor

        # If next position is valid and not on fire, move the bot
        if self.fire_spread.fire_grid[next_position[0], next_position[1]] == 1:
            # print("Next position is on fire. Replanning...")
            self.compute_shortest_path()  # Recompute the path if the next move is invalid
        else:
            self.bot_position = next_position

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

    def check_failure(self):
        """Check if the bot failed by stepping into a fire cell."""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False
