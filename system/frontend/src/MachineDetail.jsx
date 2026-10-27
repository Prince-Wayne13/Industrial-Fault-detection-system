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

const RANGES = [['day', 'Day'], ['week', 'Week'], ['month', 'Month'], ['year', 'Year']]
const when = (t) => (t ? new Date(t * 1000).toLocaleString() : '')

function Graph({ machineId, parameter, label, unit }) {
  const [range, setRange] = useState('day')
  const [limits, setLimits] = useState(null)
  useEffect(() => { get('/api/limits').then(setLimits) }, [])
  const [points, setPoints] = useState([])
  useEffect(() => {
    let alive = true
    const load = () => get(`/api/machines/${machineId}/history?parameter=${parameter}&range=${range}`).then((d) => alive && setPoints(d)).catch(() => {})
    load()
    const timer = setInterval(load, 10000)
    return () => { alive = false; clearInterval(timer) }
  }, [machineId, parameter, range])
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
      {points.length === 0 ? <p className="muted">No readings saved for this period yet.</p> : (
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
  const [range, setRange] = useState('day')

  const loadFaults = useCallback(() => {
    get(`/api/faults/history?machine_id=${id}`).then(setFaults).catch(() => {})
  }, [id])
  useEffect(() => {
    loadFaults()
    live.on('faults_changed', loadFaults)
    return () => live.off('faults_changed', loadFaults)
  }, [loadFaults])

  const machine = data?.machines.find((m) => m.id === id)
  useEffect(() => { if (machine && !parameter) setParameter(Object.keys(machine.parameters)[0]) }, [machine, parameter])
  if (!data) return <div className="page"><p className="muted">Connecting to the server…</p></div>
  if (!machine) return <div className="page"><Link to="/">‹ Overview</Link><h1>No such machine</h1></div>

  const role = user?.role
  const me = user?.username
  const act = async (path, body) => {
    const r = await post(path, body)
    setMessage(r.ok ? '' : r.message)
  }
  const mine = (f) => f.acknowledged_by.some((a) => a.user === me)
  const labels = PARAM_LABEL[machine.type]

  return (
    <div className="page">
      <Link to="/">‹ Overview</Link>
      <div className="card-head detail-head">
        <h1>{machine.name}</h1>
        <span className={`badge ${machine.status}`}>{STATUS_LABEL[machine.status]}</span>
        {machine.maintenance && <span className="mark mark-maint">Maintenance</span>}
        {machine.overdue && <span className="mark mark-overdue">Overdue</span>}
      </div>

      {role === 'engineer' && (
        <div className="demo-row maint-row">
          <label>Maintenance minutes <input type="number" min="1" value={minutes} onChange={(e) => setMinutes(e.target.value)} /></label>
          {machine.maintenance
            ? <button className="demo-btn" onClick={() => act(`/api/machines/${id}/maintenance`, { on: false })}>End maintenance</button>
            : <button className="demo-btn" onClick={() => act(`/api/machines/${id}/maintenance`, { on: true, minutes: Number(minutes) })}>Start maintenance</button>}
        </div>
      )}
      {message && <p className="muted" role="status">{message}</p>}

      <h2>Live readings</h2>
      <div className="card-grid tiles">
        {Object.entries(machine.parameters).map(([name, p]) => (
          <div key={name} className="card tile">
            <div className="param-name">{labels[name]}</div>
            {p.sensor_fault ? <span className="mark mark-fault">Sensor fault</span> : (
              <div className="tile-value"><strong>{formatValue(name, p.value)}</strong> <span className="unit">{p.value === null ? '' : UNITS[name]}</span>
                {p.invalid && <span className="mark mark-invalid">Invalid</span>}</div>
            )}
            <span className={`badge ${p.status}`}>{STATUS_LABEL[p.status]}</span>
          </div>
        ))}
      </div>

      <h2>Window and graph</h2>
      <div className="demo-row">
        <label>Parameter
          <select value={parameter} onChange={(e) => setParameter(e.target.value)}>
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
            <button className="demo-btn" onClick={async () => { const r = await download(`/api/report?machine_id=${id}&range=${range}`, `${id}-${range}-report.csv`); if (!r.ok) setMessage(r.message) }}>Generate report</button>
          </>
        )}
      </div>
      {parameter && limits?.limits && (
        <LiveWindow machine={machine} parameter={parameter} label={labels[parameter]} unit={UNITS[parameter]}
                    rule={limits.limits[machine.type]?.[parameter] ?? {}} fraction={limits.trend_fraction ?? 1} />
      )}
      {parameter && <Graph machineId={id} parameter={parameter} label={labels[parameter]} unit={UNITS[parameter]} />}

      <h2>History and faults</h2>
      {faults.length === 0 ? <p className="muted">No faults recorded for this machine.</p> : (
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
                      <button className="demo-btn" onClick={() => act(`/api/faults/${f.id}/acknowledge`)}>Acknowledge</button>}
                    {f.status === 'open' && role === 'engineer' && mine(f) &&
                      <button className="demo-btn" onClick={() => act(`/api/faults/${f.id}/resolve`)}>Resolve</button>}
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
