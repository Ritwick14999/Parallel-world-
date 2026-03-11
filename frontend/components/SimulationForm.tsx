'use client';

import { useState } from 'react';
import type { PathName, SimulationRequest, SimulationResponse } from '@/lib/types';

const PATH_OPTIONS: PathName[] = [
  'startup_founder',
  'ms_then_industry',
  'faang_engineer',
  'research_scientist',
  'indie_hacker',
  'crypto_trader'
];

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

const toLabel = (path: PathName) =>
  path
    .split('_')
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join(' ');

interface Props {
  onResult: (data: SimulationResponse) => void;
}

export default function SimulationForm({ onResult }: Props) {
  const [loading, setLoading] = useState(false);
  const [loadingPreset, setLoadingPreset] = useState(false);
  const [error, setError] = useState('');

  async function runPayload(payload: SimulationRequest) {
    const response = await fetch(`${API_BASE}/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error('Could not run simulation right now.');
    }

    const data = (await response.json()) as SimulationResponse;
    onResult(data);
  }

  async function handleLoadSample() {
    setLoadingPreset(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE}/sample-profiles?limit=1`);
      if (!response.ok) {
        throw new Error('Could not load sample profile.');
      }
      const data = (await response.json()) as { samples: SimulationRequest[] };
      if (!data.samples?.length) {
        throw new Error('No sample profiles available.');
      }
      await runPayload(data.samples[0]);
    } catch {
      setError('Could not load sample profile. Make sure backend is running on localhost:8000.');
    } finally {
      setLoadingPreset(false);
    }
  }

  async function handleSubmit(formData: FormData) {
    setLoading(true);
    setError('');

    const selectedPaths = PATH_OPTIONS.filter((path) => formData.get(path) === 'on');
    const seedValue = String(formData.get('seed') ?? '').trim();

    const payload: SimulationRequest = {
      profile: {
        age: Number(formData.get('age') ?? 20),
        location: String(formData.get('location') ?? 'India'),
        skills: String(formData.get('skills') ?? '').split(',').map((s) => s.trim()).filter(Boolean),
        goals: String(formData.get('goals') ?? '').split(',').map((s) => s.trim()).filter(Boolean),
        decisions_under_consideration: selectedPaths.length > 0 ? selectedPaths : ['faang_engineer', 'startup_founder']
      },
      universes: Number(formData.get('universes') ?? 500),
      years: Number(formData.get('years') ?? 15),
      ...(seedValue ? { seed: Number(seedValue) } : {})
    };

    try {
      await runPayload(payload);
    } catch {
      setError('Could not reach the backend. Make sure API is running on localhost:8000.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form action={handleSubmit} className="card stack">
      <h2>Tell us about your current situation</h2>
      <p className="muted">Tip: You can run a ready-made demo profile if you want to test quickly.</p>
      <label>Age<input name="age" type="number" min={15} max={80} defaultValue={20} /></label>
      <label>Current location<input name="location" defaultValue="India" /></label>
      <label>Skills (comma separated)<input name="skills" defaultValue="python, ai, system design" /></label>
      <label>Goals (comma separated)<input name="goals" defaultValue="impact, wealth, freedom" /></label>
      <label>How many simulated futures?<input name="universes" type="number" min={50} max={5000} defaultValue={600} /></label>
      <label>Years to project<input name="years" type="number" min={5} max={25} defaultValue={15} /></label>
      <label>Random seed (optional)<input name="seed" type="number" placeholder="leave empty for random run" /></label>

      <fieldset>
        <legend>Paths you are seriously considering</legend>
        {PATH_OPTIONS.map((path) => (
          <label key={path} className="inline">
            <input type="checkbox" name={path} defaultChecked={path !== 'crypto_trader'} />
            {toLabel(path)}
          </label>
        ))}
      </fieldset>

      {error && <p className="error">{error}</p>}

      <div className="actions">
        <button type="submit" disabled={loading || loadingPreset}>{loading ? 'Running scenarios…' : 'Compare my life paths'}</button>
        <button type="button" className="secondary" onClick={handleLoadSample} disabled={loading || loadingPreset}>
          {loadingPreset ? 'Loading demo…' : 'Run demo profile'}
        </button>
      </div>
    </form>
  );
}
