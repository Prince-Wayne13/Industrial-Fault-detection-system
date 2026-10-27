// Words and units shown on the dashboard. One place, so a wording change (for example warning -> abnormal) is one edit.
// Open item: "warning" and "abnormal" mean the same first level. Both are kept until the SRS wording is settled.
export const STATUS_LABEL = { normal: 'Normal', warning: 'Warning', abnormal: 'Abnormal', critical: 'Critical', unknown: 'Waiting' }

export const RANK = { unknown: -1, normal: 0, abnormal: 1, warning: 1, critical: 2 }

export const UNITS = { temperature: '°C', current: 'A', vibration: 'mm/s', rpm: 'rpm', fan_rpm: 'rpm' }
const DECIMALS = { temperature: 1, current: 1, vibration: 2, rpm: 0, fan_rpm: 0 }

export const PARAM_LABEL = {
  motor: { temperature: 'Temperature', current: 'Current', vibration: 'Vibration', rpm: 'Speed' },
  pump: { temperature: 'Bearing temp.', current: 'Current', vibration: 'Vibration', rpm: 'Speed' },
  ups: { temperature: 'Internal temp.', current: 'Current', fan_rpm: 'Fan speed' },
}

export function formatValue(parameter, value) {
  return typeof value === 'number' ? value.toFixed(DECIMALS[parameter] ?? 1) : '—'
}

export function worst(parameters) {
  return Object.values(parameters).reduce((w, p) => (RANK[p.status] > RANK[w] ? p.status : w), 'unknown')
}
