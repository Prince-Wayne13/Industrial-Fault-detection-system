// Overview. Requirements: FR-1, FR-2, FR-3, FR-13, FR-14, FR-24, NFR-8, PR-001, PR-002, PR-001b
import MachineCard from './MachineCard.jsx'
import { useOverview } from './useLive.js'

const GROUPS = [['motor', 'Motors'], ['pump', 'Water pumps'], ['ups', 'Backup power']]

export default function Overview() {
  const { data, connected } = useOverview()
  if (!data) return <div className="page"><h1>Overview</h1><p className="muted">Connecting to the server…</p></div>
  return (
    <div className="page">
      {!connected && <div className="notice notice-lost">Live connection lost. The numbers below may be old. Trying again…</div>}
      {data.link === 'cut' && (
        <div className="notice notice-delayed">Connection to the online database is cut. Readings are still collected and shown here; {data.pending} saved windows will be sent when it returns.</div>
      )}
      {data.alerts_delayed && <div className="notice notice-delayed">Alerts delayed: a fault alert came more than 2 seconds late.</div>}
      <h1>Overview</h1>
      {data.machines.length === 0 && (
        <p className="muted">No machines are registered yet. The Administrator can add them on the Admin page.</p>
      )}
      {GROUPS.map(([type, title]) => {
        const list = data.machines.filter((m) => m.type === type)
        if (list.length === 0) return null
        return (
          <section key={type}>
            <h2 className="group-title">{title}</h2>
            <div className="card-grid">{list.map((m) => <MachineCard key={m.id} machine={m} />)}</div>
          </section>
        )
      })}
    </div>
  )
}
