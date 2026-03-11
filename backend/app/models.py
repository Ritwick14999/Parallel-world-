from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal, cast


PathName = Literal[
    "startup_founder",
    "ms_then_industry",
    "faang_engineer",
    "research_scientist",
    "indie_hacker",
    "crypto_trader",
]

ALLOWED_PATHS: tuple[PathName, ...] = (
    "startup_founder",
    "ms_then_industry",
    "faang_engineer",
    "research_scientist",
    "indie_hacker",
    "crypto_trader",
)


@dataclass(slots=True)
class UserProfile:
    age: int
    location: str
    skills: list[str] = field(default_factory=list)
    goals: list[str] = field(default_factory=list)
    decisions_under_consideration: list[PathName] = field(default_factory=list)


@dataclass(slots=True)
class SimulationRequest:
    profile: UserProfile
    universes: int = 1000
    years: int = 15
    seed: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "SimulationRequest":
        profile_raw = data.get("profile", {})

        decisions_raw = [str(path) for path in profile_raw.get("decisions_under_consideration", [])]
        clean_decisions = [cast(PathName, path) for path in decisions_raw if path in ALLOWED_PATHS]

        if not clean_decisions:
            clean_decisions = ["faang_engineer", "ms_then_industry"]

        profile = UserProfile(
            age=max(15, min(80, int(profile_raw.get("age", 20)))),
            location=str(profile_raw.get("location", "Unknown")),
            skills=[str(skill) for skill in profile_raw.get("skills", [])][:20],
            goals=[str(goal) for goal in profile_raw.get("goals", [])][:20],
            decisions_under_consideration=clean_decisions,
        )

        seed_raw = data.get("seed")
        seed = int(seed_raw) if seed_raw not in (None, "") else None

        return cls(
            profile=profile,
            universes=max(50, min(5000, int(data.get("universes", 1000)))),
            years=max(5, min(25, int(data.get("years", 15)))),
            seed=seed,
        )


@dataclass(slots=True)
class UniverseOutcome:
    universe_id: int
    selected_path: PathName
    final_age: int
    net_worth_usd: float
    happiness_score: float
    regret_score: float
    career_score: float
    key_events: list[str]


@dataclass(slots=True)
class PathAggregate:
    path: PathName
    samples: int
    avg_net_worth_usd: float
    avg_happiness_score: float
    avg_regret_score: float
    avg_career_score: float
    overall_score: float


@dataclass(slots=True)
class SimulationSummary:
    best_happiness_universe_id: int
    best_wealth_universe_id: int
    lowest_regret_universe_id: int
    recommended_path: PathName
    recommendation_confidence: float
    path_breakdown: list[PathAggregate]


@dataclass(slots=True)
class SimulationResponse:
    profile: UserProfile
    universes_simulated: int
    years_simulated: int
    outcomes: list[UniverseOutcome]
    summary: SimulationSummary

    def to_dict(self) -> dict:
        return asdict(self)
