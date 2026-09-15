"""Repository-level viability gates for externally discovered work."""


def repository_eligible(*, archived: bool, writable: bool = True) -> bool:
    """Archived repositories cannot accept normal contribution PRs.

    writable refers to the upstream accepting changes, not our local permissions.
    """
    return (not archived) and writable


def rejection_reason(*, archived: bool, writable: bool = True) -> str | None:
    if archived:
        return "ARCHIVED_REPOSITORY"
    if not writable:
        return "UPSTREAM_NOT_WRITABLE"
    return None
