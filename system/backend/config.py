"""Every setting in one place. The numbers come from the SRS. Change them here only."""
import os
from dotenv import load_dotenv

load_dotenv()

READING_INTERVAL_S = 1         # FR-3a   one reading per second per parameter
WINDOW_S = 10                  # FR-6, PR-001   status is set every 10 seconds
SENSOR_TIMEOUT_S = 3           # FR-13   no reading for 3 seconds = sensor fault
ALERT_LIMIT_S = 2              # PR-001a, PR-001b, PR-002
NORMAL_KEEP_HOURS = 24         # FR-9b   readings of a normal window are deleted after this
STORAGE_ALERT_AT = 0.75        # FR-21a, NFR-10
LOCAL_STORAGE_CAP_MB = int(os.getenv("LOCAL_STORAGE_CAP_MB", "512"))  # placeholder: measure, then decide
LOCAL_DB_PATH = os.getenv("LOCAL_DB_PATH", "local_store.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")
ONLINE_FALLBACK_PATH = "online_store.db"   # used when DATABASE_URL is empty (simulated online database)

SESSION_DEFAULT_MIN = 5        # FR-26
SESSION_MIN_MIN = 1
SESSION_MAX_MIN = 5
LOGIN_MAX_FAILS = 5            # FR-28d
LOGIN_BLOCK_MIN = 15
PASSWORD_MIN_LEN = 15          # FR-28a
PASSWORD_MAX_LEN = 128         # must accept 64 or more

# Limits from Appendix A. None means the SRS gives no number: the team has to decide (see build-plan).
# "warning" and "critical" are levels. "abnormal" is for parameters that only have one abnormal level (FR-5).
LIMITS = {
    "motor": {
        "temperature": {"warning": 130, "critical": 150},
        "current":     {"warning": 31,  "critical": 35},
        "vibration":   {"warning": None, "critical": None},   # SRS: normal below 2.8 mm/s, critical "per ISO 10816-3"
        "rpm":         {"warning": None, "critical": None},
    },
    "pump": {
        "temperature": {"abnormal": 95},                      # bearing temperature
        "current":     {"abnormal": None},
        "vibration":   {"abnormal": 5.0},
        "rpm":         {"abnormal": None},
    },
    "ups": {
        "temperature": {"abnormal": 75},                      # internal temperature
        "current":     {"abnormal": None},
        "fan_rpm":     {"abnormal_below": 1000},
    },
}

# What counts as a physically possible reading (FR-14). These are placeholders for the team to confirm.
PHYSICAL_RANGE = {
    "temperature": (-20, 300),
    "current": (0, 500),
    "vibration": (0, 100),
    "rpm": (0, 10000),
    "fan_rpm": (0, 10000),
}
