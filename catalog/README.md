# Referensbiblioteken – Barnskoj

Här samlas researchposter om **fiktiva figurer/programvärldar** och **verkliga kända personer**. Katalogen är ett metadata- och inspirationsregister, **inte ett bibliotek av bilder som får återanvändas**.

## Kanonisk skrivmodell
Det redigerbara masterregistret är [source/entities_base.csv](source/entities_base.csv) tillsammans med [source/legacy_details.csv](source/legacy_details.csv); faktabelägg och taggkopplingar är separata inputs. **Ändra inte `entities.csv` eller kategorivyer direkt.** Kör `python scripts/build_catalog.py` och `python scripts/build_discovery.py` samt hela [DevOps-testkedjan](../devops/RUNBOOK.md).

## Gemensam standard
[Alla 485 entiteter](entities.csv), inklusive 55 [universum](universes.csv), har samma 17 attribut och 14 obligatoriska taggdimensioner. Se [paritetsstandard](../docs/PARITY_STANDARD.md) och [forskningsgap](../quality/RESEARCH_PARITY.md). Äldre separata listor finns kvar för kategoriserad sökning och är synkroniserade mot det kanoniska registret.

## Register
- [Fiktiva figurer och världar](characters.csv): 246 poster från en bredare uppsättning franchises/programvärldar; alla poster har status `research_candidate`.
- [Verkliga kändisar](celebrities.csv): 184 poster från musik, sport, film/tv och andra profiler; alla poster har status `research_candidate`.
- [Fördjupning om barnprogram och kulturarv](heritage.md)
- [Licens- och publiceringspolicy](../docs/RIGHTS.md)

## Arkitektur
**Referensobjekt** (person/figur/universum) ↔ **aktivitet** (prick-till-prick, quiz, labyrint, målarbild, memory etc) ↔ **asset** (redigerbar bild, utskrift, facit).

En referens kan förekomma i flera aktiviteter utan att vi duplicerar grunddata. Exakta namn används för sökbar research. För produktion krävs rättighetsprövning per konkret asset och användning. Alternativet är att skapa ett självständigt originalmotiv utan förväxlingsrisk.

## Individuella fördjupningsregister
Varje CSV-rad har `profile_path` med direkt länk till en Markdownfil under [profiles/characters](../profiles/characters/) eller [profiles/people](../profiles/people/). Länkarna är kontrollerade mot repository-trädet (430/430 matchar). 36 entiteter har minst ett kontrollerat faktapåstående; övriga behöver kompletterande sourcing. Se [källregistret](../sources/registry.csv) och [biblioteksrevisionen](REGISTRY_AUDIT.md).

## Källdossierer
Nu finns även `source_dossier_path` i båda CSV-katalogerna. [430 individuella källdossierer](../sources/entity-dossiers/) är länkade till respektive profil och listar registrerade source-ID och källornas begränsningar. Se [täckningsmätningen](../sources/COVERAGE_DASHBOARD.md) för verkliga luckor.

## Katalogens referenssystem
- [Taggar och facetter](../tags/README.md)
- [55 universumsprofiler](universes.csv)
- [Identitets- och aliasregister](identity_registry.csv)
- [39 atomära belägg](../evidence/claims.csv)
- [430 individuella kvalitetsgrader](../quality/entity_quality.csv)

## Kvalitetsstatus
`research_candidate → source_checked → rights_checked → usable_reference`. En referenspost som inte klarat detta flöde får inte publiceras som en godkänd bildresurs.

## Uppdatering
Årlig redaktionell översyn för samtida trender; historiska namn får stå kvar för generationsbredd. Datum, genre och roll ska verifieras på objektnivå innan redaktionell användning. Inga topplistor eller popularitetsanspråk finns i denna första provbank.
