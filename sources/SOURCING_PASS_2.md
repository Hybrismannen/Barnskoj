# Sourcing expansion — 2026-11-19 (Pass 2)

## Scope and integrity
- 57 source candidates evaluated from web search results or exact existing URLs.
- **46 distinct new URLs** added to the source inventory, total 71 rows including prior registry.
- **184 profile records** can be linked to at least one newly discovered domain-, universe-, or person-specific source; **224 new catalog↔source relationships**.
- A domain portal does **not** verify the named person's individual details. Every link is marked as a research lead; only person-specific pages are candidates for atomic statement verification.
- Names and URLs are source discovery, not proof of image usage rights or comprehensive biographical verification.

## Source selection
- 1960–90 Swedish programming: Sveriges Television catalogue and primary programme pages
- International characters: rights holders, publishers, companies behind licensed worlds
- Rock/pop: Rock & Roll Hall of Fame original artist entries and archival index
- Sport: FIFA, Swedish FA, NBA, Olympics, NHL
- Nostalgic material culture: Nordiska museet's original holdings

## Evidence gates
`source_discovered` → `source_page_read` → `specific_claim_checked` → `independent_corroboration_if_material` → `rights_evaluated` → `production_eligible`.

Do not automatically upgrade an entity's `verification_status` from research_candidate. Some characters listed in an original programme may not be explicitly documented on a programme's overview page.

## Data quality issues
- A single row may represent multiple persons (e.g. group), performer, fictional persona, or collective; audit `record_kind` before mapping a source statement.
- Alias duplication (Mondo/Armand Duplantis) remains an identified task.
- Generation filters must separate character creation, Swedish broadcast, and user childhood years.
- There is no general permission to reproduce character silhouettes or portraits for commercial books.
