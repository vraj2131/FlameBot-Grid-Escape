import heapq
import random
from fireSpread import FireSpread

class Bot4:
    def __init__(self, environment, q=0.5, alpha=2):
        """Initialize Bot4"""
        self.environment = environment
        self.q = q
        self.alpha = alpha  # weight factor (will be used for risk and reward)
        self.bot_position = None
        self.button_position = None
        self.fire_spread = None
        # g and rhs values used for risk assessment  
        self.g = {}
        self.rhs = {}
        self.queue = []
        # heuristic used for priority
        self.key_modifier = 0
        self.last_bot_position = None

    def initialize(self):
        """Initialize fire, bot, and button"""
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

        # Button position
        self.button_position = random.choice(open_cells)

        # D* Lite variables
        self.g = {}
        self.rhs = {}
        # Set to inf
        for x in range(self.environment.grid_size):
            for y in range(self.environment.grid_size):
                self.g[(x, y)] = float('inf')
                self.rhs[(x, y)] = float('inf')

        self.rhs[self.button_position] = 0
        self.queue = []
        self.key_modifier = 0
        self.last_bot_position = self.bot_position

        # goal pushed to queue
        heapq.heappush(self.queue, (self.calculate_key(self.button_position), self.button_position))

    def manhattan_heuristic(self, a, b):
        """Manhattan distance between points a and b."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def calculate_key(self, s):
        """Priority key for a node"""
        g_rhs_min = min(self.g[s], self.rhs[s])
        return (g_rhs_min + self.manhattan_heuristic(self.bot_position, s) + self.key_modifier, g_rhs_min)

    def update_vertex(self, u):
        """Update vertex in the queue."""
        if u != self.button_position:
            min_rhs = float('inf')
            for neighbor in self.get_neighbors(u):
                min_rhs = min(min_rhs, self.g[neighbor] + 1)  
            self.rhs[u] = min_rhs

        # Remove node from the queue if it's already in
        if (self.calculate_key(u), u) in self.queue:
            self.queue.remove((self.calculate_key(u), u))
            heapq.heapify(self.queue)

        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.queue, (self.calculate_key(u), u))

    def compute_shortest_path(self):
        """Find shortest path incrementally, used D* Lite."""
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
        """Move the bot to next step"""
        if self.bot_position == self.button_position:
            return  

        # Update heuristic
        if self.bot_position != self.last_bot_position:
            self.key_modifier += self.manhattan_heuristic(self.last_bot_position, self.bot_position)
            self.last_bot_position = self.bot_position

        self.compute_shortest_path()

        # moving to best neighbor
        min_cost = float('inf')
        next_position = self.bot_position

        for neighbor in self.get_neighbors(self.bot_position):
            cost = self.g[neighbor] + 1  
            if cost < min_cost:
                min_cost = cost
                next_position = neighbor

  
        if self.fire_spread.fire_grid[next_position[0], next_position[1]] == 1:
            self.compute_shortest_path()  
        else:
            self.bot_position = next_position

    def get_neighbors(self, current):
        """Get neighbors"""
        neighbors = []
        x, y = current
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for dx, dy in directions:
            res_x, res_y = x + dx, y + dy
            if 0 <= res_x < self.environment.grid_size and 0 <= res_y < self.environment.grid_size:
                if self.environment.grid[res_x, res_y] == 1 and self.fire_spread.fire_grid[res_x, res_y] == 0: 
                    neighbors.append((res_x, res_y))

        return neighbors

    def check_failure(self):
        """Checking for failure"""
        if self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1:
            return True
        return False
