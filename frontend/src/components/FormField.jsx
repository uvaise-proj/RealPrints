/**
 * Reusable field renderer. Driven entirely by the field config object from stageFields.js.
 * Supports: text input, number input, select dropdown.
 */
export default function FormField({ field, value, onChange }) {
  const id = `field-${field.name}`
  const handleChange = (e) => onChange(field.name, e.target.value)

  return (
    <div className="form-field">
      <label htmlFor={id} className="form-field__label">
        {field.label}
        {field.unit && <span className="form-field__unit">{field.unit}</span>}
        {field.required && (
          <span className="form-field__required" aria-label="required">*</span>
        )}
      </label>

      {field.type === 'select' ? (
        <select
          id={id}
          className="form-field__input"
          value={value}
          onChange={handleChange}
          required={field.required}
        >
          <option value="">Choose…</option>
          {field.options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          id={id}
          type={field.type}
          className="form-field__input"
          value={value}
          onChange={handleChange}
          required={field.required}
          placeholder={field.placeholder}
          min={field.min}
          max={field.max}
          step={field.step}
          inputMode={field.inputMode}
        />
      )}
    </div>
  )
}
