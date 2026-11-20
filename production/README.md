# Barnskoj – skapande och publicering

Denna mapp är **den verkliga leveransjournalen**, separat från kulturella forskningsreferenser och 32 kreativa motivkoncept.

## Register
- [activities.csv](activities.csv): **faktiskt producerade eller pågående aktivitetsblad**. Ny rad först när produktion startar; en idé i `creative/motifs.json` är inte en aktivitet.
- [assets.csv](assets.csv): originalfil, facit, publiceringsrätt och teknisk granskning per digital tillgång.
- [RELEASE_GATE.md](RELEASE_GATE.md): villkor för att publicera en aktivitet.

## Koppling till resten
`referens → temakoppling → motivkoncept → originalillustration → aktivitet + facit → trycktest/rättighetsprövning → publicerad produkt`.

### Nuvarande tillstånd
Det finns **0 registrerade aktiviteter och 0 producerade assets**. Detta är ett ärligt läge, inte ett fel. De 32 motiven är koncept och får inte räknas som färdiga böcker.

### Ändring och validering
Efter ändring i dessa register: kör `python scripts/validate_production.py`, `python scripts/build_discovery.py` och samtliga CI-test. Allt går lokalt utan konton eller nätverk.
