import { useState, useEffect } from 'react'
import { fetchProjects } from '../api/client.js'

export default function ProjectSelect({ onSelect }) {
  const [projects, setProjects] = useState([])
  const [search, setSearch]     = useState('')
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)

  useEffect(() => {
    fetchProjects()
      .then((data) => setProjects(data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const filtered = projects.filter((p) => {
    const q = search.toLowerCase()
    return (
      p.project_id.toLowerCase().includes(q) ||
      p.client_name.toLowerCase().includes(q)
    )
  })

  return (
    <div className="screen">
      <div className="search-wrapper">
        <span className="search-icon" aria-hidden>🔍</span>
        <input
          type="search"
          className="search-input"
          placeholder="Search by ID or client name…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          autoFocus
        />
      </div>

      {loading && (
        <div className="project-list">
          {[1, 2, 3, 4].map((n) => (
            <div key={n} className="skeleton skeleton--card" />
          ))}
        </div>
      )}

      {error && (
        <div className="status-banner status-banner--error">
          <span className="status-banner__icon">⚠️</span>
          <span className="status-banner__msg">Could not load projects: {error}</span>
        </div>
      )}

      {!loading && !error && (
        <div className="project-list">
          {filtered.length === 0 ? (
            <div className="empty-state">
              {search ? `No results for "${search}"` : 'No projects found.'}
            </div>
          ) : (
            filtered.map((p) => (
              <button
                key={p.project_id}
                className="project-card"
                onClick={() => onSelect(p)}
              >
                <div className="project-card__info">
                  <span className="project-card__id">{p.project_id}</span>
                  <span className="project-card__client">{p.client_name}</span>
                  {p.date && (
                    <span className="project-card__meta">{p.date}</span>
                  )}
                </div>
                <span className="project-card__arrow" aria-hidden>›</span>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  )
}
