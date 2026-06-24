/**
 * Single metric tile used in the Summary grid.
 * accent — optional CSS colour value applied as a left border stripe.
 */
export default function StatCard({ value, label, accent }) {
  return (
    <div
      className="stat-card"
      style={accent ? { borderLeftColor: accent, borderLeftWidth: 4 } : undefined}
    >
      <div className="stat-card__value">{value ?? '—'}</div>
      <div className="stat-card__label">{label}</div>
    </div>
  )
}
