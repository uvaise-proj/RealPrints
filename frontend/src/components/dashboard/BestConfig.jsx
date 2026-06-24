import { useState, useEffect } from 'react'
import { fetchBestConfig } from '../../api/analytics.js'
import StageFilterBar from './StageFilterBar.jsx'
import ConfigTable    from './ConfigTable.jsx'

export default function BestConfig() {
  const [filters, setFilters] = useState({ processType: '', garmentMaterial: '' })
  const [data,    setData]    = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  useEffect(() => {
    if (!filters.processType) { setData(null); return }

    setLoading(true)
    setError(null)

    fetchBestConfig({
      process_type:     filters.processType,
      garment_material: filters.garmentMaterial || undefined,
    })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [filters.processType, filters.garmentMaterial])

  const handleChange = (key, val) => setFilters((prev) => ({ ...prev, [key]: val }))

  return (
    <section className="db-section" aria-labelledby="bestconfig-title">
      <div className="db-section__header">
        <span className="db-section__icon" aria-hidden>⭐</span>
        <h2 className="db-section__title" id="bestconfig-title">Best Config</h2>
      </div>

      <StageFilterBar
        processType={filters.processType}
        garmentMaterial={filters.garmentMaterial}
        onChange={handleChange}
      />

      {!filters.processType && (
        <div className="db-prompt">Select a stage to view the recommended configuration.</div>
      )}

      {loading && <div className="skeleton" style={{ height: 140 }} />}

      {error && !loading && (
        <div className="status-banner status-banner--error" role="alert">
          <span className="status-banner__icon" aria-hidden>⚠️</span>
          <span className="status-banner__msg">{error}</span>
        </div>
      )}

      {data && !loading && (
        data.sample_count === 0 ? (
          <div className="db-prompt">{data.message}</div>
        ) : (
          <>
            <div className="config-meta">
              <span className="config-meta__chip">
                <strong>{data.sample_count}</strong> samples
              </span>
              {data.average_quality != null && (
                <span className="config-meta__chip">
                  Avg quality <strong>{data.average_quality} / 5</strong>
                </span>
              )}
            </div>
            <ConfigTable config={data.best_config} />
          </>
        )
      )}
    </section>
  )
}
