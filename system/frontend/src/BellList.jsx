// Bell list. Requirements: FR-8b, FR-17
// The faults this person acknowledged that are not resolved yet. Choosing one opens that machine's page.
import { Link } from 'react-router-dom'
import { STATUS_LABEL } from './status.js'

export default function BellList({ bell, storageAlerts, onClose }) {
  return (
    <div className="card bell-list">
      {bell.length === 0 && !storageAlerts && <p className="muted">No open faults.</p>}
      {storageAlerts > 0 && <p className="muted">Storage is nearly full. See the Admin page.</p>}
      {bell.map((f) => (
        <Link key={f.id} to={`/machine/${f.machine_id}`} className="bell-item" onClick={onClose}>
          <span>{f.machine_name} · {f.parameter}</span>
          <span className={`badge ${f.level}`}>{STATUS_LABEL[f.level] ?? f.level}</span>
        </Link>
      ))}
    </div>
  )
}
