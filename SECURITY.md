# Security policy

## Scope

Bypass Android FLAG_SECURE Restrictions is intended for controlled research on applications owned by, or explicitly authorized for testing by, the researcher.

The project will not accept features that:

- activate for arbitrary packages or use wildcard targeting;
- target financial, identity, health, password-management, or other third-party applications;
- hide root or evade Play Integrity, application attestation, or anti-tamper controls;
- inject globally into `system_server`;
- collect screenshots, recordings, credentials, tokens, or personal information;
- send telemetry or other information over the network.

Future process-specific behavior must fail closed and require all authorization checks: exact package name, debuggable application state, explicit opt-in metadata, and a pinned signing-certificate digest.

## Reporting

Do not open a public issue for a vulnerability that could affect users. Send a private report to the repository owner with the affected version, reproduction conditions, impact, and a proposed mitigation. Replace this paragraph with a project security contact before publishing the repository.

## Release safety

Release artifacts are built deterministically and accompanied by `SHA256SUMS`. The project does not claim that checksums alone establish publisher identity; published releases should additionally use the repository host's signed-release or provenance features.
