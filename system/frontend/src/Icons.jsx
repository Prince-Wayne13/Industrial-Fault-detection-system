// Small line icons, drawn here so no icon package is needed.
const P = {
  mark: <><path d="M3 12h4l2.5-6 4 12 2.5-6H21" /></>,
  grid: <><rect x="3" y="3" width="7" height="7" rx="1.5" /><rect x="14" y="3" width="7" height="7" rx="1.5" /><rect x="3" y="14" width="7" height="7" rx="1.5" /><rect x="14" y="14" width="7" height="7" rx="1.5" /></>,
  list: <><path d="M8 6h13M8 12h13M8 18h13" /><circle cx="4" cy="6" r="1" /><circle cx="4" cy="12" r="1" /><circle cx="4" cy="18" r="1" /></>,
  shield: <><path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z" /><path d="M9 12l2 2 4-4" /></>,
  sliders: <><path d="M4 7h9M17 7h3M4 17h3M11 17h9" /><circle cx="15" cy="7" r="2" /><circle cx="9" cy="17" r="2" /></>,
  play: <><circle cx="12" cy="12" r="9" /><path d="M10 8.5l5 3.5-5 3.5z" /></>,
  check: <><path d="M9 6h11M9 12h11M9 18h11" /><path d="M3.5 6l1.2 1.2L7 5M3.5 12l1.2 1.2L7 11M3.5 18l1.2 1.2L7 17" /></>,
  search: <><circle cx="11" cy="11" r="7" /><path d="M20 20l-3.5-3.5" /></>,
  bell: <><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a2 2 0 0 0 3.4 0" /></>,
  bluetooth: <><path d="M7 7l10 10-5 5V2l5 5L7 17" /></>,
  wifi: <><path d="M5 12.5a10 10 0 0 1 14 0" /><path d="M1.5 9a15 15 0 0 1 21 0" /><path d="M8.5 16a5.5 5.5 0 0 1 7 0" /><circle cx="12" cy="19.5" r="1" /></>,
  chevron: <><path d="M6 9l6 6 6-6" /></>,
  close: <><path d="M6 6l12 12M18 6L6 18" /></>,
  motor: <><circle cx="12" cy="12" r="7.5" /><circle cx="12" cy="12" r="2.5" /><path d="M12 4.5v5M12 14.5v5M4.5 12h5M14.5 12h5" /></>,
  pump: <><path d="M12 3s-6.5 7-6.5 11.2a6.5 6.5 0 0 0 13 0C18.5 10 12 3 12 3z" /><path d="M9 14.5a3 3 0 0 0 3 3" /></>,
  ups: <><rect x="3" y="7" width="16" height="10" rx="2" /><path d="M21 10.5v3" /><path d="M11.5 9.5l-2 3h3l-2 3" /></>,
  logout: <><path d="M9 4H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h4" /><path d="M16 8l4 4-4 4M20 12H9" /></>,
}

export default function Icon({ name, size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
         strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      {P[name]}
    </svg>
  )
}
