"""Constants for the Plejd component."""

DOMAIN = "plejd"
MANUFACTURER = "Plejd"

CONF_SITE_ID = "siteId"
CONF_SITE_TITLE = "siteTitle"

# Local reliability defaults for Home Assistant 2026.8 and Plejd firmware 6.43.x.
ENABLE_ACTIVE_BUTTON_POLLING = False
RECONNECT_NON_GATEWAY_CONTROL_WRITES = True
DUPLICATE_BUTTON_EVENT_WINDOW_SECONDS = 0.25
