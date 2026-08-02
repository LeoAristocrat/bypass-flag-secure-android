# Contributing

Contributions should preserve the fail-closed, explicitly authorized research scope described in `SECURITY.md`.

## Development workflow

1. Create a focused branch.
2. Keep all shell files LF-only and compatible with BusyBox `ash`.
3. Run `python tools/build.py`.
4. Run `python tools/validate.py dist/*.zip`.
5. Run `python -m unittest discover -s tests -v`.
6. Update the compatibility matrix only with results reproduced on the exact listed environment.

Pull requests should explain behavior, risk, test coverage, recovery behavior, and the environments on which the change was exercised.

Changes that broaden targeting, weaken authorization checks, evade integrity systems, or introduce data collection are out of scope.
