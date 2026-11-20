# Barnskoj

**Lek, skapa, klura och upptäck – för barn, unga och vuxna.**

Barnskoj är under uppbyggnad som ett generationsöverskridande kultur-, originalmotiv- och aktivitetsbibliotek. **Ingen färdig utskrivbar aktivitet har publicerats ännu.** Underlagen ska bli prick-till-prick, målarbilder, mandala, kreativt spel och nostalgiska vuxenböcker.

## Tre arbetslager

| Del | Innehåll | Faktiskt tillstånd |
| --- | --- | --- |
| [Kulturreferenser](catalog/entities.csv) | 485 figurer, personer/grupper och programvärldar, 90 källadresser, 39 avgränsade faktabelägg | Forskningsdata, inte bildlicenser |
| [Kreativa motiv](creative/README.md) | 32 självständiga originalkoncept, 12 teman, 6 format och 8 generationskollektioner | Förslag – inga färdiga originalbilder |
| [Färdiga aktiviteter och assets](production/README.md) | Aktivitetsblad, originalfiler, facit, rättighetsbeslut och trycktest | **0 producerade/publicerade** |

Den automatiskt uppdaterbara statusen finns i [discovery/metrics.json](discovery/metrics.json).

## Sök, kombinera och skapa

[Upptäcktsgrafen](discovery/README.md) binder ihop **680 noder, 3 073 relationer och 704 kreativa förslag** genom epoker, intressen, figurer, sport, musik, barn-tv, originalmotiv, format och bokserier.

- [Filter- och sökindex](discovery/search.csv)
- [Relationer med bevisgränser](discovery/edges.csv)
- [Redaktionella korskopplingsförslag](discovery/crosslinks.csv)
- [Generationsbibliotek 1950–2025](catalog/decades/collections.csv)

Kör lokalt i repot:

```bash
python scripts/query_discovery.py --entity BS-CHAR-0001
python scripts/query_discovery.py --theme music --era 1970s
```

Att en skyddad figur eller kändis leder till ett tema innebär **inte** att vi får reproducera karaktären eller porträttet.

## Forskningskvalitet och taggning

Alla 485 objekt har [17 obligatoriska attribut och 14 taggdimensioner](docs/PARITY_STANDARD.md). [134 taggdefinitioner](tags/taxonomy.csv) och 8 086 taggkopplingar möjliggör kombinationer. Verifieringsstatus enligt [QA-registret](quality/RESEARCH_PARITY.md): **Q0 191 · Q1 257 · Q2 37 · Q3 0**.

En källadress är inte en kontrollerad faktauppgift. Ett datakort är inte en färdig illustration. Ett motivkoncept är inte en publicerad aktivitet.

## Produktionsflödet

```text
Kulturreferens → tema/epok → självständigt originalmotiv
→ aktivitetsformat → skapad illustration + ev. facit
→ rättighets-, tillgänglighets- och tryckgranskning
→ registrerad och publicerad aktivitet/bok
```

[Prick-till-prick](library/prick-till-prick/README.md) · [Vuxennostalgi](library/adult-nostalgia/README.md) · [Produktvision](docs/PRODUCT.md) · [Release-grind](production/RELEASE_GATE.md).

## Uppdatera dataset

**Redigera källan, generera vyerna.** Den befintliga entitetsmodellen har ännu äldre parallella katalogfiler som behöver en separat, versionssäker konsolidering. Det nya kreativ-/discovery-lagret är automatiskt reproducerbart:

```bash
python scripts/build_discovery.py
python scripts/build_discovery.py --check
python scripts/validate_catalog.py
python scripts/validate_parity.py
python scripts/validate_production.py
python -m unittest discover -s tests -v
```

[Systemkartan](docs/SYSTEM_ARCHITECTURE.md) visar källor och härledda vyer. [Arkitekturrevision](docs/ARCHITECTURE_AUDIT_2026-11-20.md) beskriver flaskhalsar och prioriterad utveckling. [Roadmap](docs/ROADMAP.md) följer leveranser.

## CDX

[Det lokala CDX-ankaret](.cdx/anchor.json) har versionspinnad Conductellence-policy **1.0.0** och en [CI-kontroll](.github/workflows/cdx-anchor-audit.yml).

**Status: ANCHOR_DECLARED / NOT_VERIFIED.** Barnskoj har ännu ingen central CDX Estate-admission och ingen verifierad consequential runtime. [CDX-status och gränser](.cdx/README.md).

**Projektregel:** Källa ≠ faktabelägg ≠ bildlicens. Koncept ≠ producerat material. Strukturell QA ≠ fullständig forskning.
