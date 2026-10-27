"""The status model. Threshold screening, then the 10-second trend check, then the classifier.
FR-4, FR-5, FR-6, NFR-1, NFR-2, NFR-9. One parameter's logic can change without touching the others (limits live in config).

Statuses: normal, warning, critical for parameters with two limits; normal, abnormal for every other parameter (FR-5)."""
import random

import config
from config import RANK

_CLF = None
_CLF_TRIED = False


def rule_for(machine_type, parameter):
    return config.LIMITS.get(machine_type, {}).get(parameter, {})


def levels_for(machine_type, parameter):
    """The statuses this parameter can have."""
    r = rule_for(machine_type, parameter)
    if r.get("warning") is not None or r.get("critical") is not None:
        return ("normal", "warning", "critical")
    if r.get("abnormal") is not None or r.get("abnormal_below") is not None:
        return ("normal", "abnormal")
    return ("normal",)


def threshold_level(machine_type, parameter, value):
    """Screening of ONE reading: 'normal', 'warning', 'critical' or 'abnormal'. FR-4."""
    r = rule_for(machine_type, parameter)
    if r.get("critical") is not None and value > r["critical"]:
        return "critical"
    if r.get("warning") is not None and value > r["warning"]:
        return "warning"
    if r.get("abnormal") is not None and value > r["abnormal"]:
        return "abnormal"
    if r.get("abnormal_below") is not None and value < r["abnormal_below"]:
        return "abnormal"
    return "normal"


def limit_in_force(machine_type, parameter, level, value=None):
    """The number that was crossed. Stored on the fault record. FR-23d."""
    r = rule_for(machine_type, parameter)
    if level in ("warning", "critical"):
        return r.get(level)
    if r.get("abnormal") is not None and (value is None or value > r["abnormal"]):
        return r["abnormal"]
    return r.get("abnormal_below")


def fluctuation(machine_type, parameter, values):
    """FR-4 / SRS A.4 'fluctuating'. The typical step from one reading to the next, as a share of the mean (median of the 9 steps).
    A swing steps by a lot every second; one spike, one ramp or plain noise leave the median step small, so FR-6 still holds."""
    if rule_for(machine_type, parameter).get("fluctuation_step") is None or len(values) < 4:
        return None
    mean = sum(values) / len(values)
    if mean == 0:
        return None
    steps = sorted(abs(b - a) for a, b in zip(values, values[1:]))
    n = len(steps)
    med = steps[n // 2] if n % 2 else (steps[n // 2 - 1] + steps[n // 2]) / 2
    return med / abs(mean)


def is_fluctuating(machine_type, parameter, values):
    cv = fluctuation(machine_type, parameter, values)
    return cv is not None and cv > rule_for(machine_type, parameter)["fluctuation_step"]


def observed_value(machine_type, parameter, values):
    """The reading furthest past the limit, for the pop-up ('138 C now')."""
    if not values:
        return None
    r = rule_for(machine_type, parameter)
    if r.get("abnormal_below") is not None and min(values) < r["abnormal_below"] and not any(v > (r.get("abnormal") or r.get("warning") or float("inf")) for v in values):
        return min(values)
    return max(values)


def trend_check(levels, fraction=None):
    """levels = the screening level of each clean reading in the 10-second window.
    The window gets the highest level that at least `fraction` of its readings reach. One reading alone never does. FR-6."""
    fraction = config.TREND_FRACTION if fraction is None else fraction
    if not levels:
        return "normal"
    n = len(levels)
    for lv in sorted(set(levels), key=lambda x: RANK[x], reverse=True):
        if lv == "normal":
            return "normal"
        share = sum(1 for x in levels if RANK[x] >= RANK[lv]) / n
        if share >= fraction:
            return lv
    return "normal"


def _features(machine_type, parameter, values):
    ranks = [RANK[threshold_level(machine_type, parameter, v)] for v in values]
    n = len(ranks)
    return [sum(r >= 1 for r in ranks) / n, sum(r >= 2 for r in ranks) / n, min(ranks) / 2, max(ranks) / 2]


def _train():
    """Logistic regression on the labelled set made from seed data. Classes: 0 normal, 1 first level, 2 critical."""
    global _CLF, _CLF_TRIED
    _CLF_TRIED = True
    try:
        from sklearn.linear_model import LogisticRegression
    except ImportError:
        return None
    import seed
    rows = seed.labelled_windows(random.Random(1), per_case=30)
    x = [_features(w["machine_type"], w["parameter"], w["values"]) for w in rows]
    y = [{"normal": 0, "warning": 1, "abnormal": 1, "critical": 2}[w["truth"]] for w in rows]
    _CLF = LogisticRegression(max_iter=2000).fit(x, y)
    return _CLF


def classify(machine_type, parameter, window_values):
    """The final status for one parameter for one window. FR-5.
    1. Screening and the trend check decide whether anything is flagged at all (FR-4, FR-6).
    2. Only a flagged window goes to the classifier, which assigns the level (DD-05)."""
    allowed = levels_for(machine_type, parameter)
    levels = [threshold_level(machine_type, parameter, v) for v in window_values]
    rule_level = trend_check(levels)
    if rule_level == "normal" and is_fluctuating(machine_type, parameter, window_values) and "abnormal" in allowed:
        return "abnormal"                      # a steady spread over the whole window counts, one wild reading does not (std needs all 10)
    if rule_level == "normal":
        return "normal"
    clf = _CLF if _CLF_TRIED else _train()
    if clf is None:
        return rule_level
    cls = int(clf.predict([_features(machine_type, parameter, window_values)])[0])
    if cls == 0:
        return rule_level
    if cls == 2 and "critical" in allowed:
        return "critical"
    return "warning" if "warning" in allowed else "abnormal"


def evaluate(seed_value=2, per_case=40):
    """NFR-1 and NFR-2: run the labelled set and count what was found. Uses a different random seed from training."""
    import seed
    rows = seed.labelled_windows(random.Random(seed_value), per_case=per_case)
    crit = [w for w in rows if w["truth"] == "critical" and w["parameter"] in ("temperature", "current")]
    vib = [w for w in rows if w["truth"] != "normal" and w["parameter"] == "vibration"]
    everything = rows

    def right(ws):
        return sum(1 for w in ws if classify(w["machine_type"], w["parameter"], w["values"]) == w["truth"])

    return {"critical_temp_current": (right(crit), len(crit)), "vibration": (right(vib), len(vib)),
            "all_windows": (right(everything), len(everything))}
