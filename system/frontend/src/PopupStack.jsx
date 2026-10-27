// Fault pop-ups, one at a time, bottom right. The most serious comes first (critical, then the oldest). When this person acknowledges it,
// the next one appears. A small count says how many more are waiting. Each stays until acknowledged (FR-7, FR-8).
import FaultPopup from './FaultPopup.jsx'
import { post } from './api.js'

const rank = (p) => (p.level === 'critical' ? 0 : 1)

export default function PopupStack({ popups, machineType }) {
  if (!popups.length) return null
  const acknowledge = (id) => post(`/api/faults/${id}/acknowledge`)
  const [first] = [...popups].sort((a, b) => rank(a) - rank(b) || a.raised_at - b.raised_at)
  const waiting = popups.length - 1
  return (
    <div className="popup-stack" aria-live="assertive">
      <FaultPopup key={first.id} fault={first} machineType={machineType} onAcknowledge={acknowledge} />
      {waiting > 0 && <div className="popup-waiting">{waiting} more waiting. They appear one by one as you acknowledge.</div>}
    </div>
  )
}
