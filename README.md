# Serveis en Xarxa (MkDocs)

Web: <https://cipfpbatoi.github.io/mkdocs-sx/>

Aquest repositori és la font de veritat dels materials i publica el lloc a
GitHub Pages. Edita el contingut directament en `content/` i mantín la
navegació de `mkdocs.yml` actualitzada.

El repositori [`arturocandela/gitbook-sx`](https://github.com/arturocandela/gitbook-sx)
és una còpia de seguretat transitòria, prevista per a eliminar-se. Els seus
canvis es publiquen a GitBook; GitBook ja no és la font dels continguts d'aquest
projecte. Mantín els canvis compatibles amb aquella còpia mentre siga necessària.

## Importació antiga de GitBook

`scripts/sync_gitbook.py` es conserva només per a importacions puntuals: esborra
i regenera els espais marcats amb `.gitbook-space` i la navegació, de manera que
pot destruir canvis fets ací. No l'executes com a sincronització habitual; si
cal una importació, revisa abans l'origen i els canvis locals. L'script exigeix
`--overwrite-local-content` per a confirmar aquesta operació.

## Previsualització local

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```
