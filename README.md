# Barnskoj

**Lek, skapa, klura och upptäck – för barn, unga och vuxna.**

Barnskoj är under uppbyggnad som ett generationsöverskridande kultur-, originalmotiv- och aktivitetsbibliotek. **Ingen färdig utskrivbar aktivitet har publicerats ännu.** Underlagen ska bli prick-till-prick, målarbilder, mandala, kreativt spel och nostalgiska vuxenböcker.

## Tre arbetslager

| Del | Innehåll | Faktiskt tillstånd |
| --- | --- | --- |
| [Kulturreferenser](catalog/entities.csv) | 485 figurer, personer/grupper och programvärldar, 90 källadresser, 39 avgränsade faktabelägg | Forskningsdata, inte bildlicenser |
| [Kreativa motiv](creative/README.md) | 32 självständiga originalkoncept, 12 teman, 6 format och 8 generationskollektioner | Förslag – inga färdiga originalbilder |
| [Aktiviteter och assets](production/README.md) | Tre A4-prick-till-prick-prototyper med facit (sex SVG-filer) | **3 prototyper · 0 publicerade** |

Den automatiskt uppdaterbara statusen finns i [discovery/metrics.json](discovery/metrics.json).

## Sök, kombinera och skapa

[Upptäcktsgrafen](discovery/README.md) binder ihop **689 noder, 3 085 relationer och 704 kreativa förslag** genom epoker, intressen, figurer, sport, musik, barn-tv, originalmotiv, format och bokserier.

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

**En kanonisk skrivväg:** [catalog/source/entities_base.csv](catalog/source/entities_base.csv) äger entitetsbasen och [legacy_details.csv](catalog/source/legacy_details.csv) bevarar kategoriunika fält. Källor, claims och taggar underhålls i sina respektive källregister. Alla 485 datakort och äldre CSV-vyer genereras, inte redigeras manuellt. För prototyper finns [produktionsspecifikationer](production/prototype_specs.json).

```bash
python scripts/build_catalog.py
python scripts/build_discovery.py
python scripts/build_prototypes.py
python scripts/doctor.py
```

[DevOps – exakt tre arbetspaket](devops/WORKPACKAGES.md) och [driftrutin](devops/RUNBOOK.md) beskriver vad som får redigeras, genereras och publiceras. [Systemkartan](docs/SYSTEM_ARCHITECTURE.md) visar källor och härledda vyer. [Arkitekturrevision](docs/ARCHITECTURE_AUDIT_2026-11-20.md) beskriver flaskhalsar och prioriterad utveckling. [Roadmap](docs/ROADMAP.md) följer leveranser.

## CDX

[Det lokala CDX-ankaret](.cdx/anchor.json) har versionspinnad Conductellence-policy **1.0.0** och en [CI-kontroll](.github/workflows/cdx-anchor-audit.yml).

**Status: ANCHOR_DECLARED / NOT_VERIFIED.** Barnskoj har ännu ingen central CDX Estate-admission och ingen verifierad consequential runtime. [CDX-status och gränser](.cdx/README.md).

**Projektregel:** Källa ≠ faktabelägg ≠ bildlicens. Koncept ≠ producerat material. Strukturell QA ≠ fullständig forskning.
