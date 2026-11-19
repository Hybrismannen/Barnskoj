# Barnskoj

**Lek, skapa, klura och upptäck.**

Barnskoj är ett öppet och växande bibliotek med roliga aktiviteter för barn, unga och vuxna – från lekfulla barnblad till nostalgiska illustrations- och aktivitetsböcker för vuxna. Här ska det finnas både utskrivbara material och, på sikt, digitala aktiviteter som kan användas hemma, i skolan, på fritids eller tillsammans med andra.

> Status: Grundstruktur v0.1. Innehållsidéer är inte färdigproducerade eller kvalitetssäkrade aktivitetsblad.

## Hitta något roligt

| Bibliotek | Innehåll | Status |
| --- | --- | --- |
| [Prick till prick](library/prick-till-prick/README.md) | Motiv från vardag, sport, gaming och populärkultur 1950–2025 | Planerat |
| Måla & skapa | Målarbilder, pixel art, symmetri, teckning | Planerat |
| Klurigt & smart | Labyrinter, sudoku, rebusar, logik | Planerat |
| Ord & språk | Ordsök, korsord, hemliga meddelanden | Planerat |
| Spel & utmaningar | Bingo, memory, skattjakter | Planerat |
| Bygg & konstruera | Pappersmodeller, origami, byggutmaningar | Planerat |
| Experiment | Naturvetenskap, optiska illusioner | Planerat |
| Rörelse & äventyr | Hinderbanor, utomhusuppdrag | Planerat |
| Musik & rytm | Ljudbingo, rytmlekar, musikquiz | Planerat |
| Tillsammans | Samarbetslekar, familje- och gruppuppdrag | Planerat |

## Generationer och kulturarv

Samma bibliotek täcker **1950-talet till 2025 och vidare**. Det går att filtrera efter både **motivets epok** och **målgrupp**. Vuxnas böcker med minnen från barndomen ska ha egen redaktionell stil och komplexitet, inte marknadsföras som barnarbetsblad.

- [Generationsbiblioteket 1950–2025](catalog/decades/README.md)
- [Vuxenformat: nostalgiska prick-till-prick och mandalaböcker](library/adult-nostalgia/README.md)
- [Figurbibliotek, 246 researchposter](catalog/characters.csv)
- [Kändisbibliotek, 184 researchposter](catalog/celebrities.csv)
- [Kulturarv och barnprogram](catalog/heritage.md)
- [Rättighetspolicy](docs/RIGHTS.md)

## Principer

- **Roligt först:** Innehåll ska väcka lust och nyfikenhet, inte upplevas som en skoluppgift.
- **Valfrihet:** Barn kan välja efter intresse, inte kön eller snäva åldersnormer.
- **Flera sätt att delta:** Anpassningar för motorik, perception, läsning och koncentration.
- **Lätt att använda:** Utskrifter i A4 och tydliga instruktioner; digitalt när det tillför värde.
- **Barncentrerat:** Ingen insamling av barns personuppgifter som standard.
- **Lagligt att dela:** Originalmaterial eller tydligt licensierat material; kända varumärken och karaktärer används inte som frikort för kopiering.
- **Verifierbar kvalitet:** Varje aktivitet testas före publicering.

## Referensbibliotek och källor
- [430 individuella fördjupningsregister](catalog/README.md) — 246 figurer och 184 personer/grupper, alla med egna länkade profiler
- [Sourcing- och källregister](sources/registry.csv) — 90 registrerade källposter
- [Registerrevision och begränsningar](catalog/REGISTRY_AUDIT.md)

Fördjupningsregistren byggs stegvis. 36 entiteter har avgränsade faktabelägg (Q2), 240 har ännu endast källspår (Q1) och 154 saknar källa (Q0); ingen är fullständigt djupgranskad (Q3). Ingen profil innebär rätt till ett fotograferat eller illustrerat originalverk.

### Individuella källdossierer
Alla 430 entiteter har [en fördjupningsprofil](profiles/) och [ett källdossier](sources/entity-dossiers/) länkade via katalogen. [Aktuell kvalitetsrapport](quality/COVERAGE.md) visar Q0 154, Q1 240, Q2 36 och Q3 0. Endast Q2-posterna har något specificerat faktabelägg; inget objekt har därmed godkänts för kopiering eller kommersiell bildproduktion.

## Taggsystem och evidens
- [117 taggar och 2 813 kopplingar](tags/README.md)
- [55 universum](catalog/universes.csv)
- [Identitet och alias](catalog/identity_registry.csv)
- [39 kontrollerade faktabelägg](evidence/claims.csv)
- [Aktuell kvalitetsrevision](quality/COVERAGE.md)
- [Automatisk CI-validering](.github/workflows/catalog-validation.yml)

## För utveckling

- [Produktvision och mål](docs/PRODUCT.md)
- [Innehållsmodell och metadata](docs/CONTENT_MODEL.md)
- [Roadmap](docs/ROADMAP.md)
- [Bidrag och kvalitetskontroll](CONTRIBUTING.md)

### Projektstruktur

```text
Barnskoj/
├── README.md
├── CONTRIBUTING.md
├── docs/
│   ├── PRODUCT.md
│   ├── CONTENT_MODEL.md
│   └── ROADMAP.md
└── library/
    └── prick-till-prick/
        └── README.md
```

**Versionsprincip:** Idéer, prototyper och publicerat material hålls åtskilda. Ingen aktivitet markeras som färdig innan utskrift/användning har kontrollerats.
