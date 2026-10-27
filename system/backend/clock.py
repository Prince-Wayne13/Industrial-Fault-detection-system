"""The one time source. Every part of the system asks this module for the time. FR-25.

Real mode (default): the computer clock.
Simulated mode: set_time() fixes the clock so seeded scenarios run instantly and give the same result every time.
advance() jumps the clock forward, for the demo's fast-forward (24 hours, lockout, maintenance time).
"""
import time

_fixed = None
_offset = 0.0


def now():
    return (_fixed if _fixed is not None else time.time()) + _offset


def real():
    """The computer clock, for measuring how long something took (start-up, uptime, reading time). Never moved by set_time or advance."""
    return time.time()


def set_time(t):
    global _fixed
    _fixed = float(t)


def advance(seconds):
    global _fixed, _offset
    if _fixed is not None:
        _fixed += seconds
    else:
        _offset += seconds


def use_real():
    global _fixed, _offset
    _fixed = None
    _offset = 0.0
