// Requirements tracker and measured numbers. Requirements: every requirement
// Each requirement is built, simulated, left-out or not-set. Numbers on this page are measured from the running system.
import { useEffect, useState } from 'react'
import { get } from './api.js'

const SHOW = { built: 'Built', simulated: 'Simulated', 'left-out': 'Left out', 'not-set': 'Not set' }
const pct = (a) => (a ? `${a.percent}% (${a.right} of ${a.of})` : '…')
const ms = (v) => (v == null ? '—' : `${v} ms`)

function Measured({ m }) {
  if (!m) return null
  const acc = m.accuracy?.value
  const rows = [
    ['NFR-1 critical temperature and current found', acc && typeof acc === 'object' ? pct(acc.critical_temp_current) : m.accuracy?.state],
    ['NFR-2 vibration faults found', acc && typeof acc === 'object' ? pct(acc.vibration) : m.accuracy?.state],
    ['All labelled windows right (NFR-1, NFR-2)', acc && typeof acc === 'object' ? pct(acc.all_windows) : m.accuracy?.state],
    ['PR-001 status refresh', `every ${m.status_window_s} s (${m.windows} windows set)`],
    ['PR-001a alert time after status confirmed', m.alerts ? `average ${m.alert_s_avg} s, longest ${m.alert_s_max} s, ${m.alerts_delayed} late of ${m.alerts}` : 'no faults yet'],
    ['PR-002 time a reading spends in the server', `average ${ms(m.reading_ms_avg)}, longest ${ms(m.reading_ms_max)}`],
    ['PR-003 machines at once', m.machines],
    ['PR-004 viewers now / peak', `${m.viewers} / ${m.peak_viewers}`],
    ['PR-005 readings per second', `${m.readings_per_s} (${m.readings_received} received, ${m.readings_invalid} invalid)`],
    ['PR-006 local storage used', `${(m.storage_used * 100).toFixed(3)}% of ${m.storage_cap_mb} MB`],
    ['PR-007 start-up to first data', m.startup_s == null ? '—' : `${m.startup_s} s`],
    ['NFR-5 uptime this run', `${Math.floor(m.uptime_s / 60)} min ${Math.round(m.uptime_s % 60)} s`],
  ]
  return (
    <div className="card table-wrap">
      <table className="fault-table"><tbody>{rows.map(([k, v]) => <tr key={k}><td>{k}</td><td><strong>{v}</strong></td></tr>)}</tbody></table>
    </div>
  )
}

export default function Tracker() {
  const [reqs, setReqs] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [filter, setFilter] = useState('all')
  const [checks, setChecks] = useState(null)

  useEffect(() => {
    const loadMetrics = () => get('/api/metrics').then((d) => d.uptime_s != null && setMetrics(d))
    const loadReqs = () => get('/api/requirements').then((d) => Array.isArray(d) && setReqs(d))
    loadReqs(); loadMetrics()
    const timer = setInterval(loadMetrics, 3000)
    return () => clearInterval(timer)
  }, [])
  useEffect(() => {
    get('/api/checks/status').then(setChecks)
  }, [])
  useEffect(() => {
    if (checks?.finished) get('/api/requirements').then((d) => Array.isArray(d) && setReqs(d))
  }, [checks?.finished])

  const counts = reqs.reduce((c, r) => ({ ...c, [r.status]: (c[r.status] || 0) + 1 }), {})
  const rows = reqs.filter((r) => filter === 'all' || r.status === filter)
  return (
    <div className="page">
      <h1>Requirements tracker</h1>
      <h2>Measured numbers</h2>
      <Measured m={metrics} />

      <h2>Requirements</h2>
      <div className="demo-row">
        {Object.entries(SHOW).map(([k, v]) => <span key={k} className={`chip chip-dark`}>{v}: {counts[k] || 0}</span>)}
        <label>Show
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All ({reqs.length})</option>
            {Object.entries(SHOW).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
      </div>
      <div className="card table-wrap">
        <table className="fault-table">
          <thead><tr><th>Requirement</th><th>Statement</th><th>Status</th><th>Check</th><th>Note</th></tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td><strong>{r.id}</strong></td>
                <td>{r.statement}</td>
                <td><span className={`badge tracker-${r.status}`}>{SHOW[r.status] ?? r.status}</span></td>
                <td>{r.result}</td>
                <td className="muted">{r.note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="muted">The Check column comes from the last run of the check script (Demo page, "Run all checks").</p>
    </div>
  )
}
