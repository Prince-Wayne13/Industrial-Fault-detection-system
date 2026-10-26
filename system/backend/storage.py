"""Two stores, written at the same time. Step 1.5.

  Local storage: a SQLite file with a set size (LOCAL_STORAGE_CAP_MB). When it is full, writes fail for real.
  Online database: PostgreSQL if DATABASE_URL is set; otherwise a second SQLite file stands in for it (marked simulated on the tracker).

FR-9, FR-9a, FR-9b, FR-12, FR-20, FR-21, FR-21a, NFR-6, NFR-10, PR-006
"""
import json
import sqlite3

import clock
import config

PAGE = 4096
SCHEMA = [
    "CREATE TABLE IF NOT EXISTS windows (machine_id TEXT, parameter TEXT, start_time REAL, status TEXT, n INTEGER, readings TEXT)",
    "CREATE TABLE IF NOT EXISTS faults (id INTEGER PRIMARY KEY, data TEXT)",
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)",
]


def _row(window):
    return (window["machine_id"], window["parameter"], window["start_time"], window["status"],
            window.get("n", len(window.get("readings", []))), json.dumps(window.get("readings", [])))


class LocalStore:
    """The local copy. Size is fixed: the file cannot grow past it."""

    def __init__(self, path=None, cap_mb=None):
        path = config.LOCAL_DB_PATH if path is None else path
        cap_mb = config.LOCAL_STORAGE_CAP_MB if cap_mb is None else cap_mb
        self.cap_pages = int(cap_mb * 1024 * 1024 // PAGE)
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.execute(f"PRAGMA page_size={PAGE}")
        for ddl in SCHEMA:
            self.con.execute(ddl)
        self.con.commit()
        self.con.execute(f"PRAGMA max_page_count={self.cap_pages}")   # the set size

    def used_fraction(self):
        """Used space as a share of the set size. Free pages inside the file do not count. FR-21a."""
        pages = self.con.execute("PRAGMA page_count").fetchone()[0]
        free = self.con.execute("PRAGMA freelist_count").fetchone()[0]
        return (pages - free) / self.cap_pages

    def at_alert_level(self):
        return self.used_fraction() >= config.STORAGE_ALERT_AT

    def _write(self, sql, params):
        try:
            self.con.execute(sql, params)
            self.con.commit()
            return True
        except sqlite3.OperationalError:      # "database or disk is full"
            self.con.rollback()
            return False

    def save_window(self, window):
        """True if saved, False if the store is full. The caller logs it and keeps the data. FR-20."""
        return self._write("INSERT INTO windows VALUES (?,?,?,?,?,?)", _row(window))

    def save_fault(self, fault):
        return self._write("INSERT OR REPLACE INTO faults VALUES (?,?)", (fault["id"], json.dumps(fault)))

    def faults(self):
        return [json.loads(d) for (d,) in self.con.execute("SELECT data FROM faults ORDER BY id")]

    def put_setting(self, key, value):
        return self._write("INSERT OR REPLACE INTO settings VALUES (?,?)", (key, json.dumps(value)))

    def get_setting(self, key, default=None):
        r = self.con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return json.loads(r[0]) if r else default

    def count_windows(self):
        return self.con.execute("SELECT COUNT(*) FROM windows").fetchone()[0]

    def count_readings(self):
        """Readings that went into saved windows. The count survives the 24-hour clean-up."""
        return self.con.execute("SELECT COALESCE(SUM(n),0) FROM windows").fetchone()[0]

    def count_kept_readings(self):
        return sum(len(json.loads(r)) for (r,) in self.con.execute("SELECT readings FROM windows"))

    def windows(self, machine_id=None, status=None):
        q, a = "SELECT machine_id, parameter, start_time, status, n, readings FROM windows WHERE 1=1", []
        if machine_id:
            q += " AND machine_id=?"; a.append(machine_id)
        if status:
            q += " AND status=?"; a.append(status)
        return [{"machine_id": m, "parameter": p, "start_time": s, "status": st, "n": n, "readings": json.loads(r)}
                for m, p, s, st, n, r in self.con.execute(q + " ORDER BY start_time", a)]

    def cleanup_normal(self, before):
        """FR-9b: the readings of normal windows older than `before` go. The status and time stamp stay (FR-9a).
        Warning, critical and abnormal windows are never touched (NFR-10)."""
        cur = self.con.execute("UPDATE windows SET readings='[]' WHERE status='normal' AND start_time<? AND readings!='[]'", (before,))
        self.con.commit()
        return cur.rowcount


class OnlineStore:
    """PostgreSQL when DATABASE_URL is set, otherwise a second SQLite file (simulated). The demo can cut the link
    with set_available(False). FR-12. The PostgreSQL branch needs a running server to try; the SQLite branch is what the checks use."""

    def __init__(self, url=None, fallback_path=None):
        url = config.DATABASE_URL if url is None else url
        self.available = True
        self.simulated = not url
        if url:
            import psycopg2
            self.pg = True
            self.con = psycopg2.connect(url)
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS windows (machine_id TEXT, parameter TEXT, start_time DOUBLE PRECISION, status TEXT, n INTEGER, readings TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS faults (id INTEGER PRIMARY KEY, data TEXT)")
            self.con.commit()
        else:
            self.pg = False
            self.con = sqlite3.connect(config.ONLINE_FALLBACK_PATH if fallback_path is None else fallback_path, check_same_thread=False)
            for ddl in SCHEMA:
                self.con.execute(ddl)
            self.con.commit()

    def set_available(self, value):
        self.available = value

    def _run(self, sql, params=()):
        cur = self.con.cursor()
        cur.execute(sql.replace("?", "%s") if self.pg else sql, params)
        return cur

    def save_window(self, window):
        if not self.available:
            return False
        try:
            self._run("INSERT INTO windows VALUES (?,?,?,?,?,?)", _row(window))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    def save_fault(self, fault):
        if not self.available:
            return False
        try:
            if self.pg:
                self._run("INSERT INTO faults VALUES (?,?) ON CONFLICT (id) DO UPDATE SET data=EXCLUDED.data", (fault["id"], json.dumps(fault)))
            else:
                self._run("INSERT OR REPLACE INTO faults VALUES (?,?)", (fault["id"], json.dumps(fault)))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    def count_readings(self):
        return self._run("SELECT COALESCE(SUM(n),0) FROM windows").fetchone()[0]

    def cleanup_normal(self, before):
        cur = self._run("UPDATE windows SET readings='[]' WHERE status='normal' AND start_time<? AND readings!='[]'", (before,))
        self.con.commit()
        return cur.rowcount


class DualStore:
    """Writes every window and fault to both stores. Catches a full local store and a cut online link. FR-12, FR-20, NFR-6."""

    def __init__(self, local=None, online=None):
        self.local = local or LocalStore()
        self.online = online or OnlineStore()
        self.events = []             # the log of storage events (FR-20)
        self.admin_alerts = []       # the storage alert goes to the Administrator only (FR-21a)
        self.temp_buffer = []        # new windows kept in memory while the local store is full (FR-20)
        self.pending_online = []     # windows the online database has not received yet (FR-12)
        self._alerted = False
        self._outage_logged = False

    def _event(self, kind, detail=""):
        self.events.append({"time": clock.now(), "kind": kind, "detail": detail})

    def save_window(self, window):
        ok = self.local.save_window(window)
        if not ok:
            self.temp_buffer.append(window)
            self._event("local_store_full", f"{window['machine_id']} {window['parameter']} kept in temporary storage")
        if not self.online.save_window(window):
            self.pending_online.append(window)
            if not self._outage_logged:
                self._outage_logged = True
                self._event("online_unavailable", "keeping data locally until the link returns")
        self._check_alert()
        return ok

    def save_fault(self, fault):
        ok = self.local.save_fault(fault)
        self.online.save_fault(fault)
        if not ok:
            self._event("local_store_full", f"fault {fault['id']} not saved locally")
        return ok

    def restore_online(self):
        """The link is back: send what was collected during the interruption. FR-12."""
        self.online.set_available(True)
        sent = 0
        for w in self.pending_online:
            if self.online.save_window(w):
                sent += 1
        self.pending_online = [] if sent == len(self.pending_online) else self.pending_online[sent:]
        self._outage_logged = False
        self._event("online_restored", f"{sent} windows sent")
        return sent

    def _check_alert(self):
        used = self.local.used_fraction()
        if used >= config.STORAGE_ALERT_AT and not self._alerted:
            self._alerted = True
            self.admin_alerts.append({"to": "administrator", "type": "storage", "used": round(used, 3), "time": clock.now()})
            self._event("storage_75", f"{used:.0%} of the set size is used")

    def cleanup(self):
        """FR-9b. Only the readings of normal windows older than 24 hours go. Nothing else is deleted by the system (NFR-10)."""
        before = clock.now() - config.NORMAL_KEEP_HOURS * 3600
        n = self.local.cleanup_normal(before)
        self.online.cleanup_normal(before)
        moved = 0
        for w in list(self.temp_buffer):          # space may have opened up
            if self.local.save_window(w):
                self.temp_buffer.remove(w)
                moved += 1
        if self.local.used_fraction() < config.STORAGE_ALERT_AT:
            self._alerted = False
        return n
