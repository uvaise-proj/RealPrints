import { STAGE_FIELDS } from '../config/stageFields.js'

export default function StageSelect({ project, onSelect }) {
  return (
    <div className="screen">
      <div className="context-banner">
        <span className="context-banner__label">Project</span>
        <span className="context-banner__value">
          {project.project_id} — {project.client_name}
        </span>
      </div>

      <p className="screen__hint">Select the production stage to log:</p>

      <div className="stage-grid">
        {Object.entries(STAGE_FIELDS).map(([key, stage]) => (
          <button
            key={key}
            className="stage-card"
            style={{ '--stage-color': stage.color }}
            onClick={() => onSelect(key)}
          >
            <span className="stage-card__icon" aria-hidden>{stage.icon}</span>
            <span className="stage-card__label">{stage.label}</span>
            <span className="stage-card__desc">{stage.description}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
