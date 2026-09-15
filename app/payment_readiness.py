"""Payment architecture readiness without enabling settlement.

The production app remains non-payable. This module describes the intended
testnet rail and validates that a future receiver address is syntactically
safe before it can be advertised.
"""
from dataclasses import asdict, dataclass
import re

EVM_ADDRESS = re.compile(r"^0x[a-fA-F0-9]{40}$")


@dataclass(frozen=True)
class PaymentReadiness:
    protocol: str
    version: int
    scheme: str
    network: str
    asset: str
    facilitator: str
    receiver_configured: bool
    receiver_valid: bool
    settlement_enabled: bool
    real_funds: bool
    mode: str
    blockers: list[str]


def payment_readiness(receiver: str | None = None) -> dict:
    valid = bool(receiver and EVM_ADDRESS.fullmatch(receiver))
    blockers = []
    if not receiver:
        blockers.append("receiver_wallet_not_configured")
    elif not valid:
        blockers.append("receiver_wallet_invalid")
    blockers.append("settlement_disabled")

    return asdict(PaymentReadiness(
        protocol="x402",
        version=2,
        scheme="exact",
        network="eip155:84532",
        asset="USDC_TESTNET",
        facilitator="https://x402.org/facilitator",
        receiver_configured=bool(receiver),
        receiver_valid=valid,
        settlement_enabled=False,
        real_funds=False,
        mode="PAYMENT_READY_TESTNET_NO_SETTLEMENT",
        blockers=blockers,
    ))
