"""Two stores, written at the same time. Step 6.

  Local storage: a SQLite file with a set size (LOCAL_STORAGE_CAP_MB). When it is full, writes fail for real.
  Online database: PostgreSQL if DATABASE_URL is set; otherwise a second SQLite file stands in for it.

FR-9, FR-9a, FR-9b, FR-12, FR-20, FR-21, FR-21a, NFR-6, NFR-10, PR-006
"""
import json
import sqlite3
from config import LOCAL_DB_PATH, LOCAL_STORAGE_CAP_MB, ONLINE_FALLBACK_PATH, STORAGE_ALERT_AT

PAGE = 4096
SCHEMA = """CREATE TABLE IF NOT EXISTS windows (
    machine_id TEXT, parameter TEXT, start_time REAL, status TEXT, readings TEXT)"""


class LocalStore:
    def __init__(self, path=LOCAL_DB_PATH, cap_mb=LOCAL_STORAGE_CAP_MB):
        self.cap_pages = cap_mb * 1024 * 1024 // PAGE
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.execute(f"PRAGMA page_size={PAGE}")
        self.con.execute(f"PRAGMA max_page_count={self.cap_pages}")   # the set size: the file cannot grow past it
        self.con.execute(SCHEMA)
        self.con.commit()

    def used_fraction(self):
        """Used space as a share of the set size. Free pages inside the file do not count. FR-21a."""
        pages = self.con.execute("PRAGMA page_count").fetchone()[0]
        free = self.con.execute("PRAGMA freelist_count").fetchone()[0]
        return (pages - free) / self.cap_pages

    def at_alert_level(self):
        return self.used_fraction() >= STORAGE_ALERT_AT

    def save_window(self, window):
        """Return True if saved, False if the store is full. The caller logs it and keeps the data. FR-20."""
        try:
            self.con.execute("INSERT INTO windows VALUES (?,?,?,?,?)",
                             (window["machine_id"], window["parameter"], window["start_time"],
                              window["status"], json.dumps(window.get("readings", []))))
            self.con.commit()
            return True
        except sqlite3.OperationalError:
            return False


class OnlineStore:
    """PostgreSQL when DATABASE_URL is set. The demo can cut the link with set_available(False). FR-12."""
    def __init__(self):
        self.available = True
        self.con = sqlite3.connect(ONLINE_FALLBACK_PATH, check_same_thread=False)   # TODO step 6: PostgreSQL
        self.con.execute(SCHEMA)
        self.con.commit()

    def set_available(self, value):
        self.available = value

    def save_window(self, window):
        if not self.available:
            return False
        self.con.execute("INSERT INTO windows VALUES (?,?,?,?,?)",
                         (window["machine_id"], window["parameter"], window["start_time"],
                          window["status"], json.dumps(window.get("readings", []))))
        self.con.commit()
        return True


def delete_old_normal_readings():
    """FR-9b: readings of normal windows go after 24 hours. Statuses and warning or critical records stay."""
    raise NotImplementedError("step 6")
