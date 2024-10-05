import random
from fireSpread import FireSpread
import math

class Bot5:
    def __init__(self, environment, q=0.5, simulations=100):
        """Initialize Bot5 with the environment, flammability parameter q, and number of simulations."""
        self.environment = environment
        self.q = q
        self.bot_position = None
        self.button_position = None
        self.fire_spread = None
        self.simulations = simulations  # Limit number of MCTS simulations per move
        self.visits = {}  # Dictionary to track the number of visits to states
        self.values = {}  # Dictionary to track the value of states

    def initialize(self):
        """Initialize fire, bot, and button ensuring they don't overlap."""
        open_cells = [(x, y) for x in range(self.environment.grid_size)
                      for y in range(self.environment.grid_size)
                      if self.environment.grid[x, y] == 1]  # Only open cells

        # Initialize fire spread
        self.fire_spread = FireSpread(self.environment, self.q)
        fire_start = random.choice(open_cells)
        self.fire_spread.fire_grid[fire_start[0], fire_start[1]] = 1  # Set the fire
        open_cells.remove(fire_start)  # Remove fire-start cell

        # Initialize bot position (it can't be on the fire cell)
        self.bot_position = random.choice(open_cells)
        open_cells.remove(self.bot_position)

        # Initialize button position (it can't be on the fire or bot cell)
        self.button_position = random.choice(open_cells)

    def mcts(self):
        """Perform MCTS to choose the best next move."""
        best_move = None
        best_value = -float('inf')

        # Perform MCTS simulations (Limit number of simulations)
        for _ in range(self.simulations):
            current_position = self.bot_position
            value = self.simulate_mcts(current_position)
            if value > best_value:
                best_value = value
                best_move = self.best_child(current_position)

        return best_move

    def simulate_mcts(self, current_position):
        """Simulate a single MCTS playout (selection, expansion, simulation, backpropagation)."""
        visited_states = []  # Keep track of visited states during the simulation

        # Selection and expansion: traverse the tree
        while current_position != self.button_position and not self.is_terminal_state(current_position):
            visited_states.append(current_position)
            if current_position not in self.visits:
                self.expand_state(current_position)
                break
            current_position = self.best_child(current_position)

        # Simulation: simulate a random playout with early stopping
        reward = self.rollout(current_position)

        # Backpropagation: update the value and visits for each visited state
        for state in visited_states:
            if state not in self.visits:
                self.visits[state] = 0
                self.values[state] = 0
            self.visits[state] += 1
            self.values[state] += reward

        return reward

    def expand_state(self, position):
        """Add a state to the visit and value dictionaries."""
        if position not in self.visits:
            self.visits[position] = 0
            self.values[position] = 0

    def best_child(self, position):
        """Select the best child based on the UCT (Upper Confidence Bound for Trees) formula."""
        neighbors = self.get_neighbors(position)
        best_value = -float('inf')
        best_neighbor = None

        for neighbor in neighbors:
            if neighbor not in self.visits:
                return neighbor  # Prioritize unexplored states

            # UCT formula
            uct_value = (self.values[neighbor] / self.visits[neighbor]) + math.sqrt(2 * math.log(self.visits[position]) / self.visits[neighbor])
            if uct_value > best_value:
                best_value = uct_value
                best_neighbor = neighbor

        return best_neighbor

    def rollout(self, position):
        """Simulate a random rollout from the current position with early stopping."""
        current_position = position
        for _ in range(10):  # Limit the rollout to 10 steps
            neighbors = self.get_neighbors(current_position)
            if not neighbors:
                return -1  # No valid moves, failure

            # Early stopping if near a terminal state (e.g., fire cells close)
            current_position = random.choice(neighbors)
            if current_position == self.button_position:
                return 1  # Success (bot reaches the button)
            if self.fire_spread.fire_grid[current_position[0], current_position[1]] == 1:
                return -1  # Failure (bot steps into fire)

        return 0  # Neutral outcome (no success or failure)

    def is_terminal_state(self, position):
        """Check if the current position is a terminal state."""
        return position == self.button_position or self.fire_spread.fire_grid[position[0], position[1]] == 1

    def get_neighbors(self, position):
        """Get valid neighbors of the current position (open, not on fire, and within bounds)."""
        neighbors = []
        x, y = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.environment.grid_size and 0 <= ny < self.environment.grid_size:
                # Prune neighbors that are on fire or have a high risk
                if self.environment.grid[nx, ny] == 1 and self.fire_spread.fire_grid[nx, ny] == 0:
                    neighbors.append((nx, ny))

        return neighbors

    def move_bot(self):
        """Move the bot one step along the path using MCTS."""
        best_move = self.mcts()
        self.bot_position = best_move  # Update bot's position

    def check_failure(self):
        """Check if the bot failed by stepping into a fire cell."""
        return self.fire_spread.fire_grid[self.bot_position[0], self.bot_position[1]] == 1
