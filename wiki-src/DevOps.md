# DevOps – Wiki och originalbilder före WP-godkännande

## Nuvarande historik
De tidigare tre arbetspaketen **WP01 data**, **WP02 DevOps-kvalitet** och **WP03 prototyper** har redan genomförts tekniskt och finns versionshistoriskt dokumenterade. Den historiken skrivs **inte om**.

## Bindande nya förkrav
Innan en ny iteration av WP01–WP03 deklareras genomförd ska följande vara uppfyllt:

- **Wiki-gate:** De här sidorna har publicerats och kontrollerats i GitHubs **separata** Wiki-repository.
- **Bild-gate:** Samtliga 485 entiteter och 32 motiv har en faktisk originalbilds-/referenssida och verifierad proveniens. Ett tomt fält eller sökträff duger inte.
- **Rights-gate:** För publiceringsarbete krävs separat licens- och bildrättsbeslut. Källverifierad research är inte tillräcklig.
- **CI-gate:** Kanoniska källor och genererade vyer är synkade och projektets kvalitetskontroller passerar.

Dessa förkrav kontrolleras med [prerequisite-gaten](https://github.com/Hybrismannen/Barnskoj/blob/main/scripts/check_wp_prerequisites.py), som ska blockera i stället för att ge falskt godkännande.

## Process
`Wiki-innehåll → publicera/synkronisera och verifiera Wiki → källsourca originalbilder → granska licenser → WP01 → WP02 → WP03 → acceptans`.

[WP-protokoll](https://github.com/Hybrismannen/Barnskoj/blob/main/devops/WORKPACKAGES.md) · [Runbook](https://github.com/Hybrismannen/Barnskoj/blob/main/devops/RUNBOOK.md)
