# Barnskoj – systemarkitektur och uppdateringsvägar

## Utgångspunkt
Tre åtskilda sanningslager: **evidence** (belagda sakuppgifter), **editorial discovery** (kreativa kopplingar och koncept) och **production** (faktiskt skapade och kvalitetsklarerade aktiviteter/assets). Ingen tagg eller kreativ koppling ger rätt att reproducera en skyddad figur eller kändis.

## Databeroenden
```text
catalog/entities.csv ─┐
sources/registry.csv ──┤
evidence/claims.csv ───┤
creative/*.json ───────┼── scripts/build_discovery.py
decade collections ────┤       ├── discovery/nodes.csv
production/*.csv ──────┘       ├── discovery/edges.csv
                               ├── discovery/crosslinks.csv
                               ├── discovery/search.csv
                               └── discovery/metrics.json
```

**Primära redigerbara inputs:** evidensregister, motiv-/tema-/formatkataloger, decennieserier och produktionsjournaler. `catalog/entities.csv` är gemensam **läsvy**, men äldre separata person-/figur-/universumsregister kräver fortfarande synkronisering.

**Genererade, ej manuellt redigerbara outputs:** alla `discovery/*`. CI kör generatorn i `--check` och blockerar drift.

## Relationernas betydelse
- Identitet: alias → kanonisk person; figur → universum.
- Forskning: claim → entitet och exakt käll-ID; belägget styr bara den angivna uppgiften.
- Upptäckt: entitet → kulturtema/associerad epok; motiv → tema/format/bokkollektion.
- Redaktionella förslag: högst två originalmotiv per entitet, märkta som idé och **ej licensierade porträtt/karaktärer**.

## Exempel
Fragglarna → tv/1980-tal → generiskt VHS-originalmotiv → prick-till-prick → 1980-talskollektion. Detta är redaktionell inspiration, inte ett påstående att en figurs bild förekommer på en VHS och inte rättighet att återge figuren.

## Vad som fortfarande måste rationaliseras
1. **Centralt entitets-write-model:** `characters.csv`, `celebrities.csv`, `universes.csv`, `entities.csv`, `records/*` och dossierer innehåller överlapp. Behåll existerande permanenta ID, kartlägg konsumenter och inför generator för sekundära vyer *innan* något tas bort.
2. **Verifieringsgrad:** Q0 191, Q1 257, Q2 37, Q3 0. Researchdjup är inte lösbart med flera tomma metadatafält.
3. **Grafisk produktion:** 32 motivkoncept men ännu 0 SVG/PDF, trycktest, facit eller publicerade böcker.
4. **Rättigheter:** inga godkända licenser eller porträttreproduktionsbeslut. Alla konkreta assets måste prövas separat.
5. **Användargränssnitt:** sökindex finns; publik webbläsare, preview och nedladdning saknas.
6. **CDX:** lokalt ankare deklarerat; central registrering, oberoende verifikation och eventuell runtime är ännu inte genomförda.

## Fortsatt migreringsordning
Kartlägg läs-/skrivkonsumenter → välj kanonisk skrivväg → generera äldre exportvyer → jämför diff och versionshistorik → testa länkstabilitet → arkivera överflödiga manuella kopior. Produktion av verkliga aktivitetsblad bör gå parallellt, inte vänta på Q3 för orelaterade generiska originalmotiv.
