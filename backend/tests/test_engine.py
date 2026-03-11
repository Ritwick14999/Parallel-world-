import json
from pathlib import Path

from app.models import SimulationRequest, UserProfile
from app.simulation.engine import run_simulation


def test_simulation_deterministic_seed() -> None:
    request = SimulationRequest(
        profile=UserProfile(
            age=20,
            location="India",
            skills=["python", "ml"],
            goals=["impact", "wealth"],
            decisions_under_consideration=["startup_founder", "faang_engineer", "ms_then_industry"],
        ),
        universes=100,
        years=10,
        seed=42,
    )

    response_a = run_simulation(request)
    response_b = run_simulation(request)

    assert response_a.summary == response_b.summary
    assert response_a.outcomes[0] == response_b.outcomes[0]


def test_simulation_response_shape() -> None:
    request = SimulationRequest(
        profile=UserProfile(
            age=25,
            location="US",
            skills=["ai", "distributed systems"],
            goals=["leadership"],
            decisions_under_consideration=["research_scientist", "faang_engineer"],
        ),
        universes=80,
        years=12,
    )

    response = run_simulation(request)

    assert response.universes_simulated == 80
    assert response.years_simulated == 12
    assert len(response.outcomes) == 80
    assert response.summary.recommended_path in {"research_scientist", "faang_engineer"}
    assert 0 <= response.summary.recommendation_confidence <= 1
    assert len(response.summary.path_breakdown) >= 1


def test_request_parser_filters_invalid_paths() -> None:
    request = SimulationRequest.from_dict(
        {
            "profile": {
                "age": 22,
                "location": "India",
                "skills": ["python"],
                "goals": ["impact"],
                "decisions_under_consideration": ["invalid_path", "faang_engineer"],
            },
            "universes": 100,
            "years": 10,
        }
    )

    assert request.profile.decisions_under_consideration == ["faang_engineer"]


def test_sample_profiles_file_has_200_items() -> None:
    data_file = Path(__file__).resolve().parents[1] / "data" / "sample_profiles.json"
    with data_file.open() as file:
        items = json.load(file)

    assert len(items) == 200
