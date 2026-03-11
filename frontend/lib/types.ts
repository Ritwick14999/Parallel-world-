export type PathName =
  | 'startup_founder'
  | 'ms_then_industry'
  | 'faang_engineer'
  | 'research_scientist'
  | 'indie_hacker'
  | 'crypto_trader';

export interface SimulationRequest {
  profile: {
    age: number;
    location: string;
    skills: string[];
    goals: string[];
    decisions_under_consideration: PathName[];
  };
  universes: number;
  years: number;
  seed?: number;
}

export interface UniverseOutcome {
  universe_id: number;
  selected_path: PathName;
  final_age: number;
  net_worth_usd: number;
  happiness_score: number;
  regret_score: number;
  career_score: number;
  key_events: string[];
}

export interface PathAggregate {
  path: PathName;
  samples: number;
  avg_net_worth_usd: number;
  avg_happiness_score: number;
  avg_regret_score: number;
  avg_career_score: number;
  overall_score: number;
}

export interface SimulationResponse {
  profile: SimulationRequest['profile'];
  universes_simulated: number;
  years_simulated: number;
  outcomes: UniverseOutcome[];
  summary: {
    best_happiness_universe_id: number;
    best_wealth_universe_id: number;
    lowest_regret_universe_id: number;
    recommended_path: PathName;
    recommendation_confidence: number;
    path_breakdown: PathAggregate[];
  };
}
