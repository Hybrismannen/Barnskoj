# Vektorprototyper – WP03

Tre verkliga **A4-punktrutter med separata SVG-facit** utgör ett end-to-end-test av Barnskojs kreativ- och produktionsflöde.

| Aktivitet | Motiv | Antal prickar | Original | Facit |
| --- | --- | ---: | --- | --- |
| BS-ACT-0001 | Jukebox | 55 | [SVG](prototypes/BS-ACT-0001.svg) | [SVG](solutions/BS-ACT-0001.svg) |
| BS-ACT-0002 | Discokula | 48 | [SVG](prototypes/BS-ACT-0002.svg) | [SVG](solutions/BS-ACT-0002.svg) |
| BS-ACT-0003 | Arkadmaskin | 47 | [SVG](prototypes/BS-ACT-0003.svg) | [SVG](solutions/BS-ACT-0003.svg) |

Motiven är generiska, egenproducerade enkla konturer utan kända figurer/porträtt, varumärken eller hämtade bilder. De får **inte** upphöjas till rättighetsklarerade/published utan manuell bedömning och trycktest.

**Bygg och kontrollera**
```bash
python scripts/build_prototypes.py
python scripts/build_prototypes.py --check
python scripts/validate_svg_prototypes.py
python scripts/validate_production.py
```

**Automatiska kontroller:** A4 210 × 297 mm, säker utskriftsyta, sammanhängande numrering 1–N, nummeretiketter matchar prickar, minsta avstånd för intilliggande prickar 6 mm, facit har exakt samma koordinatorutt, alla 6 assets registrerade och inga publiceringsgrindar markeras PASS utan mänsklig kontroll.

**Inte genomfört:** manuell läsbarhetsgranskning, utskriftsskala på fysisk skrivare, användartest, full tillgänglighetsutvärdering, ägar-/licensbeslut, publiceringsbeslut och PDF-export. SVG-filerna är tekniska prototyper.
