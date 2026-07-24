from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN  # pylint:disable=unused-import
from .api import get_bahnhof, get_eva_number

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("bahnhof"): str,
        vol.Optional("max_results", default=3): int,
        vol.Optional("refresh_interval", default=300): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input station exists"""

    session = async_get_clientsession(hass)
    bahnhof, title = await get_bahnhof(session, data["bahnhof"])
    if bahnhof is None:
        raise StationNotFound

    eva_number = await get_eva_number(session, bahnhof)
    if eva_number is None:
        raise StationAPIBreakage

    return {"title": title, "bahnhof": bahnhof, "eva_number": eva_number}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the configuration of the integration by the user."""

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                user_input["eva_number"] = info["eva_number"]
                user_input["bahnhof"] = info["bahnhof"]

                return self.async_create_entry(title=info["title"], data=user_input)
            except StationNotFound:
                errors["base"] = "station_not_found"
            except StationAPIBreakage:
                errors["base"] = "api_breakage"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class StationNotFound(exceptions.HomeAssistantError):
    """Error to indicate we cannot find the station."""


class StationAPIBreakage(exceptions.HomeAssistantError):
    """Error to indicate we cannot find the station."""
