"""SmartIrrigationEntity class"""
from homeassistant.helpers import entity

from .const import DOMAIN, NAME, VERSION


class SmartIrrigationEntity(entity.Entity):
    def __init__(self, coordinator, config_entry, mytype):
        self.coordinator = coordinator
        self.config_entry = config_entry
        self.type = mytype

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + "_" + self.type

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Brother entity."""
        await self.coordinator.async_request_refresh()