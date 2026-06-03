import aiohttp
from .const import API_BASE, APP_ID


class InfostanAuthError(Exception):
    pass


class InfostanApiError(Exception):
    pass


async def prijava(session: aiohttp.ClientSession, korisnicko_ime: str, lozinka: str) -> str:
    async with session.post(
        f"{API_BASE}/api/korisnik/prijava",
        json={"korisnickoIme": korisnicko_ime, "lozinka": lozinka,
              "aplikacijaId": APP_ID, "tip": "password"},
    ) as r:
        if r.status == 401:
            raise InfostanAuthError
        if r.status != 200:
            raise InfostanApiError(f"Login HTTP {r.status}")
        data = await r.json(content_type=None)
        return data["token"]


async def get_dug(session: aiohttp.ClientSession, token: str, ident: str) -> dict:
    h = {"Authorization": f"Bearer {token}"}
    async with session.get(
        f"{API_BASE}/api/SONUpit/ident/{ident}/sumarnipodaci-po-vrstama",
        headers=h,
    ) as r:
        if r.status != 200:
            raise InfostanApiError(f"Dug HTTP {r.status}")
        return await r.json(content_type=None)
