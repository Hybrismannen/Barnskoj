# Revisionsunderlag – Barnskoj, 2026-11-20

## 1. Syfte och faktisk produkt
Barnskoj ska vara **ett brett aktivitets- och motivationsbibliotek för barn, unga och vuxna**, med generationsteman 1950–2025, illustrerade originalmotiv, prick-till-prick, mandala, målarbilder och senare digitala aktiviteter. Fiktiva kulturfigurer och verkliga personer är referensbibliotek som ger kulturhistorisk orientering, inte slutprodukten i sig.

## 2. Faktisk inventering före omvandlingen
- 485 entiteter (246 figurer/programanknutna, 184 personer/grupper och 55 universum).
- 90 käll-URL:er, 39 enskilda faktabelägg; Q0 191, Q1 257, Q2 37 och Q3 0.
- 17 obligatoriska attribut och 14 obligatoriska taggdimensioner per objekt; 8 245 attributrader och 8 086 taggkopplingar.
- Många parallella presentationer per entitet: kategori-CSV, samlad CSV, originalprofil, källdossier, standarddatakort, per-attribut-evidens och QA-export.
- Två aktivitetsfamiljer dokumenterade på förslagsnivå; ingen publicerad, testad utskrivbar aktivitet/illustrationsbok i GitHub vid revisionen.
- Ingen dokumenterad licens för reproduktion av skyddade figurer, porträtt eller logotyper.

## 3. Diagnos — grundläggande obalans
**Metadataexpansion utan motsvarande kreativa originalassets.** Ett växande system av dubblerade filer/CSV-exporter ger en falsk upplevelse av täckning och fler uppdateringsytor, medan faktiskt användbart barn-/vuxenmaterial är 0. Strukturell dataparitet är inte faktaparitet.

| Problem | Konsekvens | Genomförd motåtgärd |
| --- | --- | --- |
| Person/figur/universum är isolerade från produkter | Ingen enkel väg till faktisk aktivitet | Sammanlänkad discovery-graf med teman, motiv, format, epoker och bokkollektioner |
| Källtagg och faktabelägg blandas lätt ihop | Överskattad sanningsgrad | Strikt åtskillnad mellan faktabärande claim och redaktionella kopplingar |
| Parallella manuella representationer | Hög synk- och versionsskuldsrisk | Kanoniska indata + deterministisk discovery-generator och CI-färskhetskontroll |
| Kulturreferenser blandas med upphovsrätt | Publiceringsrisk | Originalmotiv separerade från kända figurer; rättighetsgrind på varje kreativ tillgång |
| Epok = kulturens ursprung = människans barndom | Felaktiga nostalgiurval | Egen epok-/bokmodell, inga obelagda årtal sätts på personer |
| CDX saknas | Ingen uttrycklig rätt styrkedja | Deklarerat lokalt, versionspinnat CDX 1.0-ankare; central admission ej påstådd |
| Manuell korsprodukt mellan många entiteter | Explosion av irrelevanta kopplingar | Högst två tydligt markerade idéförslag per entitet, sorterade efter matchstyrka |

## 4. Nya relationella lager (installerade)
1. **Evidence graph:** faktapåståenden → källa → specificerad entitet. Bevarar exakt evidensgräns.
2. **Reference graph:** figur → universum, alias → kanoniskt objekt, entitet → ärvda ämnes- och epoktaggar. Kataloguppgifter får inte förvandlas till oberoende faktakällor.
3. **Creative graph:** originalmotiv → tema, associerad epok, format och bokkollektion. Koncept är ej utförda assets.
4. **Discovery links:** researchentitet → föreslaget originalmotiv, max 2 per entitet via temalikhet/epok. Aldrig en licensierad figuråtergivning.

[Grafens dokumentation](../discovery/README.md) · [Aktivitetskoncept](../creative/README.md) · [Genererade sökvyn](../discovery/search.csv).

## 5. Effektivisering och migreringsgräns
**Behåll befintliga register oförstörda tills datakonsumenter är kartlagda.** Nu är `catalog/entities.csv`, evidensregister, motiv-/tema-/formatkällor och bokkollektioner explicita inputs för discovery. Grafindex, korslänkar och mätetal är deterministiskt **genererade** — ändra dem inte för hand. Byggscriptet går utan nätverk och CI avvisar föråldrade outputs.

Kvarstående strukturellt behov: större datamigration till en enda faktiskt redigerbar entitetskälla. Idag är `catalog/entities.csv` gemensamt läsgränssnitt, men person/figur/universumsfiler och standarddatakort innehåller dubbletter. Att radera dem utan consumer-audit skulle bryta befintliga länkar och testsystem. Föreslagen nästa migration: besluta kanonisk write path per attribut, generera alla andra vyer, installera diff-/migreringsverifiering och därefter arkivera äldre duplicerade presentationer.

## 6. Vad som återstår och varför
- **Aktivitetsproduktion:** skapade SVG, testade PDF:er, facit, A4/A5-mallar, grafisk profil, tryckbarhet, begriplighet och tillgänglighet. Behövs för att Barnskoj ska vara ett bibliotek **att använda**, inte bara utforska.
- **Full verifiering:** Q0/Q1/Q2 → Q3 inklusive publicerings- och biografisk precision där det verkligen behövs. Behövs för faktarutor och historisk korrekthet; behöver inte bromsa en självständig illustrationsoriginal på ett generiskt föremål.
- **Rättighetsunderlag:** tillgångstyp, ägare, tillstånd, användningsområde, kommersiell/ideell omfattning, territorium, datum. Skilda beslut per faktisk asset.
- **Redaktionell curering:** barn-/vuxen-/generationsserier, svårighetsgrader, motivvariation, inkludering och empirisk användartestning. Behövs för upplevt värde.
- **Identitetsnormalisering:** verkliga programledare ligger ännu i figurregister; alias behöver dokumenterade kvalitetsbeslut. Migrera först med bevarade ID och referenser.
- **Publikt gränssnitt:** sökning/filter/förhandsbild och nedladdning är planerat, inte implementerat. Ska byggas ovanpå reproducerbara index, inte nya manuella datakopior.
- **CDX Estate Registry:** Barnskoj saknas i den centrala snapshot som granskades. Lokal declaration är första steg; central admission, oberoende verifikation och eventuell framtida runtime-gate är separata beslut.

## 7. Rekommenderade konkreta nästa leveransgrindar
- **WP-A:** tre trycktestade originalaktiviteter ur olika familjer; giltiga separata facit, tillgänglighetsgranskning.
- **WP-B:** centraliserat write-model för entiteter och källor samt automatiskt genererade legacy exports; oförändrade permanenta ID.
- **WP-C:** tre kuraterade vuxen-/barnserier med 10–20 motiv vardera och verifierad rättighetsprocess.
- **WP-D:** katalogens publika sök-/filterflöde (baserat på nuvarande `discovery/search.csv`) och kvalitativ testning.
- **WP-E:** central CDX-admission/independent verification med separat runtime-bedömning om en publik tjänst byggs.

## Kvalitetsbedömning
**Dataintegritet: fungerande. Grafbaserad uppdaterbarhet: implementerad som ny byggbar vy. Innehållsproduktion: ännu inte genomförd. Factual verification: ofullständig. Rättighetsklarering: ej genomförd. CDX: lokalt deklarerat, ej centralt verifierat.**
