import { STATUS_LABEL } from './status.js'

// The status tag from the fault pop-up: a dot and a word, never colour alone.
export default function Pill({ level, children }) {
  return <span className={`pill ${level}`}>{children || STATUS_LABEL[level] || level}</span>
}
