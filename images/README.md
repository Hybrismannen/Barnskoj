# Barnskoj – bildproveniens, original och licens

**Omfattning:** 485 kulturreferensentiteter + 32 kreativa motiv + 9 staged kontinuitetsvarianter = **526 obligatoriska poster**, med stabilt ID och eget bildsourcingspår. Ett registerspår med status `MISSING` är **inte** en tillgänglig eller licensierad bild.

## Bildtyper
1. **Historisk originalbild:** fotografi, arkivobjekt, originalillustration eller dokumentation publicerad av rättighetsinnehavare, museum, arkiv eller upphovsperson. Exakt föremål, fotograf/illustratör, proveniens och återanvändningsvillkor krävs.
2. **Sourced referensbild:** bekräftad bild som används för *research*, men inte för kommersiell reproduktion. En museumsbild kan fortfarande vara skyddad.
3. **Barnskoj-original:** en självständigt skapad egen illustration, med dokumenterat upphov, källinspiration, originalfil och rättighetsbedömning. Även en ny avritning av en skyddad figur kan kräva tillstånd.

## Workflow
`MISSING → DISCOVERED_CANDIDATE / SOURCE_CANDIDATE → SOURCE_CONFIRMED → RIGHTS_REVIEWED → APPROVED_FOR_DESIGN`.

- **SOURCE_CANDIDATE:** faktisk objekts- eller bildsida identifierad, utan garanti att rätt bild/skapare/licens har verifierats.
- **SOURCE_CONFIRMED:** rätt person/figur, ursprungligt verk, upphovsman/fotograf och exakt källa fastställd.
- **RIGHTS_REVIEWED:** licens och restriktioner dokumenterade – ej automatiskt kommersiellt godkännande.
- **APPROVED_FOR_DESIGN:** produktspecifikt beslut och bildrättighet dokumenterad.

## Wikimedia Commons
För en faktisk fil måste filens Commons-sida kopplas till `imageinfo`-metadata: `Artist`, `Credit`, `LicenseShortName`, `LicenseUrl`, `AttributionRequired`, `Restrictions` och originalfilens URL. Sökresultat eller Commons-filens existens ger inte tillräcklig rättighetskontroll. Kändisporträtt och karaktärer kan ha separata rättigheter.

Originalbilder kopieras **inte** från tredje part till detta repo före behörig granskning. En extern källa ska länkas, inte hotlinkas som om vi ägde den.

## Innehållsgrad och kvalitet
- Ett [bildkravsregister](requirements.csv) täcker samtliga 517 kanoniska ID:n och 9 staged-ID:n.
- [Källsökningsskript](../scripts/discover_image_candidates.py) ger endast **obekräftade träffar**, aldrig automatisk bildauktorisering.
- [Kvalitetsgrind](../scripts/validate_images.py) avvisar saknade IDs och förhindrar att fält för upphov/rättigheter hoppats över.
- Både forskningsnivå Q3 och separat bildrättsgranskning kan krävas för utgåvor med historiska faktarutor eller identifierbara figurer.

**Ingen av de 526 posterna ska deklareras käll- och rättighetsklarerad förrän faktiska originalbilder och villkor har verifierats.**

## WP05 – revisionsbar proveniensgranskning
Kör `python scripts/audit_image_provenance.py --summary` för summerad read-only status, eller `python scripts/audit_image_provenance.py` för enskilda brister. `--require-complete` avslutar med kod 2 så länge minst en källprovenienspost saknas. Skriptet hämtar inte bilder, skriver inga licenser och höjer aldrig bildens status automatiskt. Prioritera `SOURCE_CANDIDATE` som manuella granskningsköer; dessa är inte `SOURCE_CONFIRMED`. En komplett provenienspost är fortfarande **inte** kommersiell publiceringsrätt.
