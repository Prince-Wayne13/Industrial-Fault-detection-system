"""History and reports. Segment 3.
FR-9 call up faults and readings, FR-10 everyone views fault history; Operators and Engineers make reports
for a day, week, month or year (full readings only where kept, FR-9b: normal readings go after 24 hours,
so a long graph is built from the windows that remain)."""
import csv
import json
import io
from datetime import datetime, timezone

import clock
from config import RANK

RANGES = {"day": 86400, "week": 7 * 86400, "month": 30 * 86400, "year": 365 * 86400}


def _iso(t):
    return datetime.fromtimestamp(t, tz=timezone.utc).isoformat(timespec="seconds") if t else ""


def history(system, machine_id, parameter, span_s, points=200):
    """Graph data: one point per time bucket, with the mean, the highest value and the worst status. Windows whose
    readings were cleaned up (FR-9b) still count for the status but have no number."""
    since = clock.now() - span_s
    size = span_s / points
    rows = system.store.local.con.execute(
        "SELECT start_time, status, readings FROM windows WHERE machine_id=? AND parameter=? AND start_time>=? ORDER BY start_time",
        (machine_id, parameter, since)).fetchall()
    buckets = {}
    for start, status, readings in rows:
        b = buckets.setdefault(int((start - since) / size), {"t": start, "means": [], "max": None, "status": "normal"})
        values = json.loads(readings)
        if values:
            b["means"].append(sum(values) / len(values))
            b["max"] = max(values) if b["max"] is None else max(b["max"], max(values))
        if RANK.get(status, 0) > RANK.get(b["status"], 0):
            b["status"] = status
    return [{"t": b["t"], "mean": round(sum(b["means"]) / len(b["means"]), 2) if b["means"] else None,
             "max": b["max"], "status": b["status"]} for _, b in sorted(buckets.items())]


def report(system, machine_id=None, span_s=86400):
    """A CSV with three parts: performance (windows per parameter), the faults, and the recurring faults. FR-10."""
    now = clock.now()
    since = now - span_s
    out = io.StringIO()
    w = csv.writer(out)
    names = {i: m["name"] for i, m in system.machines.items()}
    w.writerow(["Fault-Detect report", names.get(machine_id, "All machines"), "from", _iso(since), "to", _iso(now)])
    w.writerow([])
    w.writerow(["PERFORMANCE"])
    w.writerow(["machine", "parameter", "windows", "abnormal windows", "share normal %"])
    q = "SELECT machine_id, parameter, COUNT(*), SUM(status!='normal') FROM windows WHERE start_time>=?"
    args = [since]
    if machine_id:
        q += " AND machine_id=?"
        args.append(machine_id)
    for mid, p, n, bad in system.store.local.con.execute(q + " GROUP BY machine_id, parameter ORDER BY machine_id, parameter", args):
        w.writerow([names.get(mid, mid), p, n, bad or 0, round(100 * (n - (bad or 0)) / n, 1) if n else ""])
    faults = [f for f in system.faults.history(machine_id) if f["raised_at"] >= since]
    w.writerow([])
    w.writerow(["FAULTS"])
    w.writerow(["id", "machine", "parameter", "level", "limit", "raised", "acknowledged by", "resolved by", "resolved", "alert late"])
    for f in sorted(faults, key=lambda f: f["raised_at"]):
        w.writerow([f["id"], names.get(f["machine_id"], f["machine_id"]), f["parameter"], f["level"], f["limit"], _iso(f["raised_at"]),
                    "; ".join(a["user"] for a in f["acknowledged_by"]), f["resolved_by"] or "", _iso(f["resolved_at"]),
                    "yes" if f["delayed"] else "no"])
    counts = {}
    for f in faults:
        counts[(f["machine_id"], f["parameter"])] = counts.get((f["machine_id"], f["parameter"]), 0) + 1
    w.writerow([])
    w.writerow(["RECURRING FAULTS (two or more in the period)"])
    w.writerow(["machine", "parameter", "times"])
    for (mid, p), n in sorted(counts.items(), key=lambda kv: -kv[1]):
        if n >= 2:
            w.writerow([names.get(mid, mid), p, n])
    return out.getvalue()
