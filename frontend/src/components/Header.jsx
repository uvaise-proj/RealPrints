import StepIndicator from './StepIndicator.jsx'

const TITLES = {
  project: 'Select Project',
  stage:   'Select Stage',
  form:    'Log Stage Data',
}

// title overrides the step-based title and hides step dots.
// onLogout renders a logout button on the right when title is provided.
export default function Header({ step, onBack, title, onLogout }) {
  const displayTitle = title ?? TITLES[step] ?? step

  return (
    <header className="header">
      <div className="header__inner">
        {onBack ? (
          <button className="header__back" onClick={onBack} aria-label="Go back">
            ←
          </button>
        ) : (
          <div className="header__spacer" />
        )}

        <div className="header__title">
          <span className="header__app">RealPrints</span>
          <span className="header__step">{displayTitle}</span>
        </div>

        {title ? (
          onLogout ? (
            <button className="header__logout" onClick={onLogout} aria-label="Sign out">
              ⎋
            </button>
          ) : (
            <div className="header__spacer" />
          )
        ) : (
          <StepIndicator step={step} />
        )}
      </div>
    </header>
  )
}
