"""The status model. Threshold screening, then the 10-second trend check, then the classifier.
FR-4, FR-5, FR-6, NFR-1, NFR-2, NFR-9. One parameter's logic can change without touching the others."""
from config import LIMITS


def threshold_level(machine_type, parameter, value):
    """Return "normal", "warning", "critical" or "abnormal" for ONE reading. FR-4."""
    rule = LIMITS.get(machine_type, {}).get(parameter, {})
    if rule.get("critical") is not None and value > rule["critical"]:
        return "critical"
    if rule.get("warning") is not None and value > rule["warning"]:
        return "warning"
    if rule.get("abnormal") is not None and value > rule["abnormal"]:
        return "abnormal"
    if rule.get("abnormal_below") is not None and value < rule["abnormal_below"]:
        return "abnormal"
    return "normal"


def trend_check(levels):
    """levels = the threshold level of each clean reading in the 10-second window.
    A fault needs the abnormal condition to hold across the window, never one reading alone. FR-6."""
    if not levels:
        return "normal"
    # TODO step 4: decide how much of the window must be abnormal. Starting rule: all of it.
    order = ["normal", "abnormal", "warning", "critical"]
    worst_common = min(levels, key=order.index)
    return worst_common


def classify(machine_type, parameter, window_values):
    """The classifier sets the final status for the window. FR-5.
    TODO step 10: train a logistic regression on the labelled simulated set (SRS Appendix D, NFR-1, NFR-2)."""
    levels = [threshold_level(machine_type, parameter, v) for v in window_values]
    return trend_check(levels)
