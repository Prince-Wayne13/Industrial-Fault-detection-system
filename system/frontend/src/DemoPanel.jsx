// Demo control panel. Requirements: FR-11, FR-12, DC-006
// Live scenarios change what the simulated sensors send. The scenarios that need a clock jump, a full disk or a restart are
// shown as results: "Run all checks" plays all of them in a separate process and the Tracker shows the table.
import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { get, post } from './api.js'
import { useOverview } from './useLive.js'
import { PARAM_LABEL } from './status.js'

// Which scenarios play live in the 5 minutes (each is a list of steps for the simulated sensors).
// A scenario is shown only when the machines it uses exist. 'Pump speed swings' needs Pump 1, so it appears when a pump is added.
const LIVE = [
  ['Normal running', [{ action: 'clear_all' }]],
  ['Lone spike', [{ action: 'spike', machine_id: 'motor-1', parameter: 'temperature' }]],
  ['Sustained warning', [{ action: 'warning', machine_id: 'motor-1', parameter: 'temperature' }]],
  ['Sustained critical', [{ action: 'critical', machine_id: 'motor-1', parameter: 'temperature' }]],
  ['Two faults at once', [{ action: 'warning', machine_id: 'motor-2', parameter: 'temperature' }, { action: 'warning', machine_id: 'motor-2', parameter: 'current' }]],
  ['Sensor goes silent', [{ action: 'silent', machine_id: 'motor-2', parameter: 'rpm' }]],
  ['Pump speed swings', [{ action: 'fluctuate', machine_id: 'pump-1', parameter: 'rpm' }]],
  ['Bad reading', [{ action: 'bad', machine_id: 'motor-2', parameter: 'current' }]],
  ['Maintenance', [{ action: 'maintenance', machine_id: 'motor-2', minutes: 1 }]],
  ['Slow alert', [{ action: 'slow_alert_on' }, { action: 'warning', machine_id: 'motor-1', parameter: 'vibration' }]],
  ['Connection cut', [{ action: 'cut_link' }]],
  ['Heavy load (11 machines)', [{ action: 'heavy_load' }]],
]

