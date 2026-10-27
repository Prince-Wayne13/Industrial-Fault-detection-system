// Admin. Requirements: FR-21a, FR-22, FR-27
import { useCallback, useEffect, useState } from 'react'
import { get, post, del, live } from './api.js'
import { useUser } from './user.jsx'

const when = (t) => new Date(t * 1000).toLocaleString()

export default function Admin() {
  const { user } = useUser()
  const [data, setData] = useState(null)
  const [message, setMessage] = useState('')
  const [nu, setNu] = useState({ username: '', full_name: '', role: 'operator', password: '' })
  const [nm, setNm] = useState({ id: '', name: '', type: 'motor' })
  const load = useCallback(() => { get('/api/admin').then((d) => d.users && setData(d)) }, [])
  useEffect(() => {
    load()
    const timer = setInterval(load, 5000)
    live.on('faults_changed', load)
    return () => { clearInterval(timer); live.off('faults_changed', load) }
  }, [load])

  const run = async (promise, after) => {
    const r = await promise
    setMessage(r.ok ? '' : r.message)
    if (r.ok) { load(); after?.() }
  }
  if (!data) return <div className="page"><p className="muted">Loading…</p></div>
  const s = data.storage
  const pct = Math.round(s.used * 1000) / 10

  return (
    <div className="page">
      <h1>Admin</h1>
      {message && <p className="notice notice-lost" role="alert">{message}</p>}

      <h2>Storage</h2>
      <div className="card">
        <div className="bar" role="img" aria-label={`Local storage ${pct}% used`}>
          <div className={`bar-fill ${s.used >= s.alert_at ? 'bar-hot' : ''}`} style={{ width: `${Math.max(pct, 0.5)}%` }} />
          <div className="bar-mark" style={{ left: `${s.alert_at * 100}%` }} title="Alert level" />
        </div>
        <p className="muted">{pct}% of {s.cap_mb} MB used. The alert comes at {s.alert_at * 100}%.
          {s.used >= s.alert_at && <strong> Storage is nearly full.</strong>}</p>
        <p className="muted">Online database: {s.online_available ? 'connected' : 'cut'}{s.online_simulated && ' (simulated by a second local file)'}.
          {s.pending > 0 && ` ${s.pending} windows waiting to be sent.`} {s.temp_buffer > 0 && ` ${s.temp_buffer} windows in temporary storage.`}</p>
        {s.events.length > 0 && <ul className="muted">{s.events.map((e, i) => <li key={i}>{when(e.time)} · {e.kind} {e.detail}</li>)}</ul>}
      </div>

      <h2>Users</h2>
      <div className="card table-wrap">
        <table className="fault-table">
          <thead><tr><th>Username</th><th>Full name</th><th>Role</th><th /></tr></thead>
          <tbody>
            {data.users.map((u) => (
              <tr key={u.username}>
                <td>{u.username}</td><td>{u.full_name}</td><td style={{ textTransform: 'capitalize' }}>{u.role}</td>
                <td>{u.username !== user.username && <button className="demo-btn demo-btn-off" onClick={() => run(del(`/api/admin/users/${u.username}`))}>Remove</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="demo-row top-gap">
          <label>Username<input value={nu.username} onChange={(e) => setNu({ ...nu, username: e.target.value })} /></label>
          <label>Full name<input value={nu.full_name} onChange={(e) => setNu({ ...nu, full_name: e.target.value })} /></label>
          <label>Role
            <select value={nu.role} onChange={(e) => setNu({ ...nu, role: e.target.value })}>
              <option value="operator">Operator</option><option value="engineer">Engineer</option><option value="administrator">Administrator</option>
            </select>
          </label>
          <label>Password (15 or more characters)<input type="password" value={nu.password} onChange={(e) => setNu({ ...nu, password: e.target.value })} autoComplete="new-password" /></label>
          <button className="demo-btn" onClick={() => run(post('/api/admin/users', nu), () => setNu({ username: '', full_name: '', role: 'operator', password: '' }))}>Add user</button>
        </div>
        <p className="muted">The Administrator cannot reset a password. A person changes their own on the Settings page.</p>
      </div>

      <h2>Machines</h2>
      <div className="card table-wrap">
        <table className="fault-table">
          <thead><tr><th>Id</th><th>Name</th><th>Type</th><th /></tr></thead>
          <tbody>
            {data.machines.map((m) => (
              <tr key={m.id}><td>{m.id}</td><td>{m.name}</td><td>{m.type}</td>
                <td><button className="demo-btn demo-btn-off" onClick={() => run(del(`/api/admin/machines/${m.id}`))}>Remove</button></td></tr>
            ))}
          </tbody>
        </table>
        <div className="demo-row top-gap">
          <label>Id<input value={nm.id} onChange={(e) => setNm({ ...nm, id: e.target.value })} placeholder="motor-4" /></label>
          <label>Name<input value={nm.name} onChange={(e) => setNm({ ...nm, name: e.target.value })} placeholder="Motor 4" /></label>
          <label>Type
            <select value={nm.type} onChange={(e) => setNm({ ...nm, type: e.target.value })}>
              <option value="motor">Motor</option><option value="pump">Water pump</option><option value="ups">Backup power</option>
            </select>
          </label>
          <button className="demo-btn" onClick={() => run(post('/api/admin/machines', nm), () => setNm({ id: '', name: '', type: 'motor' }))}>Add machine</button>
        </div>
      </div>

      <h2>Change log</h2>
      {data.change_log.length === 0 ? <p className="muted">No changes yet.</p> : (
        <div className="card table-wrap">
          <table className="fault-table">
            <thead><tr><th>When</th><th>Who</th><th>What</th><th>Old</th><th>New</th></tr></thead>
            <tbody>{data.change_log.map((c, i) => <tr key={i}><td>{when(c.when)}</td><td>{c.who}</td><td>{c.what}</td><td>{JSON.stringify(c.old)}</td><td>{JSON.stringify(c.new)}</td></tr>)}</tbody>
          </table>
        </div>
      )}
    </div>
  )
}
