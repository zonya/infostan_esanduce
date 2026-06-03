import json as json_lib
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
            raise InfostanApiError(f"Prijava HTTP {r.status}")
        data = await r.json(content_type=None)
        return data["token"]


async def get_podaci(session: aiohttp.ClientSession, token: str, ident: str) -> dict:
    h = {"Authorization": f"Bearer {token}"}

    async def get(url, params=None):
        async with session.get(url, headers=h, params=params) as r:
            if r.status != 200:
                return {}
            text = await r.text()
            if not text.strip() or text.strip().startswith("<"):
                return {}
            return await r.json(content_type=None)

    sort = json_lib.dumps([{"selector": "ggmm", "desc": True}])

    dug, obavestenja, dashboard, racuni = await _gather(
        get(f"{API_BASE}/api/SONUpit/ident/{ident}/sumarnipodaci-po-vrstama"),
        get(f"{API_BASE}/api/Korisnik/obavestenja"),
        get(f"{API_BASE}/api/Korisnik/dashboard"),
        get(f"{API_BASE}/api/SONUpit/ident/{ident}/racuni",
            params={"skip": "0", "take": "13", "sort": sort, "filter": ""}),
    )

    return {"dug": dug, "obavestenja": obavestenja, "dashboard": dashboard, "racuni": racuni}


async def _gather(*coros):
    import asyncio
    return await asyncio.gather(*coros, return_exceptions=False)
