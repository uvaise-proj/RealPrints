const BASE = import.meta.env.VITE_API_BASE_URL ?? ''

export async function login(username, password) {
  const res = await fetch(`${BASE}/auth/login`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ username, password }),
  })

  let body
  try { body = await res.json() } catch { body = {} }

  if (!res.ok) {
    const msg = typeof body.detail === 'string'
      ? body.detail
      : `Login failed (HTTP ${res.status})`
    throw new Error(msg)
  }

  return body // { access_token, token_type, role, username }
}
