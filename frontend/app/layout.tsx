import './styles.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Parallel Universe Simulator',
  description: 'Simulate 1000+ alternate life paths with AI-inspired agents.'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
