# Dataparitet och verifierbarhet v2.0

**Omfattning:** 485 entiteter (246 figurposter, 184 personer/grupper, 55 universum). Varje objekt måste ha 17 obligatoriska attribut, 14 obligatoriska taggdimensioner, en fördjupningsprofil, ett källdossier, ett individuellt standarddatakort och rättighetsgrind.

## Attribut
- `display_name`
- `entity_type`
- `canonical_id`
- `universe_id`
- `primary_medium`
- `genre_bucket`
- `era_association`
- `cultural_context`
- `first_appearance_year`
- `documented_swedish_broadcast_year`
- `credited_creator`
- `origin_country`
- `intended_audience`
- `activity_format`
- `rights_status`
- `publication_status`
- `research_grade`

## Taggdimensioner
- `entity_type`
- `medium`
- `cultural_context`
- `cultural_era`
- `universe`
- `curation_bucket`
- `audience`
- `activity_format`
- `source_quality`
- `rights`
- `publication`
- `geographic_origin`
- `identity`
- `language_variant`

## Evidens och betydelse
`claim_verified` = belagt av ett kontrollerat faktapåstående med källställe. `catalog_derived` = ärvt katalogfält, ej individuellt verifierat. `unknown` = öppet forskningsbehov. `not_applicable` och `not_assigned` = ska inte fyllas för denna entitet eller under forskningsfas. `policy_state` = intern rättighetsgrind. `computed_from_registry` = QA-klassning.

**Alla har nu samma standard för verifierbarhet, inte samma mängd verifierade historiska fakta.** Fält utan stöd får inte förvandlas till antaganden. Betydelsen av epok, ursprungsland och svensk sändning hålls åtskilda.

[Kanonisk redigerbar bas](../catalog/source/entities_base.csv) · [genererad läsvy med 485 entiteter](../catalog/entities.csv) · [Attributbelägg](../evidence/attribute_evidence.csv) · [Individuella datakort](../records/) · [Paritetsrevision](../quality/entity_parity.csv) · [Taggdefinitioner](../tags/taxonomy.csv).

Inga rättigheter till figurer och porträtt är klarerade. Q3 kräver verklig individuell djupgranskning med ursprungs- och versionsfakta, relevanta primärkällor, konflikthantering och redaktionell sign-off.

## Automatiserad paritet efter WP01
Ändra kanoniska fält endast i [entities_base.csv](../catalog/source/entities_base.csv). Kategoriunika uppgifter finns i [legacy_details.csv](../catalog/source/legacy_details.csv); faktabelägg i [claims.csv](../evidence/claims.csv) och [field_proofs.csv](../evidence/field_proofs.csv); taggar i [assignments.csv](../tags/assignments.csv). `python scripts/build_catalog.py` återgenererar 485 standardkort, kategorivyer och kvalitetsregister. `--check` avvisar exakt drift.
