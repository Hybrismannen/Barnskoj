# Levande universumkällor – Barnskoj

**10 franchisegrupper**, **29 länkade wiki-/ägarsidor** och **9 iscensatta, ännu ej kanoniserade figur-/personvarianter**. De befintliga 485 ID:na bevaras orörda tills varje nytt objekt har genomgått identitets- och versionsgranskning.

- [Franchisekorsning](franchises.csv): samma berättelse kan ha olika ägare och versioner (bok, film, serietidning, spel).
- [Wiki- och originalägares källor](wiki_sources.csv): källa klassad som `rights_holder`, `fan_wiki` eller `independent_wiki`.
- [Staging för nya karaktärer](staged_entities.csv): Daenerys/Khaleesi, Gandalf, Iron Man, Batman, Spider-Man, Harry Potter, Luke Skywalker.
- [Länkar till befintliga entiteter](entity_source_links.csv): Muppet/Sesame, Star Wars, Pokémon, Disney och Mumin.
- [Källövervakning](watch-state.json) och [ändringskö](change-backlog.csv): algoritmisk uppdateringsrutin, men aldrig automatisk faktaverifiering.
- [Käll- och rättighetspolicy](../rights/README.md).

## Sourcinghierarki och uppdateringar

**Originalutgivare/rättighetshavare** har större auktoritet för publikationshistorik, medverkan och juridisk hantering än en fan-wiki. **Fan-wikis** bidrar med mer detaljerade figurrelationer, kontinuiteter, böcker/avsnitt och upptäckter som kräver kontroll. En publicerad fan-wiki-ändring skapar ett *granskningsärende*, inte ett nytt automatiskt faktum i `catalog/entities.csv`.

Staginggraden är `STAGED_NOT_CANONICAL`: alla kontinuitetsvarianter, t.ex. Daenerys i HBO:s tv-serie respektive Martin-böckerna, får varsin källkoppling tills samma eller skilda kanoniska identiteter har fastställts. Utan denna separation kan filmstillbilder, böcker, lore och illustratörsrätt lätt förväxlas.

**Licensgräns:** Fandoms wiki-text licensieras normalt CC BY-SA 3.0, men bilder och skyddade karaktärsmotiv har separata rättigheter. Ingen Fandom-bild kopieras automatiskt till Barnskoj.
