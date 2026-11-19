# Innehållsmodell – Barnskoj v0.1

Modellen skiljer **den gestaltade epoken** från **vem som ska använda materialet**. En person född på 1960-talet kan ha starka barndomsminnen även från 1970-talet; detta är inte samma metadatafält.

Varje aktivitet får en egen mapp med metadata, tillgångar och eventuell instruktion.

## Obligatoriska metadata
| Fält | Exempel | Regel |
| --- | --- | --- |
| id | BS-DTD-0001 | Unik, permanent identifierare |
| title | Retro-robot | Kort svensk titel |
| category | prick-till-prick | En huvudkategori |
| themes | retro, robot, teknik | Flera sökbara intressen |
| era | 1960s | Motivets kulturhistoriska årtionde, inte användarens födelsedecennium |
| audience | adult | child, teen, adult, intergenerational; kan vara flera |
| nostalgia_theme | svensk-tv | Valfria motiv- och kulturteman |
| product_series | 60-talets barndom | Valfri bok-/serieanknytning |
| age_guide | 8–11 | Vägledande, ej exkluderande |
| difficulty | 1–5 | Relativ svårighetsgrad |
| duration_minutes | 15 | Uppskattning som ska testas |
| participants | 1 | Antal, eller intervall |
| materials | papper, penna | Vad som behövs |
| format | print-a4 | En eller flera versioner |
| instructions | Förbind prickarna i nummerordning | Kort, tillgängligt |
| accessibility | stor text, rymliga punkter | Anpassningar |
| rights_status | original | original, licensed, restricted-reference |
| source_or_license | egen originalillustration | Upphov och rättighetsgrund |
| review_status | idea | idea, prototype, tested, published |
| version | 0.1.0 | Semantisk innehållsversion |

## Bok- och vuxenutgåvor
- `audience` kan vara `adult` eller `intergenerational`.
- `book_collection_id`, `spread_order`, `print_trim_size`, `binding_margin_mm`, `complexity`, `generation_context`.
- Ett **mandalamotiv** kan ha tema hämtat från kulturhistoria men ska vara en självständig och rättighetsgranskad design, inte kopiering av kända figurer/logotyper.
- Källmetadata och licens/porträtträtt följer med även när samma motiv återanvänds i flera format.

## Extra för prick-till-prick
- dot_count
- sequence_validation: samtliga nummer unika och sammanhängande
- min_dot_spacing_mm
- page_orientation
- silhouette_readability
- solution_asset

## Mappmönster
```
library/<category>/<activity-id>/
  activity.yaml
  README.md
  source/
  print/
  solution/
```

## Exempel – ej publicerad aktivitet
```yaml
id: BS-DTD-0001
title: Retro-robot
category: prick-till-prick
themes: [retro, robot, teknik]
era: 1980s
age_guide: "8–11"
difficulty: 2
duration_minutes: 15
participants: 1
materials: [papper, penna]
format: [print-a4]
instructions: "Dra streck från 1 till sista siffran i ordning."
accessibility: [tydliga_siffror, hög_kontrast]
rights_status: original
source_or_license: "Eget originalmotiv"
review_status: idea
version: "0.1.0"
dot_count: null
```

Dessa metadata är en föreslagen specifikation, inte en uppgift om färdigproducerat material.
