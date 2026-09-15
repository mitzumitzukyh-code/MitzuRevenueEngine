from app.config import settings


def test_production_rejects_sqlite_configuration():
    assert settings.database_url


def test_worker_failure_limit_is_positive():
    assert settings.worker_max_consecutive_failures > 0
    assert settings.worker_backoff_max_seconds > 0
