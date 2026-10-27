// Which link the dashboard uses. Bluetooth is the near-range link, Wi-Fi the remote one (FR-11).
// Automatic mode prefers Bluetooth. A hand choice never falls back to the other link by itself.
// See design/top-bar.md, "Connection icons".

export const LINK_NAME = { bluetooth: 'Bluetooth', wifi: 'Wi-Fi' }

export function resolveLink(mode, btFound, wifiFound) {
  let active = null
  if (mode === 'bluetooth') active = btFound ? 'bluetooth' : null
  else if (mode === 'wifi') active = wifiFound ? 'wifi' : null
  else active = btFound ? 'bluetooth' : wifiFound ? 'wifi' : null
  const state = (name, found) => (!found ? 'offline' : active === name ? 'active' : 'available')
  return {
    active,
    bluetooth: state('bluetooth', btFound),
    wifi: state('wifi', wifiFound),
    offline: active === null,
  }
}

// The words for hover and screen readers: "Bluetooth: connected", "Wi-Fi: available", "Wi-Fi: offline".
export function linkWord(name, state) {
  return `${LINK_NAME[name]}: ${state === 'active' ? 'connected' : state}`
}
