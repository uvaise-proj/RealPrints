const STEPS = ['project', 'stage', 'form']

export default function StepIndicator({ step }) {
  const current = STEPS.indexOf(step)
  return (
    <div className="step-indicator" aria-label={`Step ${current + 1} of ${STEPS.length}`}>
      {STEPS.map((s, i) => (
        <span
          key={s}
          className={[
            'step-dot',
            i < current  ? 'step-dot--done'   : '',
            i === current ? 'step-dot--active' : '',
          ].join(' ')}
        />
      ))}
    </div>
  )
}
