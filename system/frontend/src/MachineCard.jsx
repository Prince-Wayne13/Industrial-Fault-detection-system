// One machine on the Overview: live readings, status mark, and the Maintenance, Overdue, Invalid and Sensor fault marks.
// FR-1, FR-2, FR-3, FR-5, FR-13, FR-14, FR-18, FR-19, FR-24. Choosing it opens the machine page.
import { Link } from 'react-router-dom'
import Icon from './Icons.jsx'
import Pill from './Pill.jsx'
import { UNITS, PARAM_LABEL, formatValue } from './status.js'

export default function MachineCard({ machine }) {
  return (
    <Link to={`/machine/${machine.id}`} className="mcard" aria-label={`${machine.name}, open details`}>
      <div className="head">
        <span className="icon"><Icon name={machine.type} size={22} /></span>
        <span className="name">{machine.name}</span>
        <span className="pills">
          {machine.maintenance && <Pill level="maintenance">Maintenance</Pill>}
          {machine.overdue && <Pill level="critical">Overdue</Pill>}
          <Pill level={machine.status} />
        </span>
      </div>
      <dl className="reads">
        {Object.entries(machine.parameters).map(([name, p]) => (
          <div className="read" key={name}>
            <dt>{PARAM_LABEL[machine.type][name]}</dt>
            <dd>
              {p.sensor_fault ? (
                <span className="mark sensor">Sensor fault</span>
              ) : (
                <>
                  {formatValue(name, p.value)}<span className="unit">{p.value === null ? '' : UNITS[name]}</span>
                  {p.invalid && <span className="mark invalid">Invalid</span>}
                </>
              )}
            </dd>
          </div>
        ))}
      </dl>
    </Link>
  )
}
