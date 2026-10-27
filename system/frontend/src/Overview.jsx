// The Overview: every machine at a glance. UC-1, FR-1 to FR-3, FR-13, FR-14, FR-24, NFR-8, PR-001, PR-002.
import MachineCard from './MachineCard.jsx'
import { useOverview } from './useLive.js'

const GROUPS = [['motor', 'Motors'], ['pump', 'Water pumps'], ['ups', 'Backup power']]

export default function Overview() {
  const { data, connected } = useOverview()
  if (!data) return <div className="page"><h1>Overview</h1><p className="muted">Connecting to the server…</p></div>
  const ms = data.machines
  const count = (fn) => ms.filter(fn).length
  const tiles = [
    { cls: '', label: 'Total machines', n: ms.length },
    { cls: 'normal', label: 'Normal', n: count((m) => m.status === 'normal') },
    { cls: 'warning', label: 'Warning', n: count((m) => m.status === 'warning' || m.status === 'abnormal') },
    { cls: 'critical', label: 'Critical', n: count((m) => m.status === 'critical') },
    { cls: 'maintenance', label: 'In maintenance', n: count((m) => m.maintenance) },
  ]
  return (
    <div className="page">
      {!connected && <div className="notice notice-lost">Live connection lost. The numbers below may be old. Trying again…</div>}
      {data.link === 'cut' && (
        <div className="notice notice-delayed">Connection to the online database is cut. Readings are still collected and shown here; {data.pending} saved windows will be sent when it returns.</div>
      )}
      {data.alerts_delayed && <div className="notice notice-delayed">Alerts delayed: a fault alert came more than 2 seconds late.</div>}
      <div className="page-head">
        <h1>Overview</h1>
        <p className="muted">Every machine, live. Choose one to see its readings, history and faults.</p>
      </div>
      <div className="tiles summary-tiles">
        {tiles.map((t) => (
          <div key={t.label} className={`tile ${t.cls}`}>
            <span className="label">{t.label}</span>
            <span className="num">{t.n}</span>
          </div>
        ))}
      </div>
      {ms.length === 0 && <p className="muted">No machines are registered yet. The Administrator can add them on the Admin page.</p>}
      {GROUPS.map(([type, title]) => {
        const list = ms.filter((m) => m.type === type)
        if (list.length === 0) return null
        return (
          <section className="group" key={type}>
            <div className="group-head"><h2>{title}</h2><span className="muted">{list.length}</span></div>
            <div className="cards">{list.map((m) => <MachineCard key={m.id} machine={m} />)}</div>
          </section>
        )
      })}
    </div>
  )
}
