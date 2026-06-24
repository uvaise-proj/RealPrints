import { useState, useEffect } from 'react'
import { fetchSummary } from '../../api/analytics.js'
import StatCard from './StatCard.jsx'
import RateBar  from './RateBar.jsx'

const STAGE_META = {
  fusing:   { icon: '🔥', color: '#ea580c' },
  exposing: { icon: '☀️', color: '#7c3aed' },
  printing: { icon: '🖨️', color: '#2563eb' },
  cutting:  { icon: '✂️', color: '#059669' },
}

export default function SummarySection() {
  const [data,    setData]    = useState(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)

  useEffect(() => {
    fetchSummary()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <section className="db-section" aria-labelledby="summary-title">
      <div className="db-section__header">
        <span className="db-section__icon" aria-hidden>📊</span>
        <h2 className="db-section__title" id="summary-title">Summary</h2>
      </div>

      {loading && (
        <div className="stat-grid">
          {[1, 2, 3, 4].map((n) => (
            <div key={n} className="skeleton" style={{ height: 82 }} />
          ))}
        </div>
      )}

      {error && (
        <div className="status-banner status-banner--error" role="alert">
          <span className="status-banner__icon" aria-hidden>⚠️</span>
          <span className="status-banner__msg">Could not load summary: {error}</span>
        </div>
      )}

      {data && (
        <>
          <div className="stat-grid">
            <StatCard value={data.total_projects}     label="Projects"    />
            <StatCard value={data.total_process_logs} label="Total Runs"  />
            <StatCard value={data.successful_runs}    label="Successful"  accent="var(--success)" />
            <StatCard value={data.failed_runs}        label="Failed"      accent="var(--error)"   />
          </div>

          <RateBar
            label="Overall Success"
            rate={data.overall_success_rate}
            color="var(--success)"
          />

          {data.stage_distribution.length > 0 && (
            <div className="db-stage-bars">
              {data.stage_distribution.map((s) => {
                const meta  = STAGE_META[s.process_type] ?? {}
                const label = s.process_type.charAt(0).toUpperCase() + s.process_type.slice(1)
                return (
                  <RateBar
                    key={s.process_type}
                    label={label}
                    icon={meta.icon}
                    rate={s.success_rate}
                    color={meta.color}
                    extra={`${s.success_count}/${s.total}`}
                  />
                )
              })}
            </div>
          )}
        </>
      )}
    </section>
  )
}
