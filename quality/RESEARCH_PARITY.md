# Barnskoj – forskningsparitet och rättighetsgrind v2.0

## Krav
**Alla entiteter ska ha samma verifieringskrav**, men likvärdig forskning uppnås först när varje entitet har genomgått kontrollerna. Vi accepterar inte att ett objekt sägs vara fullständigt granskad på grund av ett ifyllt formulär eller en ospecificerad URL.

### Samma fält och taggar (PASS)
- 485 av 485 har 17 obligatoriska attribut och 14 kontrollerade taggdimensioner.
- 485 individuella standarddatakort, 485 fördjupningsprofiler och 485 individuella källdossierer.
- [Attributmatris](../evidence/attribute_evidence.csv), [entitetsregister](../catalog/entities.csv), [paritetsmatris](entity_parity.csv).

### Faktisk källverifiering (BLOCKED)
| Forskningsnivå | Entiteter | Kräver |
| --- | ---: | --- |
| Q0 – ingen källa | 191 | Verifiera en objektspecifik primärkälla |
| Q1 – bara källspår | 257 | Lägg till enskilda faktapåståenden och källställen |
| Q2 – delvis faktaverifierad | 37 | Fördjupa historik, utgåvor och konfliktkontroll |
| Q3 – fullständigt verifierad | 0 | Redaktionellt signerad dossier |

**Den faktiska faktapariteten är alltså ännu inte uppnådd.** 448 objekt saknar även Q2-nivå. Alla 485 behöver ytterligare arbete för Q3.

### Obligatorisk Q3-checklista per entitet
1. Fastställ identiteten, alias och exakt entitetstyp med objektspecifik källa.
2. Verifiera historiskt ursprung/debut eller dokumentera kontrollerat att uppgiften saknas.
3. Verifiera upphovsperson/producent och originalmedium, eller dokumentera kontrollerad frånvaro.
4. Skilj första svenska förekomst från global premiär och nostalgisk målgruppsperiod.
5. Verifiera centrala verk, karaktärsrelationer eller idrotts-/musikmeriter.
6. Kontrollera flera relevanta källor, jämför motstridiga uppgifter och ange exakta källställen och granskningstid.
7. Dokumentera redaktionell sign-off. Behåll bild- och porträtträttigheter som separat produktionsspärr.

## Förvaltning
[Kvalitetsarbetskön](RESEARCH_BACKLOG.csv) innehåller en tydlig uppgift för varje entitet. [Strikt validator](../scripts/validate_parity.py) testar strukturen; [Research gate](../scripts/check_research_readiness.py) testar om alla objekt uppnått begärd lägstanivå.

**Releasepolicyn:** Inga skyddade porträtt eller figurer får publiceras utan produktspecifik rättighetskontroll även om Q3 nåtts. En viss fristående originalillustration kan lanseras separat enligt gällande rättighetsgrind.
