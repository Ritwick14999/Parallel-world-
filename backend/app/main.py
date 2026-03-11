from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import SimulationRequest
from app.simulation.engine import run_simulation

app = FastAPI(
    title="Parallel Universe Simulator API",
    description="Plan major life decisions by simulating many plausible career paths.",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "sample_profiles.json"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/sample-profiles")
def sample_profiles(limit: int = 200) -> dict:
    with DATA_FILE.open() as file:
        items = json.load(file)
    safe_limit = max(1, min(limit, len(items)))
    return {"count": safe_limit, "samples": items[:safe_limit]}


@app.post("/simulate")
def simulate(payload: dict) -> dict:
    request = SimulationRequest.from_dict(payload)
    response = run_simulation(request)
    return response.to_dict()
