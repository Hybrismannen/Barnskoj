# Kontrollregler – Barnskoj

Det maskinella testet i [scripts/validate_catalog.py](../scripts/validate_catalog.py) granskar enhets-ID, käll-ID, profil- och källdossierlänkar, universumsrelationer, alias, taggreferenser, evidenslänkar och QA-grader.

**Hårda fel = testet avbryter med FAIL**: saknat dokument, trasig CSV-rubrik, dubbelt ID, saknat source-ID, inkonsekventa taggar, fel kanonisk identitet, saknat källställe eller ej synkat QA-register.

**Varningar = forskningsskuld, men inte tekniskt fel**: oidentifierad källa för researchpost, oprecist historiskt årtionde, saknad rättighetsprövning, kvarstående redaktionella aliasfrågor.

## Forsknings- och produktionsgrind
1. Q0–Q1 = researchkandidater.
2. Q2 = ett eller flera kontrollerade specifika påståenden; inga ogrundade påståenden får smygas in.
3. Q3 = fullständig redaktionell djupverifiering med rätt datum, sammanhang, motstridiga uppgifter och flera källor.
4. Legal gate = separat från kvalitetsgrad och måste göras för det konkreta bildmaterialet.
5. Testad aktivitets-/tryckkvalitet = ytterligare separat release gate.

Testscriptet använder Python-standardbiblioteket och inga privata data, API-nycklar eller uppkoppling vid körning. GitHub Actions är konfigurerat på push/PR samt manuell start; att filen är uppladdad är inte i sig bevis för ett grönt CI-resultat.
