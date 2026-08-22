# Changelog

## 0.21.3.post5 - 2026-08-22

- Pin pyplejd to the physical-state confirmation build.
- Reject echoed `LastChangedDataVector` control packets as delivery proof.
- Poll `NodeIndexData` after non-gateway writes and require the requested power
  state plus dim level before skipping reauthentication or reconnect recovery.
- Replace the prior logical-state-only acceptance test with mandatory physical
  verification from Homey for every Plejd node.

## 0.21.3.post4 - 2026-08-21

- Reauthenticate the existing BLE connection after an unconfirmed command.
- Poll for the matching state before falling back to a full reconnect.
- Retain the tested post2/post3 reconnect path if in-place authentication does
  not flush the mesh command.

## 0.21.3.post3 - 2026-08-21

- Wait briefly for a matching device-state confirmation before reconnecting.
- Keep the reliable reconnect-and-flush path as a fallback only when the mesh
  does not confirm the command.
- Reduce normal non-gateway command latency without sacrificing the successful
  post2 fallback behavior.

## 0.21.3.post2 - 2026-08-21

- Pin the integration to the tested `krsch79/pyplejd` reliability commit.
- Flush commands to non-gateway mesh nodes with one serialized reconnect.
- Disable active button-event polling to stop stale-event feedback storms.
- Deduplicate identical button actions received within 250 milliseconds.
- Add redacted local connection and recovery counters to diagnostics.
