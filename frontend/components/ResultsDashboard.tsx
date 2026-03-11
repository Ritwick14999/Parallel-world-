import type { PathAggregate, PathName, SimulationResponse } from '@/lib/types';

interface Props {
  result: SimulationResponse;
}

const toLabel = (path: PathName) =>
  path
    .split('_')
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join(' ');

const confidenceLabel = (confidence: number): string => {
  if (confidence >= 0.6) {
    return 'High confidence';
  }
  if (confidence >= 0.3) {
    return 'Moderate confidence';
  }
  return 'Low confidence';
};

function PathRow({ aggregate }: { aggregate: PathAggregate }) {
  return (
    <tr>
      <td>{toLabel(aggregate.path)}</td>
      <td>{aggregate.samples}</td>
      <td>{aggregate.avg_happiness_score.toFixed(2)}</td>
      <td>{aggregate.avg_career_score.toFixed(2)}</td>
      <td>{aggregate.avg_regret_score.toFixed(2)}</td>
      <td>${aggregate.avg_net_worth_usd.toLocaleString()}</td>
      <td>{aggregate.overall_score.toFixed(2)}</td>
    </tr>
  );
}

export default function ResultsDashboard({ result }: Props) {
  const topBalanced = [...result.outcomes]
    .sort(
      (a, b) =>
        b.happiness_score + b.career_score - b.regret_score - (a.happiness_score + a.career_score - a.regret_score)
    )
    .slice(0, 5);

  return (
    <section className="card stack">
      <h2>Your most promising scenarios</h2>
      <p>
        Recommended direction right now: <strong>{toLabel(result.summary.recommended_path)}</strong>
      </p>
      <p className="muted">
        Confidence: <strong>{confidenceLabel(result.summary.recommendation_confidence)}</strong> ({result.summary.recommendation_confidence})
      </p>

      <div className="tableWrap">
        <table>
          <thead>
            <tr>
              <th>Path</th>
              <th>Samples</th>
              <th>Avg Happiness</th>
              <th>Avg Career</th>
              <th>Avg Regret</th>
              <th>Avg Net Worth</th>
              <th>Overall</th>
            </tr>
          </thead>
          <tbody>
            {result.summary.path_breakdown.map((aggregate) => (
              <PathRow key={aggregate.path} aggregate={aggregate} />
            ))}
          </tbody>
        </table>
      </div>

      <div className="grid">
        {topBalanced.map((outcome) => (
          <article key={outcome.universe_id} className="tile">
            <h3>Scenario {outcome.universe_id}</h3>
            <p>Path: {toLabel(outcome.selected_path)}</p>
            <p>Projected net worth: ${outcome.net_worth_usd.toLocaleString()}</p>
            <p>Happiness: {outcome.happiness_score} / 10</p>
            <p>Regret: {outcome.regret_score} / 10</p>
            <p>Career momentum: {outcome.career_score} / 10</p>
            <ul>
              {outcome.key_events.slice(0, 2).map((event) => (
                <li key={event}>{event}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}
