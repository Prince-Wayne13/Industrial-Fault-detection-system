"""The checker. Every reading passes through here before the status model. FR-14, NFR-7."""
from config import PHYSICAL_RANGE


def check_reading(reading):
    """Return (True, "") if the reading is clean, otherwise (False, reason).

    A reading is a dict: {"machine_id", "parameter", "value", "time"}.
    A bad reading is kept out, logged as invalid, and the system carries on.
    """
    value = reading.get("value")
    if value is None:
        return False, "missing"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False, "wrong type"
    if value != value:
        return False, "not a number"
    low, high = PHYSICAL_RANGE.get(reading.get("parameter"), (None, None))
    if low is not None and not (low <= value <= high):
        return False, "impossible value"
    return True, ""
