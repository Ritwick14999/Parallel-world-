from __future__ import annotations

import random
from dataclasses import dataclass

from app.models import PathAggregate, PathName, SimulationRequest, SimulationResponse, SimulationSummary, UniverseOutcome


@dataclass(slots=True)
class AgentState:
    age: int
    path: PathName
    risk_tolerance: float
    adaptability: float
    social_capital: float
    consistency: float
    wealth: float
    happiness: float
    regret: float
    career: float


PATH_BIASES: dict[PathName, dict[str, float]] = {
    "startup_founder": {"wealth": 1.35, "career": 0.95, "happiness": 0.05, "regret": 0.2},
    "ms_then_industry": {"wealth": 1.0, "career": 1.05, "happiness": 0.25, "regret": -0.05},
    "faang_engineer": {"wealth": 1.2, "career": 1.1, "happiness": 0.12, "regret": -0.05},
    "research_scientist": {"wealth": 0.85, "career": 1.25, "happiness": 0.3, "regret": -0.15},
    "indie_hacker": {"wealth": 1.1, "career": 0.92, "happiness": 0.22, "regret": 0.08},
    "crypto_trader": {"wealth": 1.3, "career": 0.6, "happiness": -0.2, "regret": 0.3},
}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _score_outcome(outcome: UniverseOutcome) -> float:
    return (
        0.35 * outcome.happiness_score
        + 0.25 * outcome.career_score
        + 0.2 * (10 - outcome.regret_score)
        + 0.2 * min(10, outcome.net_worth_usd / 220_000)
    )


def _simulate_year(state: AgentState, rng: random.Random, year_index: int) -> tuple[AgentState, str | None]:
    event_roll = rng.random()
    event: str | None = None

    if event_roll < 0.05:
        state.wealth *= 0.8
        state.happiness -= 0.45
        state.regret += 0.55
        event = f"Year {year_index}: faced a personal or financial setback"
    elif event_roll < 0.1:
        state.wealth *= 1.2
        state.career += 0.35
        state.happiness += 0.25
        event = f"Year {year_index}: got an unexpected career opportunity"
    elif event_roll < 0.15:
        state.happiness += 0.4
        state.regret -= 0.25
        event = f"Year {year_index}: improved routines and work-life balance"

    growth_noise = rng.uniform(-0.15, 0.2)
    wealth_growth = (
        0.03
        + 0.08 * state.risk_tolerance
        + 0.04 * state.adaptability
        + 0.03 * state.consistency
        + growth_noise
    ) * 100_000
    state.wealth += wealth_growth

    happiness_shift = (
        rng.uniform(-0.15, 0.16)
        + 0.07 * state.social_capital
        + 0.04 * state.adaptability
        + 0.04 * state.consistency
    )
    regret_shift = rng.uniform(-0.1, 0.14) - 0.06 * state.adaptability - 0.03 * state.consistency
    career_shift = rng.uniform(-0.08, 0.16) + 0.05 * state.social_capital + 0.04 * state.consistency

    state.happiness = _clamp(state.happiness + happiness_shift, 0, 10)
    state.regret = _clamp(state.regret + regret_shift, 0, 10)
    state.career = _clamp(state.career + career_shift, 0, 10)
    state.age += 1

    return state, event


def _init_agent(age: int, path: PathName, rng: random.Random) -> AgentState:
    bias = PATH_BIASES[path]
    return AgentState(
        age=age,
        path=path,
        risk_tolerance=_clamp(rng.gauss(0.55, 0.2), 0.05, 0.95),
        adaptability=_clamp(rng.gauss(0.58, 0.18), 0.1, 0.95),
        social_capital=_clamp(rng.gauss(0.5, 0.22), 0.05, 0.95),
        consistency=_clamp(rng.gauss(0.56, 0.17), 0.1, 0.95),
        wealth=max(0, rng.uniform(6_000, 32_000) * bias["wealth"]),
        happiness=_clamp(5.0 + bias["happiness"] + rng.uniform(-0.5, 0.5), 0, 10),
        regret=_clamp(3.8 + bias["regret"] + rng.uniform(-0.6, 0.6), 0, 10),
        career=_clamp(4.4 + bias["career"] + rng.uniform(-0.3, 0.4), 0, 10),
    )


def run_simulation(request: SimulationRequest) -> SimulationResponse:
    rng = random.Random(request.seed)
    outcomes: list[UniverseOutcome] = []
    decisions = request.profile.decisions_under_consideration

    for universe_id in range(1, request.universes + 1):
        path = rng.choice(decisions)
        agent = _init_agent(request.profile.age, path, rng)

        key_events: list[str] = []
        for year in range(1, request.years + 1):
            agent, maybe_event = _simulate_year(agent, rng, year)
            if maybe_event and len(key_events) < 4:
                key_events.append(maybe_event)

        if not key_events:
            key_events.append("Steady year-over-year progress with no major disruptions.")

        outcomes.append(
            UniverseOutcome(
                universe_id=universe_id,
                selected_path=path,
                final_age=agent.age,
                net_worth_usd=round(max(0, agent.wealth), 2),
                happiness_score=round(agent.happiness, 2),
                regret_score=round(agent.regret, 2),
                career_score=round(agent.career, 2),
                key_events=key_events,
            )
        )

    best_happiness = max(outcomes, key=lambda o: o.happiness_score)
    best_wealth = max(outcomes, key=lambda o: o.net_worth_usd)
    lowest_regret = min(outcomes, key=lambda o: o.regret_score)

    grouped: dict[PathName, list[UniverseOutcome]] = {path: [] for path in decisions}
    for outcome in outcomes:
        grouped[outcome.selected_path].append(outcome)

    path_breakdown: list[PathAggregate] = []
    path_scores: dict[PathName, float] = {}

    for path, items in grouped.items():
        if not items:
            continue
        avg_wealth = sum(i.net_worth_usd for i in items) / len(items)
        avg_happiness = sum(i.happiness_score for i in items) / len(items)
        avg_regret = sum(i.regret_score for i in items) / len(items)
        avg_career = sum(i.career_score for i in items) / len(items)
        avg_score = sum(_score_outcome(i) for i in items) / len(items)

        path_scores[path] = avg_score
        path_breakdown.append(
            PathAggregate(
                path=path,
                samples=len(items),
                avg_net_worth_usd=round(avg_wealth, 2),
                avg_happiness_score=round(avg_happiness, 2),
                avg_regret_score=round(avg_regret, 2),
                avg_career_score=round(avg_career, 2),
                overall_score=round(avg_score, 2),
            )
        )

    path_breakdown.sort(key=lambda x: x.overall_score, reverse=True)
    ranked_paths = sorted(path_scores.items(), key=lambda item: item[1], reverse=True)
    recommended_path = ranked_paths[0][0]

    top_score = ranked_paths[0][1]
    second_score = ranked_paths[1][1] if len(ranked_paths) > 1 else ranked_paths[0][1]
    confidence = _clamp((top_score - second_score) / 2.5, 0, 1)

    summary = SimulationSummary(
        best_happiness_universe_id=best_happiness.universe_id,
        best_wealth_universe_id=best_wealth.universe_id,
        lowest_regret_universe_id=lowest_regret.universe_id,
        recommended_path=recommended_path,
        recommendation_confidence=round(confidence, 2),
        path_breakdown=path_breakdown,
    )

    return SimulationResponse(
        profile=request.profile,
        universes_simulated=request.universes,
        years_simulated=request.years,
        outcomes=outcomes,
        summary=summary,
    )
