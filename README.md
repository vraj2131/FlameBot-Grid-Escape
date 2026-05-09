# FlameBot: Grid Escape Under Dynamic Constraints

A grid-based simulation framework that studies autonomous agent (bot) navigation in environments where the cost field changes every tick. The bot must reach a goal cell while fire spreads stochastically across the grid, blocking cells over time. The project implements and benchmarks several pathfinding strategies under dynamic, partially-predictable obstacles.

The problem is a clean abstraction of real-world dynamic-routing tasks: a planner must commit to a path now, but the world it planned over is no longer the world it has to traverse.

---

## Problem

A bot is placed on an `N x N` grid containing:

- **Open cells** — traversable
- **Blocked cells** — permanent obstacles (sampled at start with a configurable density)
- **Fire cells** — initially seeded at one cell, then spread stochastically each tick to neighboring open cells with a probability that scales with the number of burning neighbors and a global spread rate `q`
- **Goal cell** — the exit

Each tick:
1. The fire spreads.
2. The bot observes the grid (fully or partially, depending on the bot variant) and decides on its next move.
3. The bot moves one cell.

The bot wins if it reaches the goal. It loses if it steps onto fire, is surrounded by fire, or fire reaches the goal first.

---

## Bot Strategies

Four bots of increasing sophistication are implemented and compared:

| Bot   | Planning | Replans | Models fire? |
|-------|----------|---------|--------------|
| Bot 1 | Shortest path computed once at `t = 0`, executed open-loop | No | No |
| Bot 2 | Shortest path recomputed every tick against the current grid | Yes | No |
| Bot 3 | Replans every tick, treating cells adjacent to fire as blocked | Yes | One-step lookahead |
| Bot 4 | Replans every tick using a probabilistic cost field that weights cells by expected fire arrival time | Yes | Multi-step probabilistic |

Pathfinding uses **BFS** for the unweighted variants and **A\*** with the Manhattan heuristic for the weighted/cost-field variants. Bot 4's cost field is rebuilt each tick from the current fire frontier, so the planner reacts to how the hazard is actually moving rather than where it currently is.

---

## Repository Layout

```
.
├── main.py                # Entry point — runs experiments / single simulations
├── bots/                  # Bot 1–4 implementations and shared planner utilities
├── environment/           # Grid construction, cell types, neighborhood logic
├── fireSpread/            # Stochastic fire-propagation model
├── simulationManager/     # Tick loop, win/loss conditions, batch runner
├── utils/                 # Visualization, RNG seeding, metrics
└── requirements.txt
```

The simulation manager is decoupled from the bots and the fire model, so adding a new bot or a new spread model is a single-file change.

---

## Running

```bash
pip install -r requirements.txt
python main.py
```

`main.py` exposes flags / config for grid size, obstacle density, number of trials, spread rate `q`, and which bot to run. Edit the constants at the top of the file (or the config block) to sweep parameters.

---

## Benchmarks

Each bot is evaluated over many randomized maps and ignition points, sweeping the fire spread rate `q` from 0 to 1. The headline metric is **success rate vs. q**.

Typical findings:

- **Bot 1** (open-loop) collapses quickly as `q` grows — it commits to a path that the fire then cuts.
- **Bot 2** (replan, ignore fire dynamics) holds up at low `q` but is fragile near the fire frontier because it walks into cells that *will* be on fire next tick.
- **Bot 3** (avoid fire-adjacent cells) is meaningfully more robust but is over-cautious in sparse fires, sometimes refusing safe shortcuts.
- **Bot 4** (probabilistic cost field) dominates at moderate to high `q`, trading slightly longer paths for substantially higher survival rates.

Exact numbers depend on grid size and trial count; the simulation manager prints per-bot success rates and average path lengths at the end of each batch.

---

## What This Project Demonstrates

- Pathfinding (BFS, A\*) on dynamic, partially-predictable cost fields
- Discrete-event simulation with a clean separation between environment, hazard, and agent
- Reproducible benchmarking — fixed seeds, batched trials, per-strategy metrics
- Modular design that makes it easy to plug in a new planner or a new propagation model

---

## License

MIT.
