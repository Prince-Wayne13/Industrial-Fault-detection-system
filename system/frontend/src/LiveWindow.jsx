// The live 10-second window of one parameter. Requirements: FR-3a, FR-4, FR-5, FR-6, FR-18
// Every reading as it arrives, with its own level, so a spike is seen. The window's status is set when the 10 seconds end.
import { STATUS_LABEL, formatValue } from './status.js'

const SLOT = { normal: 'slot-normal', warning: 'slot-warning', abnormal: 'slot-warning', critical: 'slot-critical' }

function limitText(rule) {
  const parts = []
  if (rule.warning != null) parts.push(`warning above ${rule.warning}`)
  if (rule.critical != null) parts.push(`critical above ${rule.critical}`)
  if (rule.abnormal != null) parts.push(`abnormal above ${rule.abnormal}`)
  if (rule.abnormal_below != null) parts.push(`abnormal below ${rule.abnormal_below}`)
  return parts.join(' · ')
}

function Slots({ items, total, parameter }) {
  return (
    <div className="slots">
      {Array.from({ length: total }, (_, i) => {
        const it = items[i]
        return (
          <div key={i} className={`slot ${it ? SLOT[it.level] ?? 'slot-normal' : 'slot-empty'}`}>
            <span className="slot-n">{i + 1}</span>
            <strong>{it ? formatValue(parameter, it.value) : '·'}</strong>
            {it && it.level !== 'normal' && <span className="slot-flag">{STATUS_LABEL[it.level] ?? it.level}</span>}
          </div>
        )
      })}
    </div>
  )
}

export default function LiveWindow({ machine, parameter, label, unit, rule, fraction }) {
  const p = machine.parameters[parameter]
  if (!p) return null
  const length = p.window?.length ?? 10
  const now = (p.window?.readings ?? []).map(([, value, level]) => ({ value, level }))
  const last = p.last ? p.last.values.map((value, i) => ({ value, level: p.last.levels[i] })) : []
  const over = now.filter((r) => r.level !== 'normal').length
  const lastOver = last.filter((r) => r.level !== 'normal').length
  const rule_text = fraction >= 1 ? 'Every reading in a window must be over a limit before the window is flagged.' : `At least ${Math.round(fraction * 100)}% of a window must be over a limit before it is flagged.`

  return (
    <div className="card">
      <div className="card-head">
        <h3>{label} {unit && <span className="unit">({unit})</span>} · this 10-second window</h3>
        <span className="muted">{now.length} of {length} seconds</span>
      </div>
      <div className="bar" role="img" aria-label={`${now.length} of ${length} seconds`}><div className="bar-fill" style={{ width: `${(now.length / length) * 100}%` }} /></div>
      <Slots items={now} total={length} parameter={parameter} />
      <p className="muted">
        {over > 0 ? `${over} of ${now.length} readings so far are over a limit. ` : 'No reading so far is over a limit. '}
        The status is set when the 10 seconds end. {rule_text}
      </p>

      <div className="card-head top-gap">
        <h3>Last window</h3>
        {p.last && <span className={`badge ${p.last.status}`}>{STATUS_LABEL[p.last.status] ?? p.last.status}</span>}
      </div>
      {p.last ? (
        <>
          <Slots items={last} total={Math.max(length, last.length)} parameter={parameter} />
          {lastOver > 0 && p.last.status === 'normal' && <p className="muted">{lastOver} reading{lastOver > 1 ? 's were' : ' was'} over a limit, but not enough of the window: the status stayed Normal.</p>}
        </>
      ) : <p className="muted">The first window ends within 10 seconds of the server starting.</p>}
      {limitText(rule) && <p className="muted">Limits: {limitText(rule)}</p>}
    </div>
  )
}
