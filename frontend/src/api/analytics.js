import { request } from './client.js'

/** Remove null / empty-string entries so they don't appear in the query string. */
function buildQS(params) {
  const clean = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v != null && v !== '')
  )
  return new URLSearchParams(clean).toString()
}

export function fetchSummary(params = {}) {
  const qs = buildQS(params)
  return request(`/analytics/summary${qs ? `?${qs}` : ''}`)
}

export function fetchFailureRate(params) {
  return request(`/analytics/failure-rate?${buildQS(params)}`)
}

export function fetchBestConfig(params) {
  return request(`/analytics/best-config?${buildQS(params)}`)
}
