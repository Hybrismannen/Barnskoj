# Kvalitetsdjup – audit 2026-11-19

## Mätbar täckning
| Mått | Utfall |
| --- | ---: |
| Katalogposter totalt | 430 |
| Figurer/programanknutna | 246 |
| Personer/grupper | 184 |
| Universum | 55 |
| Källa-URL:er i register | 89 |
| Granskade källsidor (avgränsad omfattning) | 13 |
| Atomära källbelagda påståenden | 39 |
| Q2: minst ett verifierat påstående | 36 |
| Q1: endast källingångar | 240 |
| Q0: inga registrerade källingångar | 154 |
| Q3: fullständigt djupverifierad | 0 |
| Alias-/cross-catalog-rader | 2 |
| Verkliga programledare ännu i figurkatalog | 5 |
| Käll-ID som saknar registerträff | 276 |
| Godkända bildrättigheter | 0 |

## Åtgärder genomförda
1. Normerad taggtaxonomi och entitet↔tagg-kopplingar.
2. Separat universumsregister med egna profiler och figurlänkar.
3. Identitetsalias och särskiljning av likalydande namn.
4. Synkroniserade alla 430 enheters källdossier mot **nuvarande** källkatalog och claims (ersätter tidigare inaktuella dossierlistor).
5. Publicerings- och källgrindar separerade, samt per-entity audit-rad.
6. Källkontrollerade atomära faktapåståenden med exakt källankare.

## Identifierade systemfel
- 154 saknar käll-URL; 240 har källspår utan faktakontroll.
- Ärvda epokintervall representerar **associerad period**, inte verifierad individuell debut eller svensk sändningshistoria.
- Verkliga barn-tv-programledare förekommer i figurkatalogen och kräver en framtida skonsam datamigrering.
- De två registren har i huvudsak stora engelskspråkiga/globala universum, vilket bör kompletteras med svensk och annan regional kulturhistoria.
- De flesta figur- och personporträtt är skyddade; 0 rättigheter godkända för offentlig bokutgivning.
- Vissa äldre käll-URL:er har katalogstatus 'verified' men har ännu inte provats på nytt. Endast de 13 i `evidence/source_checks.csv` är här påståendespecifikt granskade.

## Prioriterad kvalitetskö
**P0** Identitet/alias, full synk och URL-integritet (implementerat strukturellt).  
**P1** Källbeläggning av de 154 Q0-posterna och de 240 Q1-posterna.  
**P2** Djupverifiera barn-tv 1950–1990 (upphov, svenska versioner, datum, figurrelationer).  
**P3** Licens- och tryckgranskning för konkreta serier av prick-till-prick och mandalaböcker.

**Utvärderingsregel:** Ärlig Q2-status är bättre än falskt Q3-godkännande.
