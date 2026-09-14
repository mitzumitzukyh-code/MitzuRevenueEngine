# CI validation

Every change must pass:

1. dependency installation on Python 3.12;
2. Ruff static analysis;
3. pytest unit tests.

Autonomous execution and wallet signing remain disabled until CI is green and production deployment health checks pass.
