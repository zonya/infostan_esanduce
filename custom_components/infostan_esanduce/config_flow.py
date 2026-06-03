import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .api import prijava, get_podaci, InfostanAuthError, InfostanApiError

STEP_SCHEMA = vol.Schema({
    vol.Required("korisnicko_ime"): str,
    vol.Required("lozinka"): str,
    vol.Required("ident"): str,
})


class InfostanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            session = async_get_clientsession(self.hass)
            try:
                token = await prijava(session, user_input["korisnicko_ime"], user_input["lozinka"])
                await get_podaci(session, token, user_input["ident"])
            except InfostanAuthError:
                errors["base"] = "invalid_auth"
            except InfostanApiError:
                errors["base"] = "invalid_ident"
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_input["ident"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Infostan {user_input['ident']}",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_SCHEMA, errors=errors
        )
