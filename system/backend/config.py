"""Every setting in one place. The numbers come from the SRS and from docs/design/limits-references.md.
Change them here only.

Reference tags used below ([SRS], [R1] ...) are explained in docs/design/limits-references.md.
"""
import copy
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:          # .env support is optional
    pass

READING_INTERVAL_S = 1         # FR-3a   one reading per second per parameter
WINDOW_S = 10                  # FR-6, PR-001   status is set every 10 seconds
SENSOR_TIMEOUT_S = 3           # FR-13   no reading for 3 seconds = sensor fault
ALERT_LIMIT_S = 2              # PR-001a, PR-001b, PR-002
NORMAL_KEEP_HOURS = 24         # FR-9b   readings of a normal window are deleted after this
STORAGE_ALERT_AT = 0.75        # FR-21a, NFR-10
TREND_FRACTION = 0.6           # FR-6   a window counts as a fault when at least this share of it is over a limit. Used to LABEL the training windows (and as the fallback rule if scikit-learn is missing).
STATUS_PROBABILITY = 0.5       # FR-5, FR-6   the model gives each 10-second window a fault score (0 to 100%). At or above this, the window is flagged.
LOCAL_STORAGE_CAP_MB = float(os.getenv("LOCAL_STORAGE_CAP_MB", "512"))   # decision 4: sized in metrics.projected_mb() against PR-006
LOCAL_DB_PATH = os.getenv("LOCAL_DB_PATH", "local_store.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")
ONLINE_FALLBACK_PATH = "online_store.db"   # used when DATABASE_URL is empty (simulated online database)

SESSION_DEFAULT_MIN = 5        # FR-26
SESSION_MIN_MIN = 1
SESSION_MAX_MIN = 5
LOGIN_MAX_FAILS = 5            # FR-28d
LOGIN_BLOCK_MIN = 15
PASSWORD_MIN_LEN = 8           # FR-28a (the team set the minimum at 8 on 27 Oct 2026)
PASSWORD_MAX_LEN = 128         # must accept 64 or more

# Higher number = more serious. "warning" and "abnormal" are the first level; "critical" is the second.
RANK = {"normal": 0, "abnormal": 1, "warning": 1, "critical": 2}

# Rated (nameplate) values of the simulated machines. The rpm and current limits below are fractions of these.
RATED = {
    "motor": {"current": 28, "rpm": 1480},     # [SRS A.1] ~28 A; 4-pole 50 Hz motor, synchronous 1500 rpm [R2]
    "pump":  {"current": 12, "rpm": 1450},
    "ups":   {"current": 5},
}

# Limits. Three statuses (normal, warning, critical) only where the SRS or a standard gives two limits.
# Every other parameter has two statuses: normal and abnormal (FR-5). "abnormal" = abnormal above this value,
# "abnormal_below" = abnormal under this value.
LIMITS = {
    "motor": {
        "temperature": {"warning": 130, "critical": 150},        # [SRS A.1] team-selected
        "current":     {"warning": 31,  "critical": 35},         # [SRS A.1]; 35 A = 125% of 28 A, the usual overload ceiling [R5]
        "vibration":   {"warning": 2.8, "critical": 4.5},        # [R1] ISO 10816-3 / 20816-3, Group 2, rigid support, mm/s RMS: zone B/C and C/D boundaries
        "rpm":         {"abnormal_below": 1332},                 # [SRS A.4] below 90% of rated speed (0.9 x 1480); sync speed [R2]
    },
    "pump": {
        "temperature": {"abnormal": 95},                         # [SRS A.4] bearing temperature
        "current":     {"abnormal": 13.8, "abnormal_below": 9.6},   # 115% of rated = overload [R5]; 80% of rated = underload / dry running [R3][R4]
        # [SRS A.4] normal < 3.0, abnormal > 5.0. Between 3.0 and 5.0 there is no status: one abnormal level only (decision).
        # 3.0 is the expected running level; 5.0 is the single limit. Cross-check: pump guidance puts alert levels near 5.5 mm/s for small pumps [R7].
        "vibration":   {"abnormal": 5.0},
        # [SRS A.4] "dropping or fluctuating". Dropping = below 90% of rated. Fluctuating = the median step between neighbouring readings is above 6% of the mean (normal running about 1.4%, the Noisy readings demo about 3%).
        # Normal running spreads about 1%; 6% leaves room for noise. Team-selected, pending validation.
        "rpm":         {"abnormal_below": 1305, "fluctuation_step": 0.06},
    },
    "ups": {
        "temperature": {"abnormal": 75},                         # [SRS A.3] internal temperature
        "current":     {"abnormal": 5.25},                       # 105% of rated: where UPS makers start their overload clock [R6]
        "fan_rpm":     {"abnormal_below": 1000},                 # [SRS A.3]
    },
}
MACHINE_LIMITS = {}              # machine_id -> parameter -> per-machine rule overrides
DEFAULT_LIMITS = copy.deepcopy(LIMITS)


def reset_limits():
    """Put the limits back to the values above. The dict is changed in place, so every module sees it."""
    LIMITS.clear()
    LIMITS.update(copy.deepcopy(DEFAULT_LIMITS))
    MACHINE_LIMITS.clear()


# What counts as a physically possible reading (FR-14). Decision 2. Anything outside is rejected as invalid.
PHYSICAL_RANGE = {
    "temperature": (-20, 300),     # degrees C
    "current": (0, 500),           # amps
    "vibration": (0, 50),          # mm/s RMS
    "rpm": (0, 3600),              # a 2-pole 60 Hz motor is the fastest case
    "fan_rpm": (0, 10000),
}

# For now the system shows Motor 1 and Motor 2 only (seed.LIVE_MACHINES). Set True to bring back the machine list saved in the database
# (machines an Administrator registered, and the pumps and backup power units).
USE_SAVED_MACHINES = False
