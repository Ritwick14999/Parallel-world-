'use client';

import { useState } from 'react';
import ResultsDashboard from '@/components/ResultsDashboard';
import SimulationForm from '@/components/SimulationForm';
import type { SimulationResponse } from '@/lib/types';

export default function HomePage() {
  const [result, setResult] = useState<SimulationResponse | null>(null);

  return (
    <main className="container">
      <section className="hero card">
        <h1>Parallel Universe Simulator</h1>
        <p>
          A practical decision companion to compare major life choices—startup, higher studies,
          research, or industry—and see how each path may feel over time.
        </p>
      </section>
      <SimulationForm onResult={setResult} />
      {result && <ResultsDashboard result={result} />}
    </main>
  );
}
