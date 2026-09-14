from app.ledger import record_event

class RecoveryWorker:
    """Records recovery attempts; concrete retry policies are added per adapter."""

    def recovered(self, db, *, message: str, opportunity_id: int | None = None):
        return record_event(db, kind="recovery", worker="recovery", message=message,
                            opportunity_id=opportunity_id, recovered=True)
