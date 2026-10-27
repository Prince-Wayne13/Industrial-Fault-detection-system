// Turns a raw log line into plain words. The server keeps who, when, what, old and new; this makes them readable.
import { UNITS } from './status.js'

const FIELDS = { warning: 'Warning above', critical: 'Critical above', abnormal: 'Abnormal above', abnormal_below: 'Abnormal below' }
const PARAM = { rpm: 'Speed', fan_rpm: 'Fan speed' }
const cap = (w) => (w ? w[0].toUpperCase() + w.slice(1) : w)
export const paramLabel = (p) => PARAM[p] ?? cap(p)

export const logTime = (t) => new Date(t * 1000).toLocaleString([], { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })

export const KINDS = [
  ['all', 'All'], ['limit', 'Limits'], ['acknowledge', 'Acknowledged'], ['resolve', 'Resolved'], ['people', 'Users and machines'],
]

// Returns { kind, action, details: [{ label, text, tone }] }. tone is 'changed', 'added', 'removed' or 'same'.
export function describe(entry, names = {}) {
  const [verb, ...rest] = entry.what.split(' ')
  const fault = entry.new && typeof entry.new === 'object' ? entry.new : {}
  if (verb === 'limit') {
    const [target, parameter] = rest
    const unit = UNITS[parameter] ? ` ${UNITS[parameter]}` : ''
    const old = entry.old ?? {}
    const now = entry.new ?? {}
    const details = Object.keys(FIELDS).filter((k) => k in old || k in now).map((k) => {
      const label = FIELDS[k]
      if (k in old && k in now) return old[k] === now[k] ? { label, text: `${now[k]}${unit}`, tone: 'same' } : { label, text: `${old[k]} → ${now[k]}${unit}`, tone: 'changed' }
      if (k in now) return { label, text: `added: ${now[k]}${unit}`, tone: 'added' }
      return { label, text: `${old[k]}${unit} → not necessary`, tone: 'removed' }
    })
    return { kind: 'limit', action: `Changed the ${paramLabel(parameter).toLowerCase()} limits of ${names[target] ?? target}`, details }
  }
  if (verb === 'acknowledge' || verb === 'resolve') {
    const machine = names[fault.machine] ?? fault.machine
    return {
      kind: verb,
      action: `${verb === 'acknowledge' ? 'Acknowledged' : 'Resolved'} a fault on ${machine}`,
      details: [{ label: 'Fault', text: `#${fault.fault} · ${paramLabel(fault.parameter)} · ${fault.level}`, tone: 'same' }],
    }
  }
  if (verb === 'add' && rest[0] === 'user') return { kind: 'people', action: `Added the user ${rest[1]}`, details: [{ label: 'Role', text: entry.new?.role ?? '', tone: 'same' }] }
  if (verb === 'remove' && rest[0] === 'user') return { kind: 'people', action: `Removed the user ${rest[1]}`, details: [] }
  if (verb === 'register') return { kind: 'people', action: `Registered the machine ${rest[1]}`, details: [{ label: 'Type', text: String(entry.new ?? ''), tone: 'same' }] }
  if (verb === 'remove' && rest[0] === 'machine') return { kind: 'people', action: `Removed the machine ${rest[1]}`, details: [] }
  return { kind: 'other', action: entry.what, details: [] }
}
