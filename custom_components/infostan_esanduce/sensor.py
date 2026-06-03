from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    ident = entry.data["ident"]
    async_add_entities([
        InfostanSenzorDuga(coordinator, entry, ident),
        InfostanSenzorObavestenja(coordinator, entry, ident),
    ])


class InfostanSenzorDuga(CoordinatorEntity, SensorEntity):
    """Укупан дуг према Инфостану."""

    _attr_icon = "mdi:cash-multiple"
    _attr_native_unit_of_measurement = "RSD"

    def __init__(self, coordinator, entry, ident):
        super().__init__(coordinator)
        self._attr_name = f"Инфостан {ident} — Укупан дуг"
        self._attr_unique_id = f"infostan_{ident}_ukupan_dug"

    @property
    def state(self):
        d = (self.coordinator.data or {}).get("dug", {})
        return d.get("ukupno", 0.0)

    @property
    def extra_state_attributes(self):
        d = (self.coordinator.data or {}).get("dug", {})
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


class InfostanSenzorObavestenja(CoordinatorEntity, SensorEntity):
    """Број непрочитаних обавештења."""

    _attr_icon = "mdi:bell"

    def __init__(self, coordinator, entry, ident):
        super().__init__(coordinator)
        self._attr_name = f"Инфостан {ident} — Обавештења"
        self._attr_unique_id = f"infostan_{ident}_obavestenja"

    @property
    def state(self):
        o = (self.coordinator.data or {}).get("obavestenja", {})
        return o.get("brojNeprocitanih", 0)

    @property
    def extra_state_attributes(self):
        o = (self.coordinator.data or {}).get("obavestenja", {})
        poruke = o.get("listaObavestenja", {}).get("data", [])
        return {
            "укупно": o.get("ukupanBrojObavestenja", 0),
            "прочитаних": o.get("brojProcitanih", 0),
            "последња_порука": poruke[0].get("skrOpisObavestenje") if poruke else None,
            "датум_последње": poruke[0].get("datumAktivacijeStr") if poruke else None,
        }
