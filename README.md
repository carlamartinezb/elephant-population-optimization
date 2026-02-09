# Elephant Population Optimization (Stochastic Simulation)

This project extends an elephant population model to automatically find the **darting probability** (contraception rate) that keeps the herd near carrying capacity **K** over a 200-year horizon, then studies how that “optimal” value shifts when biological parameters change.

## What this project does
- Runs a month-by-month **stochastic population simulation**
- Wraps the simulation to average multiple runs for stability
- Uses a **binary-search optimizer** to find the darting probability that makes average population ≈ K
- Performs one-at-a-time sensitivity simulations for:
  - adult survival
  - calf survival
  - calving interval
  - maximum age
  - senior survival
- Saves results as CSV and line plots (and includes a 2-parameter heatmap extension)

## Key findings
- Adult survival 0.98 → 1.00 increases optimal darting sharply (~0.31 → ~0.45)
- Calf survival 0.80 → 0.90 increases darting slightly (~0.413 → ~0.433)
- Calving interval 3.0 → 3.4 years decreases darting (~0.433 → ~0.399)
- Max age 56 → 66 increases darting (~0.408 → ~0.440)
- Senior survival 0.10 → 0.50 has a small effect (~0.421 → ~0.427)

## Repo structure
- `src/` – simulation + optimization scripts
- `data/` – CSV outputs from parameter sweeps
- `figures/` – generated plots
- `report/` – written report

## How to run
Run the parameter sweep script (generates CSV and PNG outputs):
```bash
python src/extension_p6.py
