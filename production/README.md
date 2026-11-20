# Barnskoj – skapande och publicering

Denna mapp är **den verkliga leveransjournalen**, separat från kulturella forskningsreferenser och 32 kreativa motivkoncept.

## Register
- [activities.csv](activities.csv): **faktiskt producerade eller pågående aktivitetsblad**. Ny rad först när produktion startar; en idé i `creative/motifs.json` är inte en aktivitet.
- [assets.csv](assets.csv): originalfil, facit, publiceringsrätt och teknisk granskning per digital tillgång.
- [RELEASE_GATE.md](RELEASE_GATE.md): villkor för att publicera en aktivitet.

## Koppling till resten
`referens → temakoppling → motivkoncept → originalillustration → aktivitet + facit → trycktest/rättighetsprövning → publicerad produkt`.

### Nuvarande tillstånd
Det finns **3 internt registrerade A4-prototyper och 6 programgenererade SVG-filer** (tre numrerade blad och tre facit). **0 är publicerade eller mänskligt granskade.** De 32 motiven är fortsatt koncept, utom de tre som har prototypanknytning. Se [prototyprevisionen](PROTOTYPE_REPORT.md).

### Ändring och validering
Ändra `prototype_specs.json` för teknisk SVG-konstruktion. Kör `python scripts/build_prototypes.py`, `python scripts/validate_svg_prototypes.py`, `python scripts/validate_production.py`, `python scripts/build_discovery.py` och `python scripts/doctor.py`. Alla rättighets-/tryck-/tillgänglighets-/human-review-fält står kvar i PENDING fram till faktiskt mänskligt godkännande. Allt går lokalt utan konton eller nätverk.
