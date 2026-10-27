// The activity log. Administrator only. Everything here is also saved in the database. FR-22
import { useCallback, useEffect, useState } from 'react'
import { get, live } from './api.js'
import { KINDS, describe, logTime } from './logFormat.js'

export default function Logs() {
  const [data, setData] = useState(null)
  const [kind, setKind] = useState('all')
  const [error, setError] = useState('')
  const load = useCallback(() => {
    get('/api/logs').then((d) => { if (d.logs) { setData(d); setError('') } else throw new Error(d.message || 'Could not load the log.') })
      .catch((e) => setError(e.message || 'Could not load the log.'))
  }, [])
  useEffect(() => {
    load()
    const timer = setInterval(load, 5000)
    live.on('faults_changed', load)
    return () => { clearInterval(timer); live.off('faults_changed', load) }
  }, [load])

  if (error && !data) return <div className="page"><p className="notice notice-lost" role="alert">{error}</p></div>
  if (!data) return <div className="page"><p className="muted">Loading…</p></div>
  const rows = data.logs.map((e) => ({ e, d: describe(e, data.machine_names) })).filter(({ d }) => kind === 'all' || d.kind === kind)

  return (
    <div className="page">
      <h1>Logs</h1>
      <p className="muted">Who did what and when. Every line is saved in the database, newest first. Only the Administrator can see this page.</p>
      <div className="tabs" role="tablist">
        {KINDS.map(([k, label]) => (
          <button key={k} role="tab" aria-selected={kind === k} className={`demo-btn${kind === k ? '' : ' demo-btn-off'}`} onClick={() => setKind(k)}>{label}</button>
        ))}
        <span className="muted log-count">{rows.length} of {data.total}</span>
      </div>
      {rows.length === 0 ? <p className="muted">Nothing here yet.</p> : (
        <div className="card table-wrap">
          <table className="fault-table">
            <thead><tr><th>When</th><th>Who</th><th>What happened</th><th>Details</th></tr></thead>
            <tbody>
              {rows.map(({ e, d }) => (
                <tr key={e.id ?? e.when}>
                  <td className="log-when">{logTime(e.when)}</td>
                  <td><strong>{e.who}</strong></td>
                  <td>{d.action}</td>
                  <td>
                    <div className="log-details">
                      {d.details.map((x) => (
                        <span key={x.label} className={`log-chip log-${x.tone}`}><span className="log-label">{x.label}</span>{x.text}</span>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
