// The fault pop-up (the approved design). Stays on screen until that person acknowledges it. FR-7, FR-7a, FR-7b, FR-8, FR-16.
// Acknowledging does not close the fault (FR-8b). The Administrator never gets one: the server sends none.
import { Link } from 'react-router-dom'
import Pill from './Pill.jsx'
import { PARAM_LABEL, UNITS } from './status.js'

export default function FaultPopup({ fault: f, machineType, onAcknowledge }) {
  const label = PARAM_LABEL[machineType?.(f.machine_id)]?.[f.parameter] ?? f.parameter
  const unit = UNITS[f.parameter] ?? ''
  const num = (v) => (typeof v === 'number' ? +v.toFixed(2) : v)
  const swing = f.reason === 'fluctuating'
  const low = !swing && f.value != null && f.limit != null && f.value < f.limit
  const what = swing ? `${label} is swinging up and down.` : `${label} is too ${low ? 'low' : 'high'}.`
  const numbers = swing
    ? `Readings change by ${(f.value * 100).toFixed(1)}% each second. Limit is ${(f.limit * 100).toFixed(0)}%.`
    : [f.value != null && `${num(f.value)} ${unit} now.`, f.limit != null && `Limit is ${num(f.limit)} ${unit}.`].filter(Boolean).join(' ')
  return (
    <div className="fault-popup" role="alertdialog" aria-label={`${f.machine_name} fault`}>
      <div className="top">
        <Pill level={f.level} />
        <span className="time">{new Date(f.raised_at * 1000).toLocaleTimeString()}</span>
      </div>
      <div className="machine">{f.machine_name}</div>
      <div className="what">{what}</div>
      <div className="numbers muted">{numbers}{f.delayed && ' This alert came late.'}</div>
      <div className="actions">
        <button className="btn btn-primary" onClick={() => onAcknowledge(f.id)}>Acknowledge</button>
        <Link to={`/machine/${f.machine_id}`} className="btn btn-quiet">Open {f.machine_name}</Link>
      </div>
      <div className="reminder muted">Stays on your screen until you acknowledge it.</div>
    </div>
  )
}
