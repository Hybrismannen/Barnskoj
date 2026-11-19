# Kvalitetsdjup 2026-11-19 – reparerad källintegritet

## Utfall
- **430 entiteter:** 154 Q0 utan källa, 240 Q1 med källspår, 36 Q2 med minst ett kontrollerat faktapåstående. **0 Q3** fullständigt granskade.
- **90 källregistreringar**, **39 atomära påståenden** och **13 kontrollerade webbsidor** för avgränsade fakta.
- **0 okända source-ID-kopplingar** efter schemajustering.
- **2 alias-/cross-catalog-rader**, **5 verkliga programledare ännu i figurkatalog**.
- **430 rättighetsgrindar i HOLD**: ingen publicerbar karaktärsbild eller personporträtt är licensierad.

## Reparerat importfel
Tidigare registerversion hade en oquotad rubrikrad och citerade datarader. En import behandlade oquotade rubriker fel och skrev om källregistret utan header. CSV-rubriken har återställts och alla 430 källdossierer **omgenererats med korrekt source-ID-validering**. Inga påståenden har fått höjd granskning på grund av importreparationen.

## Kritiska kvarvarande kvalitetsfrågor
1. 394 entiteter behöver objektspecifik faktagranskning.
2. Epokintervall är breda sökfacetter, inte debutår eller svensk sändningshistoria.
3. Identitet, medverkande personer, rollfigurer och kollektiv måste särskiljas.
4. Äldre source-registry-verifieringsetiketter är inte bevis för nya URL-kontroller; endast `evidence/source_checks.csv` är faktaspecifik.
5. Licensiering och tryckbarhet är helt separata arbetsflöden från källgranskningen.

## Spårbarhet
- [Kvalitetsregister](entity_quality.csv)
- [Faktapåståenden](../evidence/claims.csv)
- [Källdossierer](../sources/entity-dossiers/)
- [Taggtaxonomi](../tags/taxonomy.csv)
