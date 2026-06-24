const PROCESS_TYPES = [
  { value: 'fusing',   label: '🔥 Fusing'   },
  { value: 'exposing', label: '☀️ Exposing' },
  { value: 'printing', label: '🖨️ Printing' },
  { value: 'cutting',  label: '✂️ Cutting'  },
]

const MATERIALS = [
  { value: 'cotton',    label: 'Cotton'    },
  { value: 'polyester', label: 'Polyester' },
  { value: 'blend',     label: 'Blend'     },
  { value: 'nylon',     label: 'Nylon'     },
]

/**
 * Reusable two-select filter bar.
 * onChange(key, value) — key is 'processType' or 'garmentMaterial'.
 */
export default function StageFilterBar({ processType, garmentMaterial, onChange }) {
  return (
    <div className="filter-bar">
      <select
        className="filter-bar__select"
        value={processType}
        onChange={(e) => onChange('processType', e.target.value)}
        aria-label="Process stage"
      >
        <option value="">Stage…</option>
        {PROCESS_TYPES.map((pt) => (
          <option key={pt.value} value={pt.value}>{pt.label}</option>
        ))}
      </select>

      <select
        className="filter-bar__select"
        value={garmentMaterial}
        onChange={(e) => onChange('garmentMaterial', e.target.value)}
        aria-label="Garment material"
      >
        <option value="">All Materials</option>
        {MATERIALS.map((m) => (
          <option key={m.value} value={m.value}>{m.label}</option>
        ))}
      </select>
    </div>
  )
}
