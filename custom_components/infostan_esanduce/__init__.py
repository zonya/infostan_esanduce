from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .api import prijava, get_podaci, InfostanAuthError, InfostanApiError

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = async_get_clientsession(hass)

    async def _fetch():
        try:
            token = await prijava(session, entry.data["korisnicko_ime"], entry.data["lozinka"])
            return await get_podaci(session, token, entry.data["ident"])
        except (InfostanAuthError, InfostanApiError) as e:
            raise UpdateFailed(e) from e

    coordinator = DataUpdateCoordinator(
        hass, _LOGGER,
        name=DOMAIN,
        update_method=_fetch,
        update_interval=timedelta(hours=4),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
