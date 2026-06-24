import { useState } from 'react'
import { login as apiLogin } from '../api/auth.js'
import { saveSession } from '../auth.js'

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error,    setError]    = useState(null)
  const [loading,  setLoading]  = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const data = await apiLogin(username.trim(), password)
      saveSession(data.access_token, { username: data.username, role: data.role })
      onLogin()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div className="login-logo" aria-hidden>🏭</div>
        <h1 className="login-title">RealPrints</h1>
        <p className="login-sub">Sign in to continue</p>

        <form className="login-form" onSubmit={handleSubmit} noValidate>
          <div className="form-field">
            <label className="form-field__label" htmlFor="lp-username">
              Username
            </label>
            <input
              id="lp-username"
              className="form-field__input"
              type="text"
              autoComplete="username"
              autoCapitalize="none"
              spellCheck={false}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="lp-password">
              Password
            </label>
            <input
              id="lp-password"
              className="form-field__input"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <div className="status-banner status-banner--error" role="alert">
              <span className="status-banner__icon" aria-hidden>⚠️</span>
              <span className="status-banner__msg">{error}</span>
            </div>
          )}

          <button
            type="submit"
            className="btn btn--primary btn--full"
            disabled={loading || !username.trim() || !password}
          >
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  )
}
