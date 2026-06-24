/**
 * Single source of truth for every production stage.
 * Each field drives both the dynamic form renderer and the API payload builder.
 *
 * field.type: 'text' | 'number' | 'select'
 * field.inputMode: overrides the mobile keyboard (numeric = integers, decimal = floats)
 */
export const STAGE_FIELDS = {
  fusing: {
    label: 'Fusing',
    icon: '🔥',
    color: '#ea580c',
    description: 'Heat & adhesive settings',
    fields: [
      {
        name: 'fusing_temp',
        label: 'Fusing Temperature',
        type: 'number',
        unit: '°C',
        required: true,
        min: 0,
        step: 0.1,
        inputMode: 'decimal',
        placeholder: 'e.g. 160',
      },
      {
        name: 'printing_temp',
        label: 'Printing Temperature',
        type: 'number',
        unit: '°C',
        required: true,
        min: 0,
        step: 0.1,
        inputMode: 'decimal',
        placeholder: 'e.g. 180',
      },
      {
        name: 'paint_name',
        label: 'Paint Name',
        type: 'text',
        required: true,
        placeholder: 'e.g. Plastisol White',
      },
    ],
  },

  exposing: {
    label: 'Exposing',
    icon: '☀️',
    color: '#7c3aed',
    description: 'Screen & mesh configuration',
    fields: [
      {
        name: 'frame_size',
        label: 'Frame Size',
        type: 'text',
        required: true,
        placeholder: 'e.g. A3, 50×70 cm',
      },
      {
        name: 'mesh_count',
        label: 'Mesh Count',
        type: 'number',
        required: true,
        min: 1,
        step: 1,
        inputMode: 'numeric',
        placeholder: 'e.g. 120',
      },
      {
        name: 'quality',
        label: 'Quality Level',
        type: 'select',
        required: true,
        options: [
          { value: 'standard',        label: 'Standard' },
          { value: 'premium',         label: 'Premium' },
          { value: 'high-definition', label: 'High-Definition' },
        ],
      },
    ],
  },

  printing: {
    label: 'Printing',
    icon: '🖨️',
    color: '#2563eb',
    description: 'Ink & paper parameters',
    fields: [
      {
        name: 'print_material',
        label: 'Print Material',
        type: 'text',
        required: true,
        placeholder: 'e.g. Cotton Jersey',
      },
      {
        name: 'paper_size',
        label: 'Paper Size',
        type: 'text',
        required: true,
        placeholder: 'e.g. A4, A3',
      },
      {
        name: 'ink_type',
        label: 'Ink Type',
        type: 'text',
        required: true,
        placeholder: 'e.g. Water-based, Plastisol',
      },
      {
        name: 'ink_color',
        label: 'Ink Color',
        type: 'text',
        required: true,
        placeholder: 'e.g. CMYK, Black',
      },
      {
        name: 'paper_quantity',
        label: 'Paper Quantity',
        type: 'number',
        required: true,
        min: 1,
        step: 1,
        inputMode: 'numeric',
        placeholder: 'e.g. 500',
      },
      {
        name: 'gel_or_powder',
        label: 'Gel or Powder',
        type: 'select',
        required: true,
        options: [
          { value: 'gel',    label: 'Gel' },
          { value: 'powder', label: 'Powder' },
        ],
      },
    ],
  },

  cutting: {
    label: 'Cutting',
    icon: '✂️',
    color: '#059669',
    description: 'Piece & layout count',
    fields: [
      {
        name: 'no_of_pieces',
        label: 'Number of Pieces',
        type: 'number',
        required: true,
        min: 1,
        step: 1,
        inputMode: 'numeric',
        placeholder: 'e.g. 100',
      },
      {
        name: 'no_of_ups',
        label: 'Number of Ups',
        type: 'number',
        required: true,
        min: 1,
        step: 1,
        inputMode: 'numeric',
        placeholder: 'e.g. 4',
      },
    ],
  },
}
