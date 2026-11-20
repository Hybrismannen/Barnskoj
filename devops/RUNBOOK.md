# Barnskoj – DevOps-runbook

## En kontrollkedja
```bash
python scripts/doctor.py
```
Kommandot kör tio read-only-grindar: synkning av katalogen, äldre integritetskontroller, fältevidens/paritet, discovery, SVG, facit, publiceringsrätt, CDX-deklaration och regressionstester. Ett FAIL stoppar ändringen. Inget steg publicerar, licensierar eller ändrar extern myndighet.

## Ändra entitetsfakta eller namn
1. Redigera [entities_base.csv](../catalog/source/entities_base.csv) (gemensamma attribut) eller [legacy_details.csv](../catalog/source/legacy_details.csv) (kategoriunika fält). Bevara beständiga ID.
2. För påståenden: uppdatera [claims.csv](../evidence/claims.csv) och [source registry](../sources/registry.csv). Ange endast **verifierade attributkopplingar** i [field_proofs.csv](../evidence/field_proofs.csv).
3. För taggar: ändra [assignments.csv](../tags/assignments.csv), efter kontroll mot [taxonomy.csv](../tags/taxonomy.csv).
4. Kör `python scripts/build_catalog.py` och därefter `python scripts/build_discovery.py`.
5. Kör `python scripts/doctor.py`. Commita källfiler och alla genererade vyer i samma ändring.

**Redigera aldrig direkt:** `catalog/entities.csv`, `characters.csv`, `celebrities.csv`, `universes.csv`, `records/*.md`, `evidence/attribute_evidence.csv`, `quality/entity_quality.csv`, `quality/entity_parity.csv`, `quality/RESEARCH_BACKLOG.csv` eller `discovery/*`. Alla är genererade.

## Ändra ett kreativt koncept
Redigera [motifs.json](../creative/motifs.json), [themes.json](../creative/themes.json) eller [formats.json](../creative/formats.json); kör `python scripts/build_discovery.py` och sedan `python scripts/doctor.py`.

## Ändra en A4-prick-till-prick-prototyp
Redigera [prototype_specs.json](../production/prototype_specs.json), kör `python scripts/build_prototypes.py`, `python scripts/validate_svg_prototypes.py` och `python scripts/doctor.py`. Om nya aktivitets-ID tillkommer: lägg till rätt rad i `activities.csv` samt primär- och facitasset i `assets.csv`, bygg om discovery och kör doctor.

## Publicering
Ändra aldrig `status` till `published` utan att [produktionsgrinden](../production/RELEASE_GATE.md) är uppfylld med verkliga mänskliga beslut, tillgänglighets-/tryckprov, licenser och innehållskontroll. Automatiskt passerad geometri-QA är **inte** ett sådant beslut.

## CDX
`.cdx/anchor.json` är bundet till central CDX 1.0.0-policy men står **ANCHOR_DECLARED / NOT_VERIFIED**. Lokal CI kan inte besluta central admission. Skyddad runtime kräver separat governance om konsekventa effekter tillförs.
