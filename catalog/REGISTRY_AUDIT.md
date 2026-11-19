# Registeraudit – 2026-11-19

## Omfattning efter sourcing
- **246 figurposter**, inklusive historiska 1950–1970-talsvärldar.
- **184 kändis-/person-/grupposter**, med kompletterande musikhistoria, sport och svensk kultur.
- **430 individuella fördjupningsfiler**, konsekvent länkade från respektive CSV.
- **87 källposter**, varav flera är övergripande ingångar som inte validerar varje person eller figur.

## Styrkor
- Bra täckning av svensk nostalgisk barn-tv och globala populärkulturella universum.
- Separata domän-/figurreferenser och kreativa aktiviteter.
- Generationsspår 1950–2025; särskilt vuxna nostalgiböcker.

## Brister som återstår
1. Grundmaterialet har blandad entitetsnivå: fiktiva figurer, skådespelare/programledare och kollektiv som ”Doozers” i samma tabell. Typfält bör raffineras efter källkontroll.
2. Namn-/aliasdubletter och genrevariationer, exempelvis Armand Duplantis/Mondo Duplantis, måste normaliseras före användargränssnitt.
3. Ingen full individuell biografisk eller figurhistorisk granskning ännu: varje profil är ärligt märkt som researchkandidat.
4. Övergripande källor validerar inte 100-tals enskilda datapunkter; objektsidor måste hämtas och beläggas.
5. Ingen licens för personporträtt eller karaktärsdesign är förvärvad, inga publicerbara illustrationer har skapats.
6. En lek-/bokprodukt kräver också temakuratering, testad svårighetsgrad, upphovskontroll, facit och produktionsteknisk kontroll.

## Länk- och integritetskontroll
2026-11-19: 430 CSV-rader har 430 unika `profile_path` och samtliga 430 dokumentfiler hittades i GitHub-trädet. Profilerna är verkliga filer, inte obefintliga länkmål. **Detta validerar inte faktainnehållet.**

Fem prioriterade profiler har nu primärkällestött innehåll (Gobo, Elmo, Televinken, Skurt, Magnus). Källregistret utökat till 87; 430 enhetsspecifika källdossierer har skapats, men bara 23 poster har kandidatmatchning mot en direkt objektsida och 154 saknar fortfarande källa. För några poster har uppenbart felaktig typetikett rättats (verkliga programledare vs fiktiva figurer).

## Sourcingutvidgning — tredje etappen
- [Källdossierer](../sources/entity-dossiers/) är skapade för alla 430 registerposter.
- [Sourcing pass 2](../sources/SOURCING_PASS_2.md), [pass 3](../sources/SOURCING_PASS_3.md) och [täckningsrapport](../sources/COVERAGE_DASHBOARD.md) dokumenterar belägg, härledningsnivåer och kvarvarande luckor.
- Alla poster har en fysisk fördjupningsprofil och en fysisk källdossier. Ingen av detta betyder full individuell faktagranskning.

## Nästa researchpass – prioritering
P1: Fragglarna (fem huvudfigurer), Sesame Street (huvudensemblen), Televinken, Skurt, 1960-/1970-talets svenska barn-tv.  
P2: svenskt 1950–1990-musikarv, internationell rock/soul, fotbolls- och vinteridrottsikoner.  
P3: expansion till fler kulturer, nya språk och spel-/internetkultur samt samtida profiler.

## Godkännandemodell
Inget material går från `research_candidate` till `source_checked` utan individuell evidence-rad. Inget illustrerat material får `rights_checked` utan rättighetsbedömning för den konkreta användningen.
