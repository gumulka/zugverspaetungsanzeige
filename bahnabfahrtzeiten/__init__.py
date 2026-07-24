from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import api

PLATFORMS = [Platform.SENSOR]

type HubConfigEntry = ConfigEntry[api.BahnAbfahrtzeitenClient]


async def async_setup_entry(hass: HomeAssistant, entry: HubConfigEntry) -> bool:
    """Set up Hello World from a config entry."""

    session = async_get_clientsession(hass)
    entry.runtime_data = api.BahnAbfahrtzeitenClient(session, entry.data["bahnhof"], entry.data["eva_number"], entry.data["max_results"])

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok
