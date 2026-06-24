const TABS = [
  { id: 'operator',  icon: '🏭', label: 'Operator'  },
  { id: 'dashboard', icon: '📊', label: 'Dashboard' },
]

export default function BottomNav({ active, onChange }) {
  return (
    <nav className="bottom-nav" aria-label="Main navigation">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          className={`bottom-nav__tab${active === tab.id ? ' bottom-nav__tab--active' : ''}`}
          onClick={() => onChange(tab.id)}
          aria-current={active === tab.id ? 'page' : undefined}
        >
          <span className="bottom-nav__icon" aria-hidden>{tab.icon}</span>
          <span className="bottom-nav__label">{tab.label}</span>
        </button>
      ))}
    </nav>
  )
}
