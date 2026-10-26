"""Fault records and their life. Open -> acknowledged (each person for themselves) -> resolved. Step 5.

FR-7, FR-7a, FR-7b, FR-7c   pop-up to every connected Operator and Engineer; never to the Administrator
FR-8, FR-8a, FR-8b          each person acknowledges for themselves; record who and when; acknowledging does not close it
FR-15                       one fault record per abnormal parameter
FR-16                       no duplicate alert while a fault is open
FR-17                       only an Engineer resolves, after acknowledging; record when
FR-18, FR-19                maintenance mode for a stated time; alerts pause; overdue flag
FR-23d                      each fault stores the limit in force when it was raised
"""


def raise_fault(machine_id, parameter, level, limit_in_force):
    raise NotImplementedError("step 5")


def acknowledge(fault_id, user):
    raise NotImplementedError("step 5")


def resolve(fault_id, engineer):
    raise NotImplementedError("step 5")


def set_maintenance(machine_id, minutes, engineer):
    raise NotImplementedError("step 8")
