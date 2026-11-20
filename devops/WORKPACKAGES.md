# Barnskoj DevOps — tre genomförda arbetspaket

**Omfattning:** 2026-11-20 · Repository `Hybrismannen/Barnskoj` · branch `main` · inga ytterligare WP i denna iteration.

| WP | Leverans | Automatiserad acceptans | Mänsklig kvarstående grind |
| --- | --- | --- | --- |
| **WP01** – kanonisk data | 485 entiteter i `catalog/source/entities_base.csv`, 485 kategoriunika tillägg och 6 verifikationsankare; genererade register, QA-vyer och exakt synkroniserade 485 datakort | `build_catalog.py --check`, `validate_catalog.py`, `validate_parity.py`, mutationstest | Verifiera fortsatta forskningsluckor och redaktionella dossierer |
| **WP02** – DevOps-kvalitet | Samordnade CI-grindar för register, graf, SVG, publiceringsspärr och CDX; adversarialtester för källmanipulering och felaktig publicering; ett lokalt driftkommando | `python scripts/doctor.py`; GitHub Actions kräver PASS | Central CDX-admission och oberoende governance-verifikation sker separat |
| **WP03** – fungerande aktivitetskedja | 3 originala, reproducerbara A4-punktblad (55/48/47 punkter) samt 3 facit; 6 registrerade SVG-assets; aktivitet→motiv→format→asset i grafen | `build_prototypes.py --check`, `validate_svg_prototypes.py`, `validate_production.py`, `build_discovery.py --check` | Verklig pappersutskrift, test med användare, licens-/ägarbeslut, tillgänglighets- och human review |

## Acceptance state
- **Tekniska leverabler:** Implementerade i GitHub, automatiska regressionstester. [Katalogens CI-status](https://github.com/Hybrismannen/Barnskoj/actions/workflows/catalog-validation.yml).
- **Forskningsnivå:** Q0=191, Q1=257, Q2=37, Q3=0. Ingen kvalitetsuppblåsning.
- **Kreativt arbete:** 32 idékoncept; **3 produktionsprototyper**, 6 SVG-filer; **0 publicerade**.
- **Graph:** 689 noder, 3 085 relationer, 704 redaktionella korskopplingar.
- **CDX:** `ANCHOR_DECLARED / NOT_VERIFIED`. CDX-ankaret är lokalt CI-granskat men ännu inte centralt upptaget/verifierat; ingen consequential runtime.

## Förändringsgräns
Detta är max **tre** WP, inte en ny arkitekturplan. WP01 migrerar kompatibilitetsvyer men raderar inte historiska redaktionella dossierer eller deras källspår. WP02 kör defensiva tester men gör ingen automatisk extern distribution. WP03 levererar faktisk prototyp, inte en godkänd bok/PDF.

**Nästa möjliga beslut efter denna iteration:** påbörja mänskligt test och rättighetsgranskning för WP03-prototyper. Detta kräver separat publiceringsbeslut – inte ytterligare WP inom denna leverans.

## Prospektiv styrning efter användardirektiv 2026-11-20
De historiska WP01–WP03 behåller sina faktiska commits och tekniska PASS. **Före en ny arbetsomgång eller nytt genomförandegodkännande krävs nu** publicerad och remote-verifierad GitHub Wiki samt full originalbildsproveniens för alla 526 aktuella bildbehov. Separata rättighetsbeslut för kommersiell bokutgivning kvarstår även efter sourcing. [Maskingranskad blockeringsstatus](PRE_WP_STATUS.json) och [Wiki-först-instruktion](../docs/WIKI_WORKFLOW.md).
