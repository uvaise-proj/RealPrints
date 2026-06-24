import { clearSession, getToken } from '../auth.js'

const BASE = import.meta.env.VITE_API_BASE_URL ?? ''

export async function request(path, options = {}) {
  const token = getToken()
  const authHeader = token ? { Authorization: `Bearer ${token}` } : {}

  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...authHeader, ...options.headers },
    ...options,
  })

  if (res.status === 401) {
    clearSession()
    window.dispatchEvent(new Event('rp:unauthorized'))
    throw new Error('Session expired. Please sign in again.')
  }

  if (!res.ok) {
    let detail = `Request failed (HTTP ${res.status})`
    try {
      const body = await res.json()
      if (typeof body.detail === 'string') {
        detail = body.detail
      } else if (Array.isArray(body.detail)) {
        detail = body.detail.map((e) => e.msg).join('; ')
      }
    } catch { /* non-JSON error body */ }
    throw new Error(detail)
  }

  return res.json()
}

export function fetchProjects(params = {}) {
  const qs = new URLSearchParams({ skip: 0, limit: 100, ...params }).toString()
  return request(`/projects?${qs}`)
}

export function submitProcess(payload) {
  return request('/process', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
