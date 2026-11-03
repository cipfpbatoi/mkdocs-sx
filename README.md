# Serveis en Xarxa (MkDocs)

Web: <https://cipfpbatoi.github.io/mkdocs-sx/>

Els materials s'editen a GitBook, que els sincronitza amb el repositori
[`arturocandela/gitbook-sx`](https://github.com/arturocandela/gitbook-sx).
Aquest repositori els converteix a MkDocs (Material) i els publica a GitHub Pages.

## Incorporar els últims canvis de GitBook

```bash
git remote add upstream git@github.com:arturocandela/gitbook-sx.git  # només la primera vegada
git fetch upstream
python scripts/sync_gitbook.py --ref upstream/main
mkdocs build --strict
git add -A && git commit -m "Sincronitza amb GitBook (upstream/main@$(git rev-parse --short upstream/main))"
```

El script regenera els directoris de cada espai dins de `content/` i el bloc
`nav` de `mkdocs.yml`. **No edites a mà** aquests directoris ni el `nav`: es
sobreescriuen a cada sincronització. Els canvis de contingut es fan a GitBook.

## Previsualització local

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```
