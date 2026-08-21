# Project instructions

- Follow `/Volumes/Shared/AGENTS.md` for staging, backup, deployment, GitHub,
  notification, and secret-handling requirements.
- This fork exists only for the Raspberry Pi Home Assistant Plejd reliability
  release. Never commit Plejd credentials, Home Assistant `.storage`, recorder
  databases, logs, access tokens, or Bluetooth addresses from the live system.
- Keep `custom_components/plejd/manifest.json` pinned to an exact public
  `krsch79/pyplejd` commit, never a moving branch.
- Before deployment run `python -m unittest -v tests.test_release`, compile all
  component files, install the exact manifest requirement in a clean Python
  3.14 environment, and run Home Assistant `check_config` against a backup.
- A production acceptance test must confirm the requested gateway took over,
  exercise every light through the same Home Assistant token used by Homey,
  restore original light states, and compare unavailable periods and event-row
  growth before and after the release.
