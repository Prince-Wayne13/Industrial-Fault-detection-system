// The list under the bell: faults this person acknowledged that are not resolved yet. FR-8b, FR-17.
// The Administrator sees the storage alert only (FR-21a, FR-7b).
import { Link } from 'react-router-dom'
import Pill from './Pill.jsx'
import { useUser } from './user.jsx'

export default function BellList({ bell, storageAlerts, onClose }) {
  const { user } = useUser()
  const admin = user.role === 'administrator'
  const items = admin ? [] : bell
  return (
    <div className="popover" role="dialog" aria-label="Faults">
      <h3>{admin ? 'Storage alert' : 'Acknowledged, not resolved'}</h3>
      {items.length === 0 && !storageAlerts && <p className="muted" style={{ margin: 0 }}>Nothing waiting.</p>}
      {storageAlerts > 0 && (
        <Link to="/admin" className="pop-item" onClick={onClose}>
          <div className="row"><strong>Storage</strong><Pill level="warning" /></div>
          <div className="small">Storage is nearly full. See the Admin page.</div>
        </Link>
      )}
      {items.map((f) => (
        <Link key={f.id} to={`/machine/${f.machine_id}`} className="pop-item" onClick={onClose}>
          <div className="row"><strong>{f.machine_name}</strong><Pill level={f.level} /></div>
          <div className="small">{f.parameter}</div>
          <div className="small">{new Date(f.raised_at * 1000).toLocaleTimeString()}</div>
        </Link>
      ))}
    </div>
  )
}
