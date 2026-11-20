# Barnskoj – grafbaserad upptäckt och korsbefruktning

**Grundprincip:** Det finns en kunskapsgraf och en redaktionell upptäcktsgraf. Källbelagd identitet och faktapåståenden får aldrig sammanblandas med konceptuella kopplingar.

## Datakällor och automatiska vyer

**Primära redigerbara källor**
- [catalog/entities.csv](../catalog/entities.csv): befintliga 485 entiteter.
- [evidence/claims.csv](../evidence/claims.csv) + [sources/registry.csv](../sources/registry.csv): atomära belägg.
- [creative/motifs.json](../creative/motifs.json), [themes.json](../creative/themes.json) och [formats.json](../creative/formats.json): kuraterad originalinspiration.
- [catalog/decades/collections.csv](../catalog/decades/collections.csv): planerade bokserier.

**Genererade filer – redigera inte manuellt**
- `discovery/nodes.csv` – samma nod-ID oavsett vilken kategori eller vy som används.
- `discovery/edges.csv` – typade, spårbara relationskanter.
- `discovery/crosslinks.csv` – högst två redaktionella originalmotivförslag per entitet utifrån gemensamt **tema** och i förekommande fall associerad **epok**.
- `discovery/search.csv` – ett platt sök/filter-index för katalog, motiv och bokserier.
- `discovery/metrics.json` – maskinellt räknad aktuell status.

## Tillämpning

```bash
python scripts/build_discovery.py
python scripts/build_discovery.py --check
python scripts/query_discovery.py --entity BS-CHAR-0001
python scripts/query_discovery.py --theme music --era 1970s
```

Vid ny research: redigera faktakällor och claims samt verifiera med befintlig QA. Vid nya motiv: ändra `creative/motifs.json`, kör generatorn och checka in genererade filer. CI avvisar osynkroniserade vyer.

## Relationen betyder alltid något specifikt
- `CATALOG_MEMBER_OF`: ärvd figur→värld-relation (katalogdata, inte oberoende källgranskning).
- `IDENTITY_ALIAS_OF`: identitetsregistret kopplar samman dubbla poster.
- `CLAIM_ABOUT` och `CLAIM_SUPPORTED_BY`: *det enskilda* faktapåståendets belägg, inte stöd för hela entiteten.
- `CATALOG_TOPIC` och `CATALOG_ERA_ASSOCIATION`: bred sökkontext hämtad ur ärvda taggar, inte ett historiskt verifierat påstående.
- `EDITORIAL_DISCOVERY_CANDIDATE`: **endast ett kreativt förslag** att ta fram en självständig originalillustration. Ingen upphovs- eller porträtträtt.
- `CONCEPT_FOR_COLLECTION` / `FORMAT_CANDIDATE`: planerade användningar, inte färdiga aktiviteter.

## Varför grafen ger mer än taggar
En Fragglarna-figur kan filtreras efter TV/1980-tal, kopplas till ett generiskt **VHS-motiv**, därefter till prick-till-prick och planerad 1980-talsbok. En musikartist kan hitta en **mikrofon** via musikkontext utan att vi förfalskar artistens tidslinje eller kopierar porträttet. Själva relationerna är avsiktligt markerade som redaktionell association, inte faktabevis.

## Arkitekturbeslut
En enda redigerbar konceptpost kan återanvändas i flera format och produkter. Ingen massgenerering av ytterligare 485 dubblettdokument görs. Den nya grafen skapas deterministiskt från registren och förhindrar manuellt underhåll av ett växande korsproduktnät.
