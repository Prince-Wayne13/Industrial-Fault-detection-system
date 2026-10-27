// The frame around every page after sign in: side nav left, top bar on top, page in the middle, pop-ups bottom right.
import SideNav from './SideNav.jsx'
import TopBar from './TopBar.jsx'
import PopupStack from './PopupStack.jsx'
import InjectionTimer from './InjectionTimer.jsx'

export default function Layout({ faults, overview, machineType, children }) {
  const data = overview
  return (
    <div className="shell">
      <SideNav />
      <div className="main">
        <TopBar bell={faults.bell} storageAlerts={faults.storage_alerts} machines={data?.machines ?? []} mode={data?.mode} link={data?.link} />
        <main className="content">{children}</main>
      </div>
      <PopupStack popups={faults.popups} machineType={machineType} />
      <InjectionTimer scheduled={data?.scheduled} serverTime={data?.time} />
    </div>
  )
}
