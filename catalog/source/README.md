# Barnskoj – kanonisk skrivmodell (WP01)

**Skriv manuellt i exakt ett register per ansvar.** `entities_base.csv` äger gemensamma entitetsfält; `legacy_details.csv` bevarar kategoriunika äldre attribut som domän och ursprunglig granskningsetikett. `tags/assignments.csv` äger taggtilldelning, `evidence/claims.csv` äger faktabelägg och `evidence/field_proofs.csv` äger fältkopplingen till ett verifierat påstående.

**Automatiskt framtagna kompatibilitetsvyer** via `python scripts/build_catalog.py` är `catalog/entities.csv`, `catalog/characters.csv`, `catalog/celebrities.csv`, `catalog/universes.csv`, `quality/entity_quality.csv`, `quality/entity_parity.csv`, `quality/RESEARCH_BACKLOG.csv`, `evidence/attribute_evidence.csv` och 485 `records/*.md`.

Kommandon: `python scripts/build_catalog.py` för ombyggnad, `python scripts/build_catalog.py --check` i CI; därefter `python scripts/build_discovery.py`.

**Ändra aldrig en genererad vy direkt.** ID, alias, källkopplingar och forskningsgrader ska behållas oförändrade av en migration. Fältspecifika belägg höjer inte hela profilen till Q3. En fil på GitHub är ingen bildlicens. Separata `profiles/*` och `sources/entity-dossiers/*` är redaktionella texter, inte automatiskt genererade och raderas inte.
