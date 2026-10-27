// Machines. Requirements: FR-24, FR-5, FR-18 (filter is a design choice, not in the SRS)
import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { get, live } from './api.js'
import { useOverview } from './useLive.js'
import { STATUS_LABEL } from './status.js'

const TYPES = { motor: 'Motor', pump: 'Water pump', ups: 'Backup power' }

export default function MachinesList() {
  const { data } = useOverview()
  const [faults, setFaults] = useState([])
  const [type, setType] = useState('all')
  const [status, setStatus] = useState('all')
  const load = useCallback(() => { get('/api/faults/history').then((d) => Array.isArray(d) && setFaults(d)) }, [])
  useEffect(() => {
    load()
    live.on('faults_changed', load)
    return () => live.off('faults_changed', load)
  }, [load])
  if (!data) return <div className="page"><p className="muted">Connecting to the server…</p></div>
  const open = (id) => faults.filter((f) => f.machine_id === id && f.status === 'open').length
  const rows = data.machines.filter((m) => (type === 'all' || m.type === type) && (status === 'all' || m.status === status || (status === 'warning' && m.status === 'abnormal')))
  return (
    <div className="page">
      <h1>Machines</h1>
      <div className="demo-row">
        <label>Type
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="all">All</option>
            {Object.entries(TYPES).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
        <label>Status
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="all">All</option>
            {['normal', 'warning', 'critical'].map((s) => <option key={s} value={s}>{STATUS_LABEL[s]}</option>)}
          </select>
        </label>
      </div>
      {rows.length === 0 ? <p className="muted">No machine matches.</p> : (
        <div className="card table-wrap">
          <table className="fault-table">
            <thead><tr><th>Name</th><th>Type</th><th>Status</th><th>Open faults</th><th>Mark</th></tr></thead>
            <tbody>
              {rows.map((m) => (
                <tr key={m.id}>
                  <td><Link to={`/machine/${m.id}`}>{m.name}</Link></td>
                  <td>{TYPES[m.type]}</td>
                  <td><span className={`badge ${m.status}`}>{STATUS_LABEL[m.status]}</span></td>
                  <td>{open(m.id)}</td>
                  <td>{m.maintenance && <span className="mark mark-maint">Maintenance</span>}{m.overdue && <span className="mark mark-overdue">Overdue</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
