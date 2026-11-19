# Barnskoj – kontrollerad facetterad taggning v1.0

**Omfattning:** 430 figur/personposter, 55 universum, 117 definierade taggar och 2813 dokumenterade taggkopplingar. **Taggarna ärvda/beräknade från befintliga katalogfält; de är inte individuellt faktagranskade.**

## Standardiserad täckning 2.0
Alla 485 entiteter måste ha **14 av 14 obligatoriska fasetter** (inklusive `unassigned`, `unverified` och `not-applicable` där detta är den sanningsenliga statusen). Idag finns 134 taggdefinitioner och 8 086 relationer. Verifiering på fältnivå dokumenteras separat i [attributregistret](../evidence/attribute_evidence.csv). Denna regel kontrolleras av [paritetsvalidatorn](../scripts/validate_parity.py).

## Fasetter (se [taxonomin](taxonomy.csv))
- `type:*` identifierar fiktiv figur, verklig person, grupp eller spelad tv-roll.
- `world:BS-WORLD-xxx` är stabil koppling till en [universumsprofil](../catalog/universes.csv).
- `medium:*` avser huvudsakligt berättelse-/verksamhetsmedium enligt katalogen.
- `market:*` är grovt katalogkontext, inte nationalitet/födelseland.
- `era:YYYYs` är **associerad epok enligt katalogens breda intervall**, aldrig källtillstyrkt debutår eller bevis för aktivitet under varje årtionde.
- `sport:*` / `music:*` används bara när kataloggruppen uttryckligen är någorlunda entydig.
- `bucket:*` bevarar ursprunglig redaktionell genregruppering även när den innehåller blandad musik/sport eller epok. **Inte belägg för exakt individuell genre.**
- `format:*` och `audience:*` är framtida **aktivitetsfacetter**. De får inte automatiskt sättas på kända personer eller figurer, eftersom produktions- och licensstatus är oberoende.

## Källsystem
`assignments.csv` är det normaliserade relationsregistret. `tag_ids` i person-/figur-CSV är en redundant export för sökning och kontrolleras mot relationsregistret av validator.

## Exempel på filter
- Svensk barn-tv: `market:sweden` + `medium:television`, följt av redaktionell verifiering.
- Nostalgiska 1970-talsreferenser: `era:1970s` (bred associerad epok; kolla premiär/sändning separat).
- Verkliga musikprofiler: `type:real-person` + `medium:music`.
- Originalmandalor för vuxna: aktivitets-taggar `format:mandala` + `audience:adult` + separat motivperiod och rättigheter.

## Kvalitetsregler
1. Tagg-ID är stabilt. Namnbyte sker i etikett, inte i ID.
2. En obekräftad uppgift markeras som `catalog_derived` eller `catalog_range_inferred` i assignment_basis.
3. Ingen tagg får upphöja `research_candidate` till `source_checked`.
4. Alias pekar på kanonisk identitet. Samma sträng i olika världar får **inte** automatiskt slås samman.
5. Ursprungsår, svensk sändningstid, användarens barndomsår och tilltänkt publik är fyra oberoende datadimensioner.

Se [identitetsregister](../catalog/identity_registry.csv), [aliasregister](../catalog/aliases.csv) och [universumsregister](../catalog/universes.csv).
