import { useState, useEffect } from 'react'
import { fetchFailureRate } from '../../api/analytics.js'
import StageFilterBar from './StageFilterBar.jsx'

export default function FailureInsights() {
  const [filters, setFilters] = useState({ processType: '', garmentMaterial: '' })
  const [data,    setData]    = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  useEffect(() => {
    if (!filters.processType) { setData(null); return }

    setLoading(true)
    setError(null)

    fetchFailureRate({
      process_type:      filters.processType,
      garment_material:  filters.garmentMaterial || undefined,
    })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [filters.processType, filters.garmentMaterial])

  const handleChange = (key, val) => setFilters((prev) => ({ ...prev, [key]: val }))

  const failPct    = data ? Math.round(data.failure_rate * 100) : 0
  const isHighFail = failPct > 20

  return (
    <section className="db-section" aria-labelledby="failure-title">
      <div className="db-section__header">
        <span className="db-section__icon" aria-hidden>⚠️</span>
        <h2 className="db-section__title" id="failure-title">Failure Insights</h2>
      </div>

      <StageFilterBar
        processType={filters.processType}
        garmentMaterial={filters.garmentMaterial}
        onChange={handleChange}
      />

      {!filters.processType && (
        <div className="db-prompt">Select a stage to view failure rate.</div>
      )}

      {loading && <div className="skeleton" style={{ height: 110 }} />}

      {error && !loading && (
        <div className="status-banner status-banner--error" role="alert">
          <span className="status-banner__icon" aria-hidden>⚠️</span>
          <span className="status-banner__msg">{error}</span>
        </div>
      )}

      {data && !loading && (
        <>
          <div className="insight-stats">
            <div className="insight-stat">
              <span className="insight-stat__value">{data.total_runs}</span>
              <span className="insight-stat__label">Total</span>
            </div>
            <div className="insight-stat insight-stat--success">
              <span className="insight-stat__value">{data.success_runs}</span>
              <span className="insight-stat__label">Success</span>
            </div>
            <div className={`insight-stat${isHighFail ? ' insight-stat--danger' : ''}`}>
              <span className="insight-stat__value">{data.failed_runs}</span>
              <span className="insight-stat__label">Failed</span>
            </div>
          </div>

          <div className="rate-bar-wrap">
            <div className="rate-bar__header">
              <span className="rate-bar__label">Failure Rate</span>
              <span
                className="rate-bar__pct"
                style={{ color: isHighFail ? 'var(--error)' : 'var(--success)' }}
              >
                {failPct}%
              </span>
            </div>
            <div className="rate-bar__track">
              <div
                className="rate-bar__fill"
                style={{
                  width:      `${failPct}%`,
                  background: isHighFail ? 'var(--error)' : 'var(--success)',
                }}
              />
            </div>
            {isHighFail && (
              <p className="rate-bar__warning">High failure rate — review stage parameters.</p>
            )}
          </div>
        </>
      )}
    </section>
  )
}
