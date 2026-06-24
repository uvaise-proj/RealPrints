const LABELS = {
  fusing_temp:    'Fusing Temp',
  printing_temp:  'Printing Temp',
  paint_name:     'Paint Name',
  frame_size:     'Frame Size',
  mesh_count:     'Mesh Count',
  quality:        'Quality',
  print_material: 'Print Material',
  paper_size:     'Paper Size',
  ink_type:       'Ink Type',
  ink_color:      'Ink Color',
  paper_quantity: 'Paper Quantity',
  gel_or_powder:  'Gel / Powder',
  no_of_pieces:   'No. of Pieces',
  no_of_ups:      'No. of Ups',
}

const UNITS = {
  fusing_temp:   '°C',
  printing_temp: '°C',
}

/**
 * Renders a best_config dict as a striped key → value table.
 * Returns null when config is empty so callers don't need to guard.
 */
export default function ConfigTable({ config }) {
  const entries = Object.entries(config)
  if (entries.length === 0) return null

  return (
    <div className="config-table">
      {entries.map(([key, val]) => (
        <div key={key} className="config-table__row">
          <span className="config-table__key">{LABELS[key] ?? key}</span>
          <span className="config-table__val">
            {typeof val === 'number' ? val.toLocaleString() : val}
            {UNITS[key] ? <span className="config-table__unit"> {UNITS[key]}</span> : null}
          </span>
        </div>
      ))}
    </div>
  )
}
