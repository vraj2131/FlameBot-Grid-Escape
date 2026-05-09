# FlameBot: Grid Escape Under Dynamic Constraints

A grid-based simulation framework that studies autonomous agent (bot) navigation in environments where the cost field changes every tick. The bot must reach a goal cell while fire spreads stochastically across the grid, blocking cells over time. The project implements and benchmarks several pathfinding strategies — culminating in **D\* Lite** — under dynamic, partially-predictable obstacles.

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
2. The bot observes the grid and decides on its next move.
3. The bot moves one cell.

The bot wins if it reaches the goal. It loses if it steps onto fire, is surrounded by fire, or fire reaches the goal first.

---

## Bot Strategies

Four bots of increasing sophistication are implemented and compared:

| Bot   | Planner                                                          | Replans every tick? | Models fire ahead?       |
|-------|------------------------------------------------------------------|---------------------|--------------------------|
| Bot 1 | BFS once at `t = 0`, executed open-loop                          | No                  | No                       |
| Bot 2 | BFS recomputed every tick against the current grid               | Yes (from scratch)  | No                       |
| Bot 3 | BFS each tick, treating cells adjacent to fire as blocked        | Yes (from scratch)  | One-step lookahead       |
| Bot 4 | **D\* Lite** with a probabilistic cost field weighted by expected fire arrival time | Yes (incremental) | Multi-step probabilistic |

**Bot 4 is the strongest and the headline result of the project.** Instead of replanning shortest paths from scratch every tick — which is what Bots 2 and 3 do — Bot 4 uses **D\* Lite**, an incremental search algorithm that reuses prior search effort and repairs the path locally as edge costs change. This makes it both faster than the from-scratch replanners and more robust, because the probabilistic cost field lets it route *around* where the fire is expected to be rather than only where it currently is.

The earlier bots are kept in the codebase as baselines so D\* Lite can be evaluated against simpler planners on the same maps and seeds.

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

- **Bot 1** (open-loop BFS) collapses quickly as `q` grows — it commits to a path that the fire then cuts.
- **Bot 2** (replan, ignore fire dynamics) holds up at low `q` but is fragile near the fire frontier because it walks into cells that *will* be on fire next tick.
- **Bot 3** (avoid fire-adjacent cells) is meaningfully more robust but is over-cautious in sparse fires, sometimes refusing safe shortcuts.
- **Bot 4** (D\* Lite + probabilistic cost field) **dominates at moderate to high `q`**, achieving the highest escape success rate of all four strategies. It also avoids the redundant work that Bots 2 and 3 do by reusing the previous search rather than rebuilding it from scratch every tick.

Exact numbers depend on grid size and trial count; the simulation manager prints per-bot success rates and average path lengths at the end of each batch.

---

## Why D\* Lite

D\* Lite is the natural fit for this problem:

- The graph (the grid) is large and most edges don't change between ticks; replanning from scratch wastes the work the previous search already did.
- Edge costs change *locally* — only cells near the fire frontier — which is exactly the regime D\* Lite is designed for. It propagates updates outward from changed cells rather than re-expanding the whole frontier.
- It keeps an admissible heuristic (Manhattan distance to goal), so it inherits A\*'s focused search behavior while staying correct under cost-field updates.

The same algorithm family is used in real-world robotics for autonomous navigation in environments where the map is updated as the robot moves — which is the practical motivation for using it here.

---

## What This Project Demonstrates

- Pathfinding (BFS, A\*, D\* Lite) on dynamic, partially-predictable cost fields
- Incremental search and path repair, not just from-scratch replanning
- Discrete-event simulation with a clean separation between environment, hazard, and agent
- Reproducible benchmarking — fixed seeds, batched trials, per-strategy metrics
- Modular design that makes it easy to plug in a new planner or a new propagation model

---

## License

MIT.
