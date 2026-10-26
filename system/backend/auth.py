"""Sign in, passwords, roles. Step 7.
FR-26 sign-out time (1 to 5 minutes, each person's own), FR-27 Administrator-only functions, FR-28 sign in first,
FR-28a long passwords, FR-28b no forced mix or schedule, FR-28c refuse common passwords, FR-28d lockout,
FR-28e secure connection (set up when the server starts), FR-28f salted, scrambled passwords."""
import pathlib
import bcrypt
from config import PASSWORD_MIN_LEN, PASSWORD_MAX_LEN

ROLES = ("operator", "engineer", "administrator")
_COMMON = set()
_p = pathlib.Path(__file__).with_name("common-passwords.txt")
if _p.exists():
    _COMMON = {line.strip().lower() for line in _p.read_text(encoding="utf-8").splitlines() if line.strip()}


def password_problem(password):
    """Return a plain message if the password is not allowed, else None."""
    if len(password) < PASSWORD_MIN_LEN:
        return f"Use at least {PASSWORD_MIN_LEN} characters."
    if len(password) > PASSWORD_MAX_LEN:
        return f"Use at most {PASSWORD_MAX_LEN} characters."
    if password.lower() in _COMMON:
        return "That password is too common."
    return None     # no rule about capitals, numbers or symbols (FR-28b)


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)
