"""Constants for the Plejd component."""

DOMAIN = "plejd"
MANUFACTURER = "Plejd"

CONF_SITE_ID = "siteId"
CONF_SITE_TITLE = "siteTitle"

# Local reliability defaults for Home Assistant 2026.8 and Plejd firmware 6.43.x.
ENABLE_ACTIVE_BUTTON_POLLING = False
# Experimental central mesh mode. pyplejd post10 requests a 30-50 ms BLE
# connection interval so the gateway retains radio time for Plejd mesh traffic.
# The direct/on-demand implementation remains available as the exact post12
# rollback release and is not removed from either codebase.
ROUTE_CONTROL_WRITES_DIRECTLY = False
RECONNECT_NON_GATEWAY_CONTROL_WRITES = False
ON_DEMAND_CONTROL_CONNECTIONS = False
DUPLICATE_BUTTON_EVENT_WINDOW_SECONDS = 0.25
