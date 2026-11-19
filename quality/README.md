# Barnskoj – kvalitets- och publiceringsgrindar

**Ny gemensam omfattning:** 485 entiteter, inklusive 55 universum. [Gemensam paritetsmatris](entity_parity.csv) och [faktisk forskningsparitet](RESEARCH_PARITY.md). Tidigare `entity_quality.csv` gäller 430 figur- och personposter men inte universumen; vid samlad analys ska `catalog/entities.csv` användas.

## Forskningsnivå
`Q0_no_source → Q1_source_leads → Q2_partial_claim_verified → Q3_deep_verified`

Klassningarna är **inte procentuella sannolikheter**. För Q2 krävs en identifierbar källa och ett avgränsat faktapåstående. Q3 kräver sammanhängande historik, flera relevanta oberoende originalkällor, datum/land-/versionsavgränsning, rättande av konflikter och redaktionell granskning. Ingen entitet är Q3 efter denna omgång.

**Publiceringsnivå är separat:** data-Q3 ger ingen tillåtelse att reproducera figurer, logotyper eller foton. Juridisk och produktionsspecifik klarering krävs alltid.

- [430 individuella QA-rader](entity_quality.csv)
- [Auditrapport med mängder och fel](COVERAGE.md)
- [Faktabeläggning](../evidence/claims.csv)
- [Taggsystemet](../tags/README.md)
- [Kontrollscript](../scripts/validate_catalog.py)
