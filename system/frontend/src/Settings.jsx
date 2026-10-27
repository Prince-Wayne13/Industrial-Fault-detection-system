// Settings. Requirements: FR-23, FR-23a, FR-23b, FR-26 (the dark theme comes later)
import { useCallback, useEffect, useState } from 'react'
import { get, post } from './api.js'
import { useUser } from './user.jsx'
import { UNITS } from './status.js'
import { paramLabel } from './logFormat.js'

const KEYS = { warning: 'Warning above', critical: 'Critical above', abnormal: 'Abnormal above', abnormal_below: 'Abnormal below' }

function LimitRow({ machineId, machineName, parameter, rule, canEdit, onSaved }) {
  const [values, setValues] = useState(() => Object.fromEntries(Object.keys(KEYS).map((k) => [k, rule[k] == null ? '' : String(rule[k])])))
  const [message, setMessage] = useState('')
  const save = async () => {
    // An empty box means "not necessary": the limit is removed. Only limits with a value are used.
    const limits = Object.fromEntries(Object.entries(values).map(([k, v]) => [k, v.trim() === '' ? null : Number(v)]))
    if (Object.values(limits).some((v) => Number.isNaN(v))) return setMessage('A limit must be a number.')
    try {
      const r = await post('/api/limits', { machine_id: machineId, parameter, limits })
      setMessage(r.ok ? 'Saved. Applies from the next reading.' : r.message)
      if (r.ok) onSaved()
    } catch (e) {
      setMessage(e.message || 'Could not save this machine limit.')
    }
  }
  return (
    <tr>
      <td>{paramLabel(parameter)} <span className="unit">({UNITS[parameter]})</span></td>
      {Object.keys(KEYS).map((k) => (
        <td key={k}>
          <input type="number" step="any" value={values[k]} disabled={!canEdit} placeholder="not necessary"
                 className={`limit-input${values[k] === '' ? ' limit-empty' : ''}`}
                 onChange={(e) => setValues({ ...values, [k]: e.target.value })} aria-label={`${machineName} ${parameter} ${KEYS[k]}`} />
        </td>
      ))}
      <td>{canEdit && <button className="demo-btn" onClick={save}>Save</button>} <span className="muted">{message}</span></td>
    </tr>
  )
}

export default function Settings() {
  const { user, setUser } = useUser()
  const [limits, setLimits] = useState(null)
  const [minutes, setMinutes] = useState(user.session_min)
  const [msg, setMsg] = useState({})
  const [limitsError, setLimitsError] = useState('')
  const [pw, setPw] = useState({ old: '', new: '', again: '' })
  const loadLimits = useCallback(() => {
    get('/api/limits').then((data) => {
      if (!Array.isArray(data.machines)) throw new Error(data.message || 'The server returned invalid limits.')
      setLimits(data)
      setLimitsError('')
    }).catch((e) => setLimitsError(e.message || 'Could not load machine limits.'))
  }, [])
  useEffect(() => { loadLimits() }, [loadLimits])

  const saveMinutes = async () => {
    const r = await post('/api/me/session', { minutes: Number(minutes) })
    if (r.ok) setUser({ ...user, session_min: Number(minutes) })
    setMsg({ ...msg, session: r.ok ? 'Saved.' : r.message })
  }
  const savePassword = async () => {
    if (pw.new !== pw.again) return setMsg({ ...msg, pw: 'The two new passwords are not the same.' })
    const r = await post('/api/me/password', { old: pw.old, new: pw.new })
    setMsg({ ...msg, pw: r.ok ? 'Password changed.' : r.message })
    if (r.ok) setPw({ old: '', new: '', again: '' })
  }
  const isEngineer = user.role === 'engineer'

  return (
    <div className="page">
      <h1>Settings</h1>
      <div className="card demo-card">
        <h3>Sign-out time</h3>
        <div className="demo-row">
          <label>Minutes without activity
            <select value={minutes} onChange={(e) => setMinutes(e.target.value)}>{[1, 2, 3, 4, 5].map((m) => <option key={m} value={m}>{m}</option>)}</select>
          </label>
          <button className="demo-btn" onClick={saveMinutes}>Save</button>
          <span className="muted">{msg.session}</span>
        </div>
        <h3>Theme</h3>
        <p className="muted">Light. A dark theme will be added later.</p>
        <h3>Change password</h3>
        <div className="demo-row">
          <label>Current<input type="password" value={pw.old} onChange={(e) => setPw({ ...pw, old: e.target.value })} autoComplete="current-password" /></label>
          <label>New (8 or more characters)<input type="password" value={pw.new} onChange={(e) => setPw({ ...pw, new: e.target.value })} autoComplete="new-password" /></label>
          <label>New again<input type="password" value={pw.again} onChange={(e) => setPw({ ...pw, again: e.target.value })} autoComplete="new-password" /></label>
          <button className="demo-btn" onClick={savePassword}>Change</button>
        </div>
        <span className="muted">{msg.pw}</span>
      </div>

      {isEngineer && limits && (
        <>
          <h2>Limits</h2>
          <p className="muted">Each machine has its own limits. Fill in the limits you need and leave the others empty: an empty limit is not necessary and is not used. At least one limit must stay. Changes apply to that machine from the next reading, and are recorded in the log.</p>
          {limits.machines.length === 0 ? <p className="muted">No machines are registered.</p> : limits.machines.map((machine) => (
            <section className="group" key={machine.id}>
              <div className="group-head"><h3>{machine.name}</h3><span className="muted">{machine.type}</span></div>
              <div className="card table-wrap">
                <table className="fault-table">
                  <thead><tr><th>Parameter</th>{Object.values(KEYS).map((k) => <th key={k}>{k}</th>)}<th /></tr></thead>
                  <tbody>
                    {Object.entries(machine.limits).map(([parameter, rule]) => (
                      <LimitRow key={`${machine.id}-${parameter}`} machineId={machine.id} machineName={machine.name}
                                parameter={parameter} rule={rule} canEdit onSaved={loadLimits} />
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          ))}
        </>
      )}
      {isEngineer && limitsError && <p className="notice notice-lost" role="alert">{limitsError}</p>}
    </div>
  )
}
