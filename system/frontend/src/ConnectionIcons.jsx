// Bluetooth (near) and Wi-Fi (remote). FR-11. Three looks: active (blue glow), available, offline (grey, slashed).
// The server decides the mode (Demo page: Near / Remote). Cutting the link puts both offline (FR-12).
import Icon from './Icons.jsx'
import { linkWord } from './connection.js'

function stateFor(mode, link) {
  if (!mode) return { bluetooth: 'offline', wifi: 'offline', offline: true }
  if (link === 'cut') return { bluetooth: 'offline', wifi: 'offline', offline: true }
  return mode === 'remote'
    ? { bluetooth: 'available', wifi: 'active', offline: false }
    : { bluetooth: 'active', wifi: 'available', offline: false }
}

export default function ConnectionIcons({ mode, link }) {
  const s = stateFor(mode, link)
  const one = (name) => (
    <span className={`icon-btn link ${s[name]}`} role="img" aria-label={linkWord(name, s[name])} title={linkWord(name, s[name])}>
      <Icon name={name} />
      {s[name] === 'offline' && <span className="slash" />}
    </span>
  )
  return (
    <div className="links">
      {one('bluetooth')}
      {one('wifi')}
      {s.offline && <span className="offline-word">Offline</span>}
    </div>
  )
}
