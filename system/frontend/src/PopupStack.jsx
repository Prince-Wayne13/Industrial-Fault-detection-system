// All the fault pop-ups on screen, stacked bottom right, newest last. Each stays until this person acknowledges it (FR-7, FR-8).
import FaultPopup from './FaultPopup.jsx'
import { post } from './api.js'

export default function PopupStack({ popups, machineType }) {
  if (!popups.length) return null
  const acknowledge = (id) => post(`/api/faults/${id}/acknowledge`)
  return (
    <div className="popup-stack" aria-live="assertive">
      {[...popups].reverse().map((p) => <FaultPopup key={p.id} fault={p} machineType={machineType} onAcknowledge={acknowledge} />)}
    </div>
  )
}