export default function DemoPanel() {
  const { data } = useOverview()
  const [chosenMachine, setMachineId] = useState('')
  const [chosenParameter, setParameter] = useState('')
  const [minutes, setMinutes] = useState(30)
  const [delay, setDelay] = useState(5)
  const [message, setMessage] = useState('')
  const [checks, setChecks] = useState(null)
  const poll = useRef(null)

  const machines = data?.machines ?? []
  const machineId = chosenMachine || machines[0]?.id || ''
  const machine = machines.find((m) => m.id === machineId)
  const parameter = chosenParameter in (machine?.parameters ?? {}) ? chosenParameter : Object.keys(machine?.parameters ?? {})[0] ?? ''
  useEffect(() => () => clearInterval(poll.current), [])

  const send = async (step) => {
    const r = await post('/api/demo', { machine_id: machineId, parameter, minutes: Number(minutes), delay: Number(delay), ...step })
    setMessage(r.message)
    return r
  }
  const play = async (steps) => { for (const step of steps) { const r = await send(step); if (!r.ok) break } }
  const btn = (action, label) => <button className="demo-btn" onClick={() => send({ action })}>{label}</button>

  const runChecks = async () => {
    const r = await post('/api/checks/run')
    setMessage(r.message)
    clearInterval(poll.current)
    poll.current = setInterval(async () => {
      const s = await get('/api/checks/status')
      setChecks(s)
      if (!s.running) clearInterval(poll.current)
    }, 2000)
  }

  return (
    <div className="page">
      <h1>Demo control panel</h1>
      <p className="muted">Changes what the simulated sensors send. Watch the <Link to="/">Overview</Link> react. Open a second tab and sign in as someone else to show two people at once.</p>
      <div className="card demo-card">
        <div className="demo-row">
          <label>Start in
            <select value={delay} onChange={(e) => setDelay(e.target.value)}>
              {[[0, 'Now'], [3, '3 seconds'], [5, '5 seconds'], [7, '7 seconds'], [10, '10 seconds'], [15, '15 seconds']].map(([v, t]) => <option key={v} value={v}>{t}</option>)}
            </select>
          </label>
          <span className="muted">A countdown shows in the corner of every screen, then the injection starts. Reset, mode changes and Cancel are always immediate.</span>
        </div>
      </div>
      {message && <p className="notice notice-delayed" role="status">{message}</p>}

      <h2>Connection</h2>
      <div className="card demo-card">
        <div className="demo-row">
          <span className="chip chip-dark">{data?.mode === 'remote' ? 'Remote range · Wi-Fi' : 'Near range · Bluetooth'}</span>
          {btn('mode_near', 'Near range (Bluetooth)')}
          {btn('mode_remote', 'Remote range (Wi-Fi)')}
          <span className="muted">Same equipment data in both modes.</span>
        </div>
        <div className="demo-row">
          <span className="chip chip-dark">Sensor connection {data?.link === 'cut' ? 'offline' : 'active'}</span>
          {btn('cut_link', 'Disconnect sensors')}
          {btn('restore_link', 'Reconnect sensors')}
        </div>
        <div className="demo-row">
          <span className="chip chip-dark">Online database {data?.database_link === 'cut' ? 'offline' : 'connected'}</span>
          {btn('cut_database_link', 'Disconnect online database')}
          {btn('restore_database_link', 'Reconnect online database')}
          {data?.database_link === 'cut' && <span className="muted">{data.pending} database windows waiting to sync.</span>}
        </div>
      </div>

      <h2>Play a scenario live</h2>
      <div className="card demo-card">
        <div className="demo-row">
          {LIVE.filter(([, steps]) => steps.every((st) => !st.machine_id || machines.some((m) => m.id === st.machine_id)))
            .map(([name, steps]) => <button key={name} className="demo-btn" onClick={() => play(steps)}>{name}</button>)}
        </div>
        <div className="demo-row">
          {btn('restore_link', 'Restore connection')}
          <button className="demo-btn demo-btn-off" onClick={() => send({ action: 'remove_load' })}>Remove the extra machines</button>
          {btn('clear_all', 'Reset everything')}
        </div>
      </div>

      <h2>Pick your own</h2>
      <div className="card demo-card">
        <div className="demo-row">
          <label>Machine
            <select value={machineId} onChange={(e) => { setMachineId(e.target.value); setParameter(Object.keys(machines.find((m) => m.id === e.target.value).parameters)[0]) }}>
              {machines.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
            </select>
          </label>
          <label>Parameter
            <select value={parameter} onChange={(e) => setParameter(e.target.value)}>
              {Object.keys(machine?.parameters ?? {}).map((p) => <option key={p} value={p}>{PARAM_LABEL[machine.type][p]}</option>)}
            </select>
          </label>
        </div>
        <div className="demo-row">
          {btn('warning', 'Warning value')}
          {btn('critical', 'Critical value')}
          {btn('spike', 'One spike')}
          {btn('clear', 'Back to normal')}
          {btn('bad', 'Bad reading (5 s)')}
          {btn('silent', 'Sensor goes silent')}
        </div>
        <div className="demo-row">
          <label>Maintenance minutes <input type="number" min="0.1" step="0.1" value={minutes} onChange={(e) => setMinutes(e.target.value)} /></label>
          {btn('maintenance', 'Start maintenance')}
          {btn('end_maintenance', 'End maintenance')}
          {btn('slow_alert_on', 'Slow alerts on')}
          {btn('slow_alert_off', 'Slow alerts off')}
        </div>
      </div>

      <h2>Shown as results</h2>
      <div className="card demo-card">
        <p className="muted">Storage fills up, storage fails, restart, fault returns, limit change, nobody connected, noisy readings, labelled test set, login checks and old data run in the check script, not live.</p>
        <div className="demo-row">
          <button className="demo-btn" onClick={runChecks} disabled={checks?.running}>{checks?.running ? 'Running…' : 'Run all checks'}</button>
          <Link to="/tracker">Open the tracker</Link>
        </div>
        {checks?.output && <pre className="check-output">{checks.output}</pre>}
      </div>
    </div>
  )
}
