const KEY = 'rp_token'
const USER_KEY = 'rp_user'

export function getToken()   { return localStorage.getItem(KEY) }
export function getUser()    { try { return JSON.parse(localStorage.getItem(USER_KEY)) } catch { return null } }
export function isLoggedIn() { return Boolean(getToken()) }

export function saveSession(token, user) {
  localStorage.setItem(KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearSession() {
  localStorage.removeItem(KEY)
  localStorage.removeItem(USER_KEY)
}
