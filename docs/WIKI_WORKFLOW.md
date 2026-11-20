# Wiki-först – publiceringsflöde

GitHub Wiki är ett **separat Git-repository** (`Hybrismannen/Barnskoj.wiki.git`). All redaktionell Wiki-text har sin versionsstyrda källa i `wiki-src/`, och genererade bild-/rättighetsindex byggs från kanoniska register.

## Konfigurerad process
1. Redigera `wiki-src/*.md`, `images/*.csv`, `sourcing/*.csv` eller `rights/*.csv` efter respektive källa.
2. Kör `python scripts/build_rights.py` och `python scripts/build_wiki.py`, sedan `python scripts/doctor.py`.
3. En ändring i `wiki-src/` utlöser `.github/workflows/wiki-publish.yml`.
4. Workflödet klonar Wiki-Git, överför alla hanterade Markdown-filer, pushar och **jämför remote SHA med lokalt SHA**.
5. Först därefter kan driftansvarig attestera publiceringen i `devops/WIKI_PUBLICATION.json`; den kan inte förklaras slutförd av enbart grönt katalog-CI.

## Enda initialiseringssteget som kan kräva manuell användaråtgärd
Enligt [GitHubs dokumentation](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages) måste **den första Wiki-sidan skapas i Wiki-fliken innan Wiki Git kan klonas**. Om det saknas: gå till [Wiki-fliken](https://github.com/Hybrismannen/Barnskoj/wiki) och skapa en första sida `Home`.

Om automatisk token inte har behörighet att skriva Wiki: ange en repo-/Wiki-skrivbehörig token i repository secret **`BARNSKOJ_WIKI_TOKEN`**. Dela aldrig token i ett issue, chatmeddelande eller kodfil. GitHub Actions-loggen anger uttryckligen varför publicering misslyckas.

## Endast en publicerad Wiki, inga manuella dubbletter
- `wiki-src/` är versionerad källa, GitHub Wiki är publicerad läsvy.
- Maskingenererade index: `Bildindex*.md`, `Universumkallor.md`, `Rattighetsmatris.md`.
- Ändra inte de genererade Wiki-indexen för hand.
- Om Wiki-commit saknas är publikationsstatus **NOT_VERIFIED**, inte godkänd.

**Wiki och originalbilder är nu en separat förgrind till kommande WP, inte en retroaktiv ändring av historiska WP01–WP03.**
