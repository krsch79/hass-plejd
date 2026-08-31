# Changelog

## 0.21.3.post11 - 2026-08-31

- Stop creating the misleading `Is gateway` and `May be gateway` entities while
  direct on-demand control is active; short command sessions are not persistent
  Plejd mesh gateways.
- Add structured `PLEJD_COMMAND_AUDIT` log lines for every light command,
  including Home Assistant context identifiers but no credentials, so future
  unexpected group-off commands can be traced to their caller and timestamp.

## 0.21.3.post10 - 2026-08-27

- Discard stale state-changing LastData echoes in direct on-demand sessions.
- Use the post-command LightLevel poll as the sole authoritative Plejd state,
  preventing false off/on transitions from propagating to Homey when lights
  are adjusted in quick succession.
- Pin pyplejd to the matching post9 echo-filter build.

## 0.21.3.post9 - 2026-08-27

- Isolate every on-demand BLE session from delayed notifications belonging to
  the previously controlled Plejd node.
- Filter direct-session state updates to outputs on the connected target
  hardware, preventing stale mesh reports from switching an unrelated Home
  Assistant or Homey light state during rapid consecutive dim commands.
- Pin pyplejd to the matching post8 race-condition fix.

## 0.21.3.post8 - 2026-08-22

- Replace the long-lived Plejd gateway connection with confirmed, on-demand
  direct connections to the hardware that owns each output.
- Disconnect after each command while preserving entity availability, avoiding
  the firmware 6.43.3 output oscillation reproduced after a full power cycle.
- Use live BLE advertisements to restore availability without opening a
  controller connection.
- Pin pyplejd to the matching post7 on-demand reliability build.

## 0.21.3.post7 - 2026-08-22

- Disable the technical `May be gateway` selectors by default in the Home
  Assistant entity registry.
- Keep the selectors available for explicit troubleshooting without exposing
  them as extra physical switches to bridge clients such as Homey.

## 0.21.3.post6 - 2026-08-22

- Pin pyplejd to the direct target-node routing build.
- Route every safely mappable light command through the Plejd hardware that
  owns the addressed output instead of relying on broken firmware mesh writes.
- Keep the active target connected for successive dim commands.
- Categorize `May be gateway` as a Home Assistant configuration entity so it is
  not represented as a second physical circuit by bridge clients such as Homey.
- Retain the post5 confirmation/recovery path for non-addressable commands.

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
