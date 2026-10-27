// Fault-Detect sign-in. Requirements: FR-26, FR-28, FR-28a, FR-28b, FR-28c, FR-28d
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useUser } from './user.jsx'

const DEMO = [['admin1', 'Administrator'], ['engineer1', 'Engineer'], ['engineer2', 'Engineer'], ['operator1', 'Operator'], ['operator2', 'Operator']]

export default function SignIn() {
  const { signIn } = useUser()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState(sessionStorage.getItem('fd-note') || '')
  const [busy, setBusy] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setBusy(true)
    const r = await signIn(username.trim(), password)
    setBusy(false)
    if (r.ok) { sessionStorage.removeItem('fd-note'); navigate('/') } else setMessage(r.message)
  }

  return (
    <div className="page signin">
      <div className="card signin-card">
        <h1>Fault-Detect</h1>
        <form onSubmit={submit} className="demo-card">
          <label>Username
            <input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" autoFocus />
          </label>
          <label>Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" />
          </label>
          {message && <p className="notice notice-lost" role="alert">{message}</p>}
          <button className="demo-btn" disabled={busy || !username || !password}>Sign in</button>
        </form>
        <details className="muted">
          <summary>Demo accounts</summary>
          <p>Choose one to fill the form. Demo only: the password is <code>demo-password-for-</code> followed by the username.</p>
          <div className="demo-row">
            {DEMO.map(([u, role]) => (
              <button key={u} type="button" className="demo-btn demo-btn-off" onClick={() => { setUsername(u); setPassword(`demo-password-for-${u}`) }}>{u} · {role}</button>
            ))}
          </div>
        </details>
      </div>
    </div>
  )
}
