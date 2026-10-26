"""Administrator and limits. Step 7.
FR-22 change log (who and when), FR-23 keep the old limit and date, FR-23a Engineer changes limits without a restart,
FR-23b reject a warning limit that is not below the critical limit, FR-23c a new limit applies to later readings,
FR-27 only the Administrator manages users and machines. The Administrator cannot reset passwords."""


def change_limit(machine_type, parameter, warning, critical, engineer):
    if warning is not None and critical is not None and warning >= critical:
        return False, "The warning limit must be below the critical limit."     # FR-23b
    raise NotImplementedError("step 7")
