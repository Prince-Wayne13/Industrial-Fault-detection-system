"""Proof for the demonstration. Segment 5.
The requirements tracker (every requirement: built, simulated, left-out or not-set), the check script runner, and the measured
numbers: NFR-1, NFR-2 accuracy, NFR-5 uptime, PR-001/PR-001a alert time, PR-002 reading time, PR-003 machines, PR-004 viewers,
PR-005 readings per second, PR-006 storage, PR-007 start-up time."""
import json
import pathlib
import re
import subprocess
import sys
import threading
import time

import clock
import config
import model

HERE = pathlib.Path(__file__).parent
REQ_DIR = HERE.parents[1] / "docs" / "design" / "requirements"
OVERRIDES = HERE / "tracker_status.json"
REPORT = HERE / "check_report.md"
_ROW = re.compile(r"^\| (\S+) \| (PASS|FAIL|SEGMENT \d+) \| (.*?) \| (.*) \|$")


def _results():
    out = {}
    if REPORT.exists():
        for line in REPORT.read_text(encoding="utf-8").splitlines():
            m = _ROW.match(line)
            if m:
                out[m.group(1)] = {"result": m.group(2), "title": m.group(3), "detail": m.group(4)}
    return out


def _sort_key(item):
    m = re.match(r"([A-Z]+)-(\d+)(.*)", item["id"])
    return ({"FR": 0, "NFR": 1, "PR": 2}.get(m.group(1), 3), int(m.group(2)), m.group(3)) if m else (9, 0, item["id"])


def requirements():
    results = _results()
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    out = []
    for path in REQ_DIR.glob("*.md"):
        if path.stem.startswith("UC-"):
            continue
        text = path.read_text(encoding="utf-8")
        meta, body = {}, text
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = m.group(2)
        paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
        res = results.get(path.stem, {})
        ov = overrides.get(path.stem, {})
        set_status = meta.get("status") if meta.get("status") not in (None, "not-set") else None
        status = ov.get("status") or set_status or ("built" if res.get("result") == "PASS" else "not-set")
        out.append({"id": path.stem, "statement": paras[0] if paras else "", "status": status, "result": res.get("result", ""),
                    "checked": res.get("title", ""), "note": ov.get("note") or res.get("detail", "")})
    return sorted(out, key=_sort_key)


# ---- the check script, run in its own process so it cannot touch the live clock ----
_check = {"running": False, "started": None, "finished": None, "returncode": None, "output": ""}


def start_checks():
    if _check["running"]:
        return False

    def work():
        _check.update(running=True, started=clock.real(), finished=None, returncode=None, output="")
        try:
            r = subprocess.run([sys.executable, "check_all.py"], cwd=HERE, capture_output=True, text=True, timeout=900)
            _check.update(returncode=r.returncode, output=(r.stdout + r.stderr)[-4000:])
        except Exception as e:
            _check.update(returncode=-1, output=str(e))
        _check.update(running=False, finished=clock.real())

    _check["running"] = True
    threading.Thread(target=work, daemon=True).start()
    return True


def checks_status():
    return dict(_check)


# ---- measured numbers ----
_accuracy = {"state": "idle", "value": None}


def _compute_accuracy():
    _accuracy["state"] = "running"
    try:
        _accuracy["value"] = {k: {"right": r, "of": n, "percent": round(100 * r / n, 1) if n else None}
                              for k, (r, n) in model.evaluate().items()}
        _accuracy["state"] = "done"
    except Exception as e:
        _accuracy.update(state="failed", value=str(e))


def metrics(feed, viewers, peak):
    """Call with feed.lock held."""
    if _accuracy["state"] == "idle":
        threading.Thread(target=_compute_accuracy, daemon=True).start()
    s = feed.system
    now = clock.real()
    up = now - feed.started
    counts = s.engine.counts
    lat = [f["alert_latency_s"] for f in s.faults.faults.values()]
    n = feed.latency["n"]
    return {
        "uptime_s": round(up, 1),
        "startup_s": round(feed.ready_at - feed.started, 2) if feed.ready_at else None,
        "viewers": viewers, "peak_viewers": peak,
        "machines": len(s.machines),
        "readings_received": counts["received"], "readings_invalid": counts["invalid"],
        "readings_per_s": round(counts["received"] / up, 1) if up else 0,
        "reading_ms_avg": round(feed.latency["sum"] / n, 2) if n else None, "reading_ms_max": round(feed.latency["max"], 2),
        "status_window_s": config.WINDOW_S, "windows": counts["windows"],
        "alerts": len(lat), "alert_s_avg": round(sum(lat) / len(lat), 3) if lat else None, "alert_s_max": max(lat) if lat else None,
        "alerts_delayed": sum(1 for f in s.faults.faults.values() if f["delayed"]),
        "storage_used": round(s.store.local.used_fraction(), 5), "storage_cap_mb": config.LOCAL_STORAGE_CAP_MB,
        "accuracy": _accuracy,
    }
