"""Restricted operational wallet boundary.

Private keys and seed phrases must never be committed to this repository.
Signing will be implemented behind a policy-enforced provider interface.
"""

class WalletDisabled(RuntimeError):
    pass
