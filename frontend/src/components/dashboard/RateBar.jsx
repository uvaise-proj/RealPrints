/**
 * Horizontal progress bar for any 0–1 rate metric.
 * color  — CSS colour value for the fill and percentage text.
 * extra  — optional sub-label text shown below the bar label.
 */
export default function RateBar({ label, icon, rate, color = 'var(--success)', extra }) {
  const pct = Math.min(100, Math.max(0, Math.round(rate * 100)))

  return (
    <div className="rate-bar-wrap">
      <div className="rate-bar__header">
        <span className="rate-bar__label">
          {icon && <span aria-hidden>{icon}</span>}
          {label}
          {extra && <span className="rate-bar__extra">{extra}</span>}
        </span>
        <span className="rate-bar__pct" style={{ color }}>{pct}%</span>
      </div>
      <div className="rate-bar__track">
        <div
          className="rate-bar__fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
    </div>
  )
}
