"""Sign in, passwords, roles. Step 1.6.
FR-26 sign-out time (1 to 5 minutes, each person's own), FR-27 Administrator-only functions, FR-28 sign in first,
FR-28a long passwords, FR-28b no forced mix or schedule, FR-28c refuse common passwords, FR-28d lockout,
FR-28e secure connection (set up when the server starts, Segment 5), FR-28f salted, scrambled passwords."""
import base64
import hashlib
import math
import pathlib
import secrets
from dataclasses import dataclass

import bcrypt

import clock
from config import (PASSWORD_MIN_LEN, PASSWORD_MAX_LEN, SESSION_DEFAULT_MIN, SESSION_MIN_MIN, SESSION_MAX_MIN,
                    LOGIN_MAX_FAILS, LOGIN_BLOCK_MIN)

ROLES = ("operator", "engineer", "administrator")

# Who may do what (Section 2.3, FR-17, FR-18, FR-23a, FR-27). The Administrator cannot reset passwords and gets no fault alerts.
PERMISSIONS = {
    "operator": {"view_overview", "view_history", "acknowledge", "report"},
    "engineer": {"view_overview", "view_history", "acknowledge", "report", "resolve", "maintenance", "change_limits"},
    "administrator": {"view_overview", "view_history", "manage_users", "manage_machines", "manage_settings", "storage"},
}


def can(role, action):
    return action in PERMISSIONS.get(role, ())


_COMMON = set()
_p = pathlib.Path(__file__).with_name("common-passwords.txt")
if _p.exists():
    _COMMON = {line.strip().lower() for line in _p.read_text(encoding="utf-8").splitlines() if line.strip()}


def password_problem(password):
    """Return a plain message if the password is not allowed, else None."""
    if not isinstance(password, str) or len(password) < PASSWORD_MIN_LEN:
        return f"Use at least {PASSWORD_MIN_LEN} characters."
    if len(password) > PASSWORD_MAX_LEN:
        return f"Use at most {PASSWORD_MAX_LEN} characters."
    if password.lower() in _COMMON:
        return "That password is too common."
    return None     # no rule about capitals, numbers or symbols (FR-28b)


def _prep(password):
    # bcrypt only reads the first 72 bytes. Hashing first lets a 64 to 128 character password count in full.
    return base64.b64encode(hashlib.sha256(password.encode("utf-8")).digest())


def hash_password(password):
    return bcrypt.hashpw(_prep(password), bcrypt.gensalt())      # salted and scrambled, FR-28f


def check_password(password, hashed):
    return bcrypt.checkpw(_prep(password), hashed)


@dataclass
class User:
    username: str
    full_name: str
    role: str
    pw_hash: bytes
    session_min: int = SESSION_DEFAULT_MIN
    failed: int = 0
    blocked_until: float = 0.0


@dataclass
class Session:
    token: str
    username: str
    role: str
    last_active: float
    timeout_min: int


class Accounts:
    def __init__(self):
        self.users = {}
        self.sessions = {}

    # --- managing accounts: Administrator only (FR-27, UC-5). There is no password reset: the Administrator cannot do it. ---
    def create_user(self, by, username, full_name, role, password):
        if by is None or not can(by.role, "manage_users"):
            return None, "Only the Administrator manages users."
        return self._add(username, full_name, role, password)

    def _add(self, username, full_name, role, password):
        if role not in ROLES:
            return None, "Unknown role."
        if username in self.users:
            return None, "That username is taken."
        problem = password_problem(password)
        if problem:
            return None, problem
        user = User(username, full_name, role, hash_password(password))
        self.users[username] = user
        return user, ""

    def remove_user(self, by, username):
        if by is None or not can(by.role, "manage_users"):
            return False, "Only the Administrator manages users."
        if username not in self.users:
            return False, "No such user."
        del self.users[username]
        for tok in [t for t, s in self.sessions.items() if s.username == username]:
            del self.sessions[tok]
        return True, ""

    def change_own_password(self, user, old, new):
        if not check_password(old, user.pw_hash):
            return False, "Wrong password."
        problem = password_problem(new)
        if problem:
            return False, problem
        user.pw_hash = hash_password(new)
        return True, ""

    # --- signing in (FR-28, FR-28d) ---
    def sign_in(self, username, password):
        user = self.users.get(username)
        if user is None:
            return None, "Wrong username or password."
        now = clock.now()
        if user.blocked_until > now:
            minutes = math.ceil((user.blocked_until - now) / 60)
            return None, f"This account is blocked. Try again in {minutes} minutes."
        if not check_password(password, user.pw_hash):
            user.failed += 1
            if user.failed >= LOGIN_MAX_FAILS:
                user.failed = 0
                user.blocked_until = now + LOGIN_BLOCK_MIN * 60
                return None, f"Too many wrong passwords. The account is blocked for {LOGIN_BLOCK_MIN} minutes."
            return None, "Wrong username or password."
        user.failed = 0
        session = Session(secrets.token_urlsafe(24), user.username, user.role, now, user.session_min)
        self.sessions[session.token] = session
        return session, ""

    def session_for(self, token, touch=True):
        """The live session, or None. None means the person must sign in (FR-28), also after the idle time ran out (FR-26).
        touch=False is for calls the screen makes by itself (live data); only a person's own action keeps the session alive."""
        session = self.sessions.get(token)
        if session is None:
            return None
        now = clock.now()
        if now - session.last_active > session.timeout_min * 60:
            del self.sessions[token]
            return None
        if touch:
            session.last_active = now
        return session

    def set_session_minutes(self, token, minutes):
        """Each person sets their own sign-out time, 1 to 5 minutes. FR-26."""
        session = self.session_for(token)
        if session is None:
            return False, "Sign in first."
        if not isinstance(minutes, int) or isinstance(minutes, bool) or not (SESSION_MIN_MIN <= minutes <= SESSION_MAX_MIN):
            return False, f"Choose {SESSION_MIN_MIN} to {SESSION_MAX_MIN} minutes."
        session.timeout_min = minutes
        self.users[session.username].session_min = minutes
        return True, ""

    def sign_out(self, token):
        self.sessions.pop(token, None)
