"""Platform for sensor integration."""

from typing import Any, override

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .const import DOMAIN  # pylint:disable=unused-import

import asyncio
from datetime import timedelta
import logging

from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    api = config_entry.runtime_data

    coordinator = BahnZeitenCoordinator(hass, config_entry, api)

    # Fetch initial data so we have data when entities subscribe
    #
    # If the refresh fails, async_config_entry_first_refresh will
    # raise ConfigEntryNotReady and setup will try again later.
    #
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        BahnZeitenSensor(coordinator, idx, config_entry.data["bahnhof"].lower())
        for idx, _ in enumerate(coordinator.data)
    )


class BahnZeitenCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, config_entry, bahn_api):
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Bahn Abfahrtzeiten",
            config_entry=config_entry,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=config_entry.data["refresh_interval"]),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=False,
        )
        self._bahn_api = bahn_api

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        async with asyncio.timeout(10):
            return await self._bahn_api.get_status()


class BahnZeitenSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, idx, bahnhof):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        self._coordinator = coordinator
        self._attr_unique_id = f"{bahnhof}_{idx}"
        _LOGGER.debug(f"Creating sensor {self._attr_unique_id}")
        self.__set_value()

    def __set_value(self):
        data = self._coordinator.data[self.idx]
        if data["canceled"]:
            self._attr_native_value = f"--:-- {data['destination']}"
        elif data["delayed"]:
            self._attr_native_value = f"{data['delayed_time']} {data['destination']}"
        else:
            self._attr_native_value = f"{data['scheduled_time']} {data['destination']}"

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        return self._coordinator.data[self.idx]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.__set_value()
        self.async_write_ha_state()
