#!/usr/bin/env python3
"""Sincronitza el contingut del repositori GitBook (gitbook-sx) cap a `content/`.

Font de veritat:
  * `gitbook-docs.yaml`  -> ordre i títol dels espais (pestanyes de MkDocs).
  * `<espai>/SUMMARY.md` -> pàgines publicades i la seua jerarquia.

Ús habitual (amb el remot `upstream` apuntant a arturocandela/gitbook-sx):

    git fetch upstream
    python scripts/sync_gitbook.py --ref upstream/main
    mkdocs build --strict

També accepta un directori ja descarregat: `--src /ruta/a/gitbook-sx`.

Què fa:
  1. Esborra de `content/` els espais sincronitzats prèviament (els directoris
     marcats amb `.gitbook-space`) i els torna a crear.
  2. Copia només les pàgines referenciades a SUMMARY.md (GitBook deixa còpies
     òrfenes quan es mouen pàgines) i `.gitbook/assets/` -> `assets/`
     (MkDocs ignora els directoris que comencen per punt).
  3. Converteix la sintaxi pròpia de GitBook a Material for MkDocs:
     `{% hint %}` -> admonitions, `{% embed %}` -> enllaç, enllaços a
     directoris (`./`, `../`) -> `README.md`.
  4. Regenera el bloc `nav` de `mkdocs.yml` entre els marcadors
     `# BEGIN nav` / `# END nav`. Les pàgines amb `hidden: true` es publiquen
     però no apareixen al menú (igual que a GitBook).
"""
from __future__ import annotations

import argparse
import io
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"
MKDOCS_YML = REPO / "mkdocs.yml"
MARKER = ".gitbook-space"

HINT_STYLES = {"info": "info", "warning": "warning", "danger": "danger", "success": "success"}
HINT_TITLES = {"info": "Informació", "warning": "Atenció", "danger": "Perill", "success": "Correcte", "note": "Nota"}

# Els emojis dels títols de GitBook es substitueixen per icones de Material al menú.
EMOJI_ICONS = {
    "⚒": "material/hammer-wrench",
    "🛠": "material/hammer-wrench",
    "📎": "material/paperclip",
    "📝": "material/pencil-outline",
    "💡": "material/lightbulb-on-outline",
}
# Icona per defecte segons el grup del SUMMARY.md (si el títol no porta emoji).
GROUP_ICONS = {
    "fonaments": "material/book-open-variant",
    "qualificables": "material/clipboard-check-outline",
    "pràctiques": "material/paperclip",
}
GROUP_TITLES = {"pindoles formatives": "Píndoles formatives"}
LEADING_EMOJI = re.compile(r"^([^\w\s(\[\"'¿¡]+)\s*")


