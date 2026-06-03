# Infostan eSanduče — Home Assistant integracija

Nezvanična HACS integracija za praćenje komunalnih zaduženja i računa putem [eSanduče portala](https://esanduce.rs).

## Šta pruža

| Senzor | Opis |
|--------|------|
| `sensor.infostan_IDENT_ukupan_dug` | Ukupan neizmireni dug (RSD) |
| `sensor.infostan_IDENT_poslednji_racun` | Iznos poslednjeg računa sa istorijom 13 meseci |
| `sensor.infostan_IDENT_obavestenja` | Broj nepročitanih obaveštenja |

## Instalacija

### Putem HACS (preporučeno)

1. HACS → Custom repositories → dodaj `https://github.com/zonya/infostan_esanduce` → Integration
2. Instaliraj **Infostan eSanduče**
3. Restartuj Home Assistant
4. Podešavanja → Integracije → Dodaj → **Infostan eSanduče**

### Ručno

Kopiraj `custom_components/infostan_esanduce/` u `<config>/custom_components/` i restartuj HA.

## Konfiguracija

| Polje | Opis |
|-------|------|
| Korisničko ime | Korisničko ime sa eSanduče portala |
| Lozinka | Lozinka sa eSanduče portala |
| Broj identa | Broj identa (vidljiv na računu ili u portalu) |

## Napomene

- Podaci se osvežavaju svakih 4 sata
- Integracija se prijavljivuje pre svakog osvežavanja (JWT token traje ~30 min)
- Testirano na nalogu sa jednim identom (stan)
