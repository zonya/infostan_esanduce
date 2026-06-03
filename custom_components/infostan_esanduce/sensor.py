from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([InfostanSenzorDuga(coordinator, entry)])


class InfostanSenzorDuga(CoordinatorEntity, SensorEntity):
    """Ukupan dug prema Infostanu."""

    _attr_icon = "mdi:cash-multiple"
    _attr_native_unit_of_measurement = "RSD"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._entry = entry
        ident = entry.data["ident"]
        self._attr_name = f"Infostan {ident} — Укупан дуг"
        self._attr_unique_id = f"infostan_{ident}_ukupan_dug"

    @property
    def state(self):
        d = self.coordinator.data
        return d.get("ukupno", 0.0) if d else 0.0

    @property
    def extra_state_attributes(self):
        d = self.coordinator.data or {}
        return {
            "редовно_задужење": d.get("redovno_zaduzenje"),
            "тужба": d.get("tuzba"),
            "репрограм": d.get("reprogram"),
            "нетужени_део": d.get("netuzeni_deo"),
            "претплата": d.get("pretplata"),
            "корисник": d.get("naziv_korisnika", "").strip(),
            "адреса": d.get("opis", "").strip(),
            "врста": d.get("vrsta"),
        }
