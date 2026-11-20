# Barnskoj – systemarkitektur och uppdateringsvägar

## Utgångspunkt
Tre åtskilda sanningslager: **evidence** (belagda sakuppgifter), **editorial discovery** (kreativa kopplingar och koncept) och **production** (faktiskt skapade och kvalitetsklarerade aktiviteter/assets). Ingen tagg eller kreativ koppling ger rätt att reproducera en skyddad figur eller kändis.

## Databeroenden efter DevOps WP01–03
```text
KÄLLREGISTER (redigeras)
catalog/source/entities_base.csv  ───┐
catalog/source/legacy_details.csv ────┤
tags/assignments.csv ─────────────────┤
evidence/claims.csv + field_proofs.csv ┼── scripts/build_catalog.py
sources/registry.csv ─────────────────┘          │
                       ┌─────────────────────────┘
                       ↓
     catalog/entities.csv, characters.csv,
     celebrities.csv, universes.csv,
     quality/*.csv, evidence/attribute_evidence.csv,
     records/*.md  (GENERERADE)

creative/*.json ─┐
production/*.csv ├─ scripts/build_discovery.py ── discovery/*.csv + metrics.json
catalog/*.csv ───┘

production/prototype_specs.json ── scripts/build_prototypes.py
                                    ├─ 3 SVG-aktiviteter
                                    └─ 3 separata SVG-facit
```

[DevOps-kontrakt](../devops/WORKPACKAGES.md) · [En kanonisk skrivväg](../catalog/source/README.md) · [Produktionskontroll](../production/RELEASE_GATE.md).

**Det som fortfarande skrivs manuellt:** redaktionella `profiles/*` och `sources/entity-dossiers/*` samt identitets- och källdeklarationer där egna källor krävs. Omformning av 485 standarddatakort är däremot automatiserad och exakt diffkontrollerad i CI.

## Relationernas betydelse
- Identitet: alias → kanonisk person; figur → universum.
- Forskning: claim → entitet och exakt käll-ID; belägget styr bara den angivna uppgiften.
- Upptäckt: entitet → kulturtema/associerad epok; motiv → tema/format/bokkollektion.
- Redaktionella förslag: högst två originalmotiv per entitet, märkta som idé och **ej licensierade porträtt/karaktärer**.

## Exempel
Fragglarna → tv/1980-tal → generiskt VHS-originalmotiv → prick-till-prick → 1980-talskollektion. Detta är redaktionell inspiration, inte ett påstående att en figurs bild förekommer på en VHS och inte rättighet att återge figuren.

## Vad som fortfarande måste rationaliseras
1. **Entitetsmigrering:** Införd gemensam skrivväg och generator för äldre register samt 485 datakort. Separata redaktionella profiler och källdossierer kräver fortsatt mänsklig kvalitetsgranskning.
2. **Verifieringsgrad:** Q0 191, Q1 257, Q2 37, Q3 0. Researchdjup är inte lösbart med flera tomma metadatafält.
3. **Grafisk produktion:** 32 motivkoncept och nu 3 A4-originalprototyper med 3 SVG-facit. Ingen fysisk trycktestning, PDF-utgåva eller publicerad bok.
4. **Rättigheter:** inga godkända licenser eller porträttreproduktionsbeslut. Alla konkreta assets måste prövas separat.
5. **Användargränssnitt:** sökindex finns; publik webbläsare, preview och nedladdning saknas.
6. **CDX:** lokalt ankare deklarerat; central registrering, oberoende verifikation och eventuell runtime är ännu inte genomförda.

## Fortsatt arbetsordning
Uppdatera kanonisk källdata → generera alla vyer → kör 10 lokala kontrollgrindar → begär mänsklig granskning inför publicering. Avlägsna inte äldre profil- och källdossierer utan en särskild consumer-audit. Produktion av verkliga aktivitetsblad bör gå parallellt, inte vänta på Q3 för orelaterade generiska originalmotiv.
