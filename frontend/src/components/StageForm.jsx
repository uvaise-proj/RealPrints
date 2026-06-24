import { useState } from 'react'
import { STAGE_FIELDS } from '../config/stageFields.js'
import { submitProcess } from '../api/client.js'
import FormField from './FormField.jsx'

function buildInitialValues(fields) {
  return Object.fromEntries(fields.map((f) => [f.name, '']))
}

function buildPayloadData(fields, values) {
  const data = {}
  for (const field of fields) {
    data[field.name] =
      field.type === 'number' ? Number(values[field.name]) : values[field.name]
  }
  return data
}

function SuccessScreen({ project, stageConfig, onNewStage, onNewProject }) {
  return (
    <div className="success-screen">
      <span className="success-screen__icon" aria-hidden>✅</span>
      <h2 className="success-screen__title">Stage Logged!</h2>
      <p className="success-screen__subtitle">
        <strong>{stageConfig.label}</strong> data saved for project{' '}
        <strong>{project.project_id}</strong>.
      </p>
      <div className="success-screen__actions">
        <button className="btn btn--primary btn--full" onClick={onNewStage}>
          {stageConfig.icon} Log Another Stage
        </button>
        <button className="btn btn--ghost btn--full" onClick={onNewProject}>
          ↩ Switch Project
        </button>
      </div>
    </div>
  )
}

export default function StageForm({ project, stage, onNewStage, onNewProject }) {
  const stageConfig = STAGE_FIELDS[stage]

  const [values, setValues]           = useState(() => buildInitialValues(stageConfig.fields))
  const [submitState, setSubmitState] = useState('idle') // 'idle' | 'loading' | 'success' | 'error'
  const [errorMsg, setErrorMsg]       = useState('')

  const handleChange = (name, value) =>
    setValues((prev) => ({ ...prev, [name]: value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitState('loading')
    setErrorMsg('')

    try {
      await submitProcess({
        project_id:   project.project_id,
        process_type: stage,
        data:         buildPayloadData(stageConfig.fields, values),
      })
      setSubmitState('success')
    } catch (err) {
      setSubmitState('error')
      setErrorMsg(err.message)
    }
  }

  if (submitState === 'success') {
    return (
      <div className="screen">
        <SuccessScreen
          project={project}
          stageConfig={stageConfig}
          onNewStage={onNewStage}
          onNewProject={onNewProject}
        />
      </div>
    )
  }

  return (
    <div className="screen">
      <div className="context-banner">
        <span className="context-banner__label">Project</span>
        <span className="context-banner__value">
          {project.project_id} — {project.client_name}
        </span>
      </div>

      <div className="stage-badge" style={{ '--stage-color': stageConfig.color }}>
        <span aria-hidden>{stageConfig.icon}</span>
        {stageConfig.label} Stage
      </div>

      <form onSubmit={handleSubmit} className="stage-form">
        {stageConfig.fields.map((field) => (
          <FormField
            key={field.name}
            field={field}
            value={values[field.name]}
            onChange={handleChange}
          />
        ))}

        {submitState === 'error' && (
          <div className="status-banner status-banner--error" role="alert">
            <span className="status-banner__icon" aria-hidden>⚠️</span>
            <span className="status-banner__msg">
              {errorMsg || 'Submission failed. Please try again.'}
            </span>
          </div>
        )}

        <button
          type="submit"
          className="btn btn--primary btn--full"
          disabled={submitState === 'loading'}
        >
          {submitState === 'loading' ? '⏳ Submitting…' : '✓ Submit Stage Data'}
        </button>
      </form>
    </div>
  )
}
