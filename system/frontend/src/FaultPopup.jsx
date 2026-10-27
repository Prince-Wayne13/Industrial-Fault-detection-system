// Fault pop-up. Requirements: FR-7, FR-7a, FR-7b, FR-7c, FR-8, FR-8a, FR-16
// Stays on screen until this person acknowledges it. Acknowledging does not close the fault (FR-8b).
import { useState } from 'react'
import { post } from './api.js'
import { STATUS_LABEL, PARAM_LABEL } from './status.js'

export default function FaultPopup({ popups, machineType }) {
  const [error, setError] = useState('')
  if (!popups.length) return null
  const f = popups[0]
  const label = PARAM_LABEL[machineType(f.machine_id)]?.[f.parameter] ?? f.parameter
  const acknowledge = async () => {
    const r = await post(`/api/faults/${f.id}/acknowledge`)
    setError(r.ok ? '' : r.message)
  }
  return (
    <div className="popup-backdrop" role="alertdialog" aria-labelledby="popup-title">
      <div className="card popup">
        <div className="card-head">
          <h2 id="popup-title">Fault: {f.machine_name}</h2>
          <span className={`badge ${f.level}`}>{STATUS_LABEL[f.level] ?? f.level}</span>
        </div>
        <p><strong>{label}</strong> is outside its limit{f.limit != null && <> (limit {f.limit})</>}.</p>
        <p className="muted">Raised {new Date(f.raised_at * 1000).toLocaleTimeString()}{f.delayed && ' · this alert came late'}</p>
        {popups.length > 1 && <p className="muted">{popups.length - 1} more waiting.</p>}
        {error && <p className="muted" role="status">{error}</p>}
        <button className="demo-btn" onClick={acknowledge}>Acknowledge</button>
      </div>
    </div>
  )
}
