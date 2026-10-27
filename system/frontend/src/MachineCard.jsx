// Machine card. Requirements: FR-1, FR-2, FR-3, FR-5, FR-13, FR-14, FR-18, FR-19, FR-24
// One card per machine. Status is a word and a colour, never colour alone. Click opens the machine page.
import { Link } from 'react-router-dom'
import { STATUS_LABEL, UNITS, PARAM_LABEL, formatValue } from './status.js'

function Badge({ status }) {
  return <span className={`badge ${status}`}>{STATUS_LABEL[status] ?? status}</span>
}

function Row({ type, name, p }) {
  return (
    <div className="param-row">
      <span className="param-name">{PARAM_LABEL[type][name]}</span>
      <span className="param-value">
        {p.sensor_fault ? (
          <span className="mark mark-fault">Sensor fault</span>
        ) : (
          <>
            <strong>{formatValue(name, p.value)}</strong> <span className="unit">{p.value === null ? '' : UNITS[name]}</span>
            {p.invalid && <span className="mark mark-invalid">Invalid</span>}
          </>
        )}
      </span>
      {p.status !== 'normal' && p.status !== 'unknown' && <Badge status={p.status} />}
    </div>
  )
}

export default function MachineCard({ machine }) {
  return (
    <Link to={`/machine/${machine.id}`} className={`card machine-card status-${machine.status}`}>
      <div className="card-head">
        <h3>{machine.name}</h3>
        <Badge status={machine.status} />
      </div>
      {(machine.maintenance || machine.overdue) && (
        <div className="marks">
          {machine.maintenance && <span className="mark mark-maint">Maintenance</span>}
          {machine.overdue && <span className="mark mark-overdue">Overdue</span>}
        </div>
      )}
      {Object.entries(machine.parameters).map(([name, p]) => (
        <Row key={name} type={machine.type} name={name} p={p} />
      ))}
    </Link>
  )
}
