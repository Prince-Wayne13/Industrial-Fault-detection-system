// Machine detail. Requirements: FR-9, FR-10, FR-15, FR-17, FR-18, FR-19
// Live readings, graph (Day, Week, Month, Year), fault history, acknowledge, resolve, maintenance, report.
import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { get, post, live, download } from './api.js'
import { useOverview } from './useLive.js'
import { useUser } from './user.jsx'
import LiveWindow from './LiveWindow.jsx'
import { STATUS_LABEL, UNITS, PARAM_LABEL, formatValue } from './status.js'
import Pill from './Pill.jsx'
import Icon from './Icons.jsx'

const RANGES = [['day', 'Day'], ['week', 'Week'], ['month', 'Month'], ['year', 'Year']]
const when = (t) => (t ? new Date(t * 1000).toLocaleString() : '')

function Graph({ machineId, parameter, label, unit }) {
  const [range, setRange] = useState('day')
  const [result, setResult] = useState({ key: '', points: [] })
  const [error, setError] = useState('')
  const queryKey = `${parameter}:${range}`
  useEffect(() => {
    let alive = true
    const load = async () => {
      try {
        const data = await get(`/api/machines/${machineId}/history?parameter=${parameter}&range=${range}`)
        if (!alive) return
        if (!Array.isArray(data)) throw new Error(data.message || 'The server returned invalid history data.')
        setResult({ key: queryKey, points: data })
        setError('')
      } catch (e) {
        if (alive) setError(e.message || 'Could not load readings for this period.')
      }
    }
    load()
    const timer = setInterval(load, 10000)
    return () => { alive = false; clearInterval(timer) }
  }, [machineId, parameter, range, queryKey])
  const points = result.key === queryKey ? result.points : []
  const tick = (t) => new Date(t * 1000).toLocaleString([], range === 'day' ? { hour: '2-digit', minute: '2-digit' } : { month: 'short', day: 'numeric' })
  return (
    <div className="card">
      <div className="card-head">
        <h3>{label} {unit && <span className="unit">({unit})</span>}</h3>
        <div className="range-buttons">
          {RANGES.map(([key, text]) => (
            <button key={key} className={range === key ? 'demo-btn' : 'demo-btn demo-btn-off'} onClick={() => setRange(key)}>{text}</button>
          ))}
        </div>
      </div>
      {error ? <p className="notice notice-lost" role="alert">{error}</p> : points.length === 0 ? <p className="muted">No readings saved for this period yet.</p> : (
        <div style={{ height: 220 }}>
          <ResponsiveContainer>
            <LineChart data={points}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-faint)" />
              <XAxis dataKey="t" tickFormatter={tick} type="number" domain={['dataMin', 'dataMax']} fontSize={12} />
              <YAxis domain={['auto', 'auto']} fontSize={12} width={50} />
              <Tooltip labelFormatter={when} />
              <Line type="monotone" dataKey="mean" stroke="var(--secondary)" dot={false} connectNulls isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
      {range !== 'day' && <p className="muted">Normal readings are kept for 24 hours (FR-9b), so longer graphs show the windows that remain.</p>}
    </div>
  )
}

export default function MachineDetail() {
  const { id } = useParams()
  const { data } = useOverview()
  const { user } = useUser()
  const [faults, setFaults] = useState([])
  const [parameter, setParameter] = useState('')
  const [minutes, setMinutes] = useState(30)
  const [message, setMessage] = useState('')
  const [faultError, setFaultError] = useState('')
  const [limits, setLimits] = useState(null)
  const [range, setRange] = useState('day')

  const loadFaults = useCallback(() => {
    get(`/api/faults/history?machine_id=${encodeURIComponent(id)}`).then((data) => {
      if (!Array.isArray(data)) throw new Error(data.message || 'The server returned invalid fault history.')
      setFaults(data)
      setFaultError('')
    }).catch((e) => setFaultError(e.message || 'Could not load fault history.'))
  }, [id])
  useEffect(() => {
    loadFaults()
    live.on('faults_changed', loadFaults)
    return () => live.off('faults_changed', loadFaults)
  }, [loadFaults])
  useEffect(() => {
    let alive = true
    get('/api/limits').then((data) => {
      if (!Array.isArray(data?.machines)) throw new Error(data.message || 'The server returned invalid machine limits.')
      if (alive) setLimits(data)
    }).catch((e) => {
      if (alive) setMessage(e.message || 'Could not load machine limits.')
    })
    return () => { alive = false }
  }, [])

  const machine = data?.machines.find((m) => m.id === id)
  const selectedParameter = machine?.parameters[parameter] ? parameter : Object.keys(machine?.parameters ?? {})[0]
  if (!data) return <div className="page"><p className="muted">Connecting to the server…</p></div>
  if (!machine) return <div className="page"><Link to="/">‹ Overview</Link><h1>No such machine</h1></div>

  const role = user?.role
  const me = user?.username
  const act = async (path, body) => {
    try {
      const r = await post(path, body)
      setMessage(r.ok ? '' : r.message)
      if (r.ok) loadFaults()
    } catch (e) {
      setMessage(e.message || 'The action could not be completed.')
    }
  }
  const mine = (f) => f.acknowledged_by?.some((a) => a.user === me) ?? false
  const labels = PARAM_LABEL[machine.type] ?? {}

  return (
    <div className="page machine-page">
      <Link to="/machines" className="machine-back">‹ <span>Back to machines</span></Link>
      <header className="machine-hero card">
        <div className="machine-identity">
          <span className="machine-icon"><Icon name={machine.type} size={26} /></span>
          <div>
            <p className="machine-eyebrow">Machine details</p>
            <h1>{machine.name}</h1>
            <p className="muted">{machine.type === 'ups' ? 'Backup power' : machine.type === 'pump' ? 'Water pump' : 'Motor'}</p>
          </div>
        </div>
        <div className="machine-state">
          {!machine.maintenance && !machine.connection_offline && <Pill level={machine.status} />}
          {machine.maintenance && <Pill level="maintenance">Maintenance · readings paused</Pill>}
          {machine.connection_offline && <Pill level="unknown">Connection offline</Pill>}
          {machine.overdue && <Pill level="critical">Overdue</Pill>}
        </div>
      </header>

      {role === 'engineer' && (
        <section className="machine-maintenance card">
          <div>
            <h2>Maintenance mode</h2>
            <p className="muted">{machine.maintenance ? 'Live readings and new fault alerts are paused while this machine is being serviced.' : 'Pause live readings and new fault alerts while this machine is being serviced.'}</p>
          </div>
          <div className="demo-row">
            {!machine.maintenance && <label>Duration (minutes)<input type="number" min="1" value={minutes} onChange={(e) => setMinutes(e.target.value)} /></label>}
            {machine.maintenance
              ? <button className="btn btn-quiet" onClick={() => act(`/api/machines/${id}/maintenance`, { on: false })}>End maintenance</button>
              : <button className="btn btn-primary" onClick={() => act(`/api/machines/${id}/maintenance`, { on: true, minutes: Number(minutes) })}>Start maintenance</button>}
          </div>
        </section>
      )}
      {message && <p className="notice notice-lost" role="status">{message}</p>}
      {(machine.maintenance || machine.connection_offline) && (
        <div className="notice notice-delayed" role="status">
          {machine.maintenance ? 'Readings are paused while this machine is under maintenance.' : 'The sensor connection is offline. Readings will resume when the connection is restored.'}
        </div>
      )}

      <section className="machine-section">
        <div className="machine-section-head">
          <div><p className="machine-eyebrow">At a glance</p><h2>Live readings</h2></div>
          <span className="muted">Updates in real time</span>
        </div>
        <div className="card-grid tiles machine-readings">
          {Object.entries(machine.parameters).map(([name, p]) => (
            <div key={name} className={`card tile reading-card reading-${p.status}`}>
              <div className="param-name">{labels[name]}</div>
              {machine.maintenance || machine.connection_offline ? <span className="mark mark-paused">Readings paused</span> : p.sensor_fault ? <span className="mark mark-fault">Sensor fault</span> : (
                <div className="tile-value"><strong>{formatValue(name, p.value)}</strong> <span className="unit">{p.value === null ? '' : UNITS[name]}</span>
                  {p.invalid && <span className="mark mark-invalid">Invalid</span>}</div>
              )}
              {!machine.maintenance && !machine.connection_offline && <Pill level={p.status} />}
            </div>
          ))}
        </div>
      </section>

      <section className="machine-section">
        <div className="machine-section-head">
          <div><p className="machine-eyebrow">Performance</p><h2>Readings and trends</h2></div>
        </div>
        <div className="machine-controls card">
          <label>Parameter
            <select value={selectedParameter} onChange={(e) => setParameter(e.target.value)}>
              {Object.keys(machine.parameters).map((p) => <option key={p} value={p}>{labels[p]}</option>)}
            </select>
          </label>
          {(role === 'operator' || role === 'engineer') && (
            <>
              <label>Report period
                <select value={range} onChange={(e) => setRange(e.target.value)}>
                  {RANGES.map(([k, t]) => <option key={k} value={k}>{t}</option>)}
                </select>
              </label>
              <button className="btn btn-primary" onClick={async () => {
                try {
                  const r = await download(`/api/report?machine_id=${encodeURIComponent(id)}&range=${range}`, `${id}-${range}-report.csv`)
                  if (!r.ok) setMessage(r.message)
                  else setMessage('')
                } catch (e) {
                  setMessage(e.message || 'Could not generate the report.')
                }
              }}>Generate report</button>
            </>
          )}
        </div>
        {!machine.maintenance && !machine.connection_offline && limits?.machines && selectedParameter && (
          <LiveWindow machine={machine} parameter={selectedParameter} label={labels[selectedParameter]} unit={UNITS[selectedParameter]}
                      rule={limits.machines.find((item) => item.id === machine.id)?.limits[selectedParameter] ?? {}}
                      fraction={limits.trend_fraction ?? 0.6} cut={limits.status_probability ?? 0.5} />
        )}
        {selectedParameter && <Graph machineId={id} parameter={selectedParameter} label={labels[selectedParameter]} unit={UNITS[selectedParameter]} />}
      </section>

      <section className="machine-section">
        <div className="machine-section-head">
          <div><p className="machine-eyebrow">Fault log</p><h2>History and faults</h2></div>
          <span className="machine-fault-count">{faults.length} {faults.length === 1 ? 'event' : 'events'}</span>
        </div>
        {faultError ? <p className="notice notice-lost" role="alert">{faultError}</p> : faults.length === 0 ? <div className="card machine-empty"><p>No faults recorded for this machine.</p><span className="muted">Fault events will appear here when detected.</span></div> : (
          <div className="card table-wrap">
            <table className="fault-table">
              <thead><tr><th>Parameter</th><th>Level</th><th>Raised</th><th>Acknowledged by</th><th>State</th><th /></tr></thead>
              <tbody>
                {faults.map((f) => (
                  <tr key={f.id}>
                    <td>{labels[f.parameter] ?? f.parameter}</td>
                    <td><span className={`badge ${f.level}`}>{STATUS_LABEL[f.level] ?? f.level}</span></td>
                    <td>{when(f.raised_at)}{f.delayed && ' (late)'}</td>
                    <td>{f.acknowledged_by.map((a) => a.user).join(', ') || '—'}</td>
                    <td>{f.status === 'resolved' ? `Resolved by ${f.resolved_by}, ${when(f.resolved_at)}` : 'Open'}</td>
                    <td>
                      {f.status === 'open' && (role === 'operator' || role === 'engineer') && !mine(f) &&
                        <button className="btn btn-quiet" onClick={() => act(`/api/faults/${f.id}/acknowledge`)}>Acknowledge</button>}
                      {f.status === 'open' && role === 'engineer' && mine(f) &&
                        <button className="btn btn-primary" onClick={() => act(`/api/faults/${f.id}/resolve`)}>Resolve</button>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  )
}
