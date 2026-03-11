# Architecture Overview

## Product Lens

This project is a **decision support tool**, not a certainty machine.
It helps users compare plausible futures and make informed choices.

## Components

1. **Input Intake (Frontend + API contract)**
   - Captures age, skills, goals, and candidate paths.
2. **Profile Sampler**
   - Uses user inputs + stochastic traits (risk appetite, adaptability, consistency).
3. **Simulation Engine**
   - Runs year-by-year transitions with opportunities, setbacks, and routine improvements.
4. **Outcome Scorer**
   - Balances happiness, career momentum, regret, and wealth.
5. **Path Analytics Layer**
   - Aggregates path-level averages and computes recommendation confidence.
6. **Dashboard Renderer**
   - Shows top scenarios plus a path comparison table.

## Backend

- `app/models.py`: dataclasses + input normalization.
- `app/simulation/engine.py`: deterministic simulation, scoring, path analytics.
- `app/main.py`: `/health`, `/simulate`, `/sample-profiles`.
- `data/sample_profiles.json`: 200 demo-ready request samples.

## Frontend

- `app/page.tsx`: top-level page composition.
- `components/SimulationForm.tsx`: input, API calls, demo profile quick run.
- `components/ResultsDashboard.tsx`: ranked scenarios + path-level comparison table.

## Runbook

- Docker path for fastest setup: `docker compose up --build`.
- Manual local path available for backend/frontend independently.
