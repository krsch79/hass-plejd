# Changelog

## 0.21.3.post2 - 2026-08-21

- Pin the integration to the tested `krsch79/pyplejd` reliability commit.
- Flush commands to non-gateway mesh nodes with one serialized reconnect.
- Disable active button-event polling to stop stale-event feedback storms.
- Deduplicate identical button actions received within 250 milliseconds.
- Add redacted local connection and recovery counters to diagnostics.