# ---------------------------------------------------------------- source ----
def extract_ref(ref: str, dest: Path) -> None:
    data = subprocess.run(["git", "archive", "--format=tar", ref], cwd=REPO,
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(dest, filter="data")


# --------------------------------------------------------------- summary ----
LINK_RE = re.compile(r"^(?P<indent>\s*)[*-] \[(?P<title>.+?)\]\((?P<path>[^)]+)\)")
HEADING_RE = re.compile(r"^##\s+(?P<title>.+)$")
TAG_RE = re.compile(r"<[^>]+>")


def clean_title(title: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub("", title)).strip()


def split_emoji(title: str) -> tuple[str, str | None]:
    """'⚒️ Títol' -> ('Títol', 'material/hammer-wrench')."""
    m = LEADING_EMOJI.match(title)
    if not m:
        return title, None
    emoji = m.group(1).replace("\ufe0f", "").strip()
    return title[m.end():].strip(), EMOJI_ICONS.get(emoji[:1])


def nice_group(title: str) -> str:
    title, _ = split_emoji(title)
    if title.isupper():
        title = title.capitalize()
    return GROUP_TITLES.get(title.lower(), title)


def parse_summary(text: str):
    """Torna una llista de grups [(títol|None, [node])]; node = {title, path, children}."""
    groups: list[tuple[str | None, list]] = [(None, [])]
    stack: list[tuple[int, list, str | None]] = []
    for line in text.splitlines():
        if m := HEADING_RE.match(line):
            groups.append((nice_group(clean_title(m["title"])), []))
            stack = []
            continue
        if m := LINK_RE.match(line):
            level = len(m["indent"].replace("\t", "  ")) // 2
            title, icon = split_emoji(clean_title(m["title"]))
            group = (groups[-1][0] or "").lower()
            if stack:  # fill: hereta la icona del pare si no en té
                icon = icon or stack[-1][2]
            icon = icon or GROUP_ICONS.get(group) or GROUP_ICONS.get(title.lower())
            node = {"title": title, "icon": icon, "path": m["path"].strip(), "children": []}
            while stack and stack[-1][0] >= level:
                stack.pop()
            (stack[-1][1] if stack else groups[-1][1]).append(node)
            stack.append((level, node["children"], icon))
    return [(t, items) for t, items in groups if items]


def iter_paths(nodes):
    for n in nodes:
        yield n["path"]
        yield from iter_paths(n["children"])


# ------------------------------------------------------------- transform ----
HINT_OPEN = re.compile(r'^(?P<indent>[ \t]*)\{%\s*hint(?:\s+style="(?P<style>\w+)")?\s*%\}\s*$')
HINT_CLOSE = re.compile(r"^[ \t]*\{%\s*endhint\s*%\}\s*$")
EMBED_RE = re.compile(r'\{%\s*embed\s+url="(?P<url>[^"]+)"\s*%\}')
MD_LINK_RE = re.compile(r"\]\((?P<target><[^>]+>|[^)\s]+)(?P<rest>[^)]*)\)")


def convert_hints(text: str) -> str:
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        m = HINT_OPEN.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent = m["indent"]
        kind = HINT_STYLES.get(m["style"] or "info", "note")
        body, i = [], i + 1
        while i < len(lines) and not HINT_CLOSE.match(lines[i]):
            body.append(lines[i]); i += 1
        i += 1  # endhint
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        out.append(f'{indent}!!! {kind} "{HINT_TITLES.get(kind, kind.capitalize())}"')
        out.append("")
        for b in body:
            b = b[len(indent):] if b.startswith(indent) else b.lstrip()
            out.append(f"{indent}    {b}" if b.strip() else "")
        out.append("")
    return "\n".join(out)


FENCE_RE = re.compile(r"^\s*(```|~~~)")


def convert_hard_breaks(text: str) -> str:
    """GitBook marca els salts de línia amb `\\` al final; Python-Markdown no.

    Es converteixen en dos espais finals, excepte dins de blocs de codi
    (on la barra és, per exemple, continuació de línia de Bash).
    """
    out, in_fence, in_pre = [], False, False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif "<pre" in line:
            in_pre = "</pre>" not in line
        elif "</pre>" in line:
            in_pre = False
        elif not in_fence and not in_pre and line.endswith("\\") and not line.endswith("\\\\"):
            line = line[:-1].rstrip() + "  "
        out.append(line)
    return "\n".join(out)


def fix_links(text: str, page: Path, space_root: Path) -> str:
    def repl(m: re.Match) -> str:
        target = m["target"]
        bare = target[1:-1] if target.startswith("<") else target
        if re.match(r"^[a-z]+:|^#|^/", bare):
            return m.group(0)
        path, _, frag = bare.partition("#")
        if path in ("", ".") and not frag:
            return m.group(0)
        if path == "" or path.endswith("/") or path in (".", ".."):
            candidate = posixpath.normpath(posixpath.join(path or ".", "README.md"))
            if (page.parent / candidate).resolve().is_file():
                new = candidate + (f"#{frag}" if frag else "")
                new = f"<{new}>" if " " in new else new
                return f"]({new}{m['rest']})"
        return m.group(0)
    return MD_LINK_RE.sub(repl, text)


def transform(text: str, page: Path, space_root: Path) -> str:
    text = text.replace(".gitbook/assets/", "assets/")
    text = convert_hard_breaks(text)
    text = convert_hints(text)
    text = EMBED_RE.sub(lambda m: f"[▶ {m['url']}]({m['url']})", text)
    text = fix_links(text, page, space_root)
    return text


def set_icon(text: str, icon: str | None) -> str:
    """Afig `icon:` al front matter (Material el mostra al menú)."""
    if not icon:
        return text
    if text.startswith("---\n"):
        end = text.find("\n---", 3)
        meta = text[4:end]
        if re.search(r"^icon:", meta, flags=re.M):
            return text
        return f"---\nicon: {icon}\n{meta}{text[end:]}"
    return f"---\nicon: {icon}\n---\n\n{text}"


def iter_nodes(nodes):
    for n in nodes:
        yield n
        yield from iter_nodes(n["children"])


def is_hidden(md: Path) -> bool:
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    try:
        meta = yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return False
    return bool(meta.get("hidden"))


# ------------------------------------------------------------------- nav ----
def q(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def nav_lines(nodes, base: str, depth: int, hidden: set[str]) -> list[str]:
    pad = "  " * depth
    lines = []
    for n in nodes:
        rel = posixpath.join(base, n["path"])
        if rel in hidden:
            continue
        if n["children"]:
            title = n["title"].capitalize() if n["title"].isupper() else n["title"]
            lines.append(f"{pad}- {q(title)}:")
            lines.append(f"{pad}    - Presentació: {q(rel)}")
            lines += nav_lines(n["children"], base, depth + 2, hidden)
        else:
            lines.append(f"{pad}- {q(n['title'])}: {q(rel)}")
    return lines


def write_nav(spaces, hidden: set[str]) -> None:
    lines = ["nav:", "  - Inici: README.md"]
    for title, path, groups in spaces:
        lines.append(f"  - {q(title.replace(' - ', ' · '))}:")
        for gtitle, items in groups:
            if gtitle:
                sub = nav_lines(items, path, 4, hidden)
                if sub:  # un grup amb totes les pàgines ocultes no es mostra
                    lines.append(f"      - {q(gtitle)}:")
                    lines += sub
            else:
                lines += nav_lines(items, path, 3, hidden)
    if hidden:
        lines += ["", "# Pàgines amb `hidden: true` a GitBook: es publiquen però no van al menú.",
                  "not_in_nav: |"] + [f"  /{h}" for h in sorted(hidden)]
    block = "# BEGIN nav (generat per scripts/sync_gitbook.py, no editar a mà)\n" \
            + "\n".join(lines) + "\n# END nav"
    yml = MKDOCS_YML.read_text(encoding="utf-8")
    new, n = re.subn(r"# BEGIN nav.*?# END nav", lambda _: block, yml, flags=re.S)
    if n != 1:
        sys.exit("No s'han trobat els marcadors '# BEGIN nav' / '# END nav' a mkdocs.yml")
    MKDOCS_YML.write_text(new, encoding="utf-8")


# ------------------------------------------------------------------ main ----
def sync(src: Path) -> None:
    cfg = yaml.safe_load((src / "gitbook-docs.yaml").read_text(encoding="utf-8"))
    # Ordre de les pestanyes: SA01…SA06 i després la resta (SAXX - AWS Academy).
    entries = sorted(cfg["site"]["structure"], key=lambda e: e["title"])

    for d in CONTENT.iterdir():
        if d.is_dir() and (d / MARKER).exists():
            shutil.rmtree(d)

    spaces, hidden = [], set()
    for e in entries:
        sdir = src / e["content"]["directory"]
        path = e["path"]
        dest = CONTENT / path
        groups = parse_summary((sdir / "SUMMARY.md").read_text(encoding="utf-8"))
        dest.mkdir(parents=True)
        (dest / MARKER).write_text(f"Sincronitzat des de GitBook: {e['title']}\n")
        if (sdir / ".gitbook" / "assets").is_dir():
            shutil.copytree(sdir / ".gitbook" / "assets", dest / "assets")
        for _, items in groups:
            for rel in iter_paths(items):
                srcf, dstf = sdir / rel, dest / rel
                if not srcf.is_file():
                    print(f"AVÍS: {path}/{rel} és a SUMMARY.md però no existeix", file=sys.stderr)
                    continue
                dstf.parent.mkdir(parents=True, exist_ok=True)
                dstf.write_text(srcf.read_text(encoding="utf-8"), encoding="utf-8")
                if is_hidden(srcf):
                    hidden.add(posixpath.join(path, rel))
        for _, items in groups:
            for n in iter_nodes(items):
                f = dest / n["path"]
                if f.is_file():
                    text = transform(f.read_text(encoding="utf-8"), f, dest)
                    f.write_text(set_icon(text, n["icon"]), encoding="utf-8")
        spaces.append((e["title"], path, groups))
        print(f"{e['title']}: {sum(1 for g in groups for _ in iter_paths(g[1]))} pàgines")

    write_nav(spaces, hidden)
    if hidden:
        print("Pàgines ocultes (fora del menú):", *sorted(hidden), sep="\n  ")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ref", help="referència git (p. ex. upstream/main)")
    g.add_argument("--src", type=Path, help="directori amb una còpia del repositori GitBook")
    args = ap.parse_args()
    if args.src:
        sync(args.src.resolve())
    else:
        with tempfile.TemporaryDirectory() as tmp:
            extract_ref(args.ref, Path(tmp))
            sync(Path(tmp))


if __name__ == "__main__":
    main()
