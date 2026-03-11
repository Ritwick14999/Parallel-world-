# Parallel Universe Simulator

Parallel Universe Simulator is a full-stack project for **human decision support**.

It helps you compare big life choices (startup, MS, research, job paths) by simulating many plausible futures and showing practical trade-offs.

## What is included

- FastAPI backend with:
  - `POST /simulate` for running simulations
  - `GET /sample-profiles` for ready-to-run demo inputs
  - `GET /health` for health checks
- Next.js frontend with a human-friendly form and results dashboard
- Path-level comparison table (averages + overall score + confidence)
- 200 ready sample requests in `backend/data/sample_profiles.json`
- Backend tests for determinism and response shape
- Docker Compose for one-command local startup

## Copy-paste quick start (recommended)

```bash
git clone <your-repo-url>
cd Parallel-world-
docker compose up --build
```

Then open:
- Frontend: `http://localhost:3000`
- Backend docs: `http://localhost:8000/docs`

## Manual local run

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 npm run dev
```

## Example API call

```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "age": 20,
      "location": "India",
      "skills": ["python", "ml"],
      "goals": ["impact", "wealth"],
      "decisions_under_consideration": ["startup_founder", "faang_engineer", "ms_then_industry"]
    },
    "universes": 500,
    "years": 15,
    "seed": 42
  }'
```

## Why this feels human

- Event text is grounded in real life (setbacks, opportunities, routine improvements).
- Output emphasizes life quality (happiness, regret, career momentum), not just money.
- Recommendation now includes confidence and path-by-path summary so users can inspect the trade-offs.

## Resume talking points

- Built a Monte Carlo-style career/life simulator with deterministic seeding.
- Implemented an interpretable simulation engine and weighted outcome scorer.
- Added path-level analytics and confidence to make recommendations auditable.
- Added a production-like API and full-stack dashboard.
- Shipped with 200 sample payloads for demos and testing.
