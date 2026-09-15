from app.repository_gate import rejection_reason, repository_eligible


def test_archived_repository_is_never_eligible():
    assert repository_eligible(archived=True) is False
    assert rejection_reason(archived=True) == "ARCHIVED_REPOSITORY"


def test_active_repository_can_proceed_to_other_filters():
    assert repository_eligible(archived=False) is True
    assert rejection_reason(archived=False) is None


def test_read_only_upstream_is_rejected():
    assert repository_eligible(archived=False, writable=False) is False
    assert rejection_reason(archived=False, writable=False) == "UPSTREAM_NOT_WRITABLE"
