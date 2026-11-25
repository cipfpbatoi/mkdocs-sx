# Repository Guidelines

## Project Structure & Module Organization
- This repository is the source of truth. Edit content in `content/` and maintain the navigation in `mkdocs.yml` directly.
- `arturocandela/gitbook-sx` (remote `upstream`) is a temporary backup intended for eventual removal; its changes publish to GitBook. Keep changes compatible with that repository while it remains in use.
- `scripts/sync_gitbook.py` is a legacy import tool, not a routine synchronization step. It overwrites marked spaces and navigation; use it only for a deliberate import after reviewing local changes.
- Hand-maintained files include `content/`, `mkdocs.yml`, `scripts/`, and `.github/`.
- Nav icons come from `icon:` front matter injected by the sync script (GitBook title emojis are mapped in `EMOJI_ICONS`/`GROUP_ICONS`).
- Images live in each space's `assets/` (renamed from `.gitbook/assets/`, which MkDocs ignores). Pages reference them with raw HTML `<img>`, so `use_directory_urls: false` must stay.
- MkDocs config in `mkdocs.yml` (Material theme, Catalan locale) builds from `content/` and writes static output to `docs/` (gitignored) for GitHub Pages. Keep `requirements.txt` aligned with that stack.

## Build, Test, and Development Commands
- `python -m pip install -r requirements.txt` — install MkDocs, Material theme, and plugins (page-to-pdf, print-site).
- `mkdocs serve --strict` — live preview at http://127.0.0.1:8000 with broken-link and heading checks.
- `mkdocs build --strict` — production build to `docs/`; CI workflow uses the same command before deploying to Pages.

## Coding Style & Naming Conventions
- Write Markdown in concise Catalan/Spanish; prefer active voice and short sections. Start pages with YAML front matter when a `description` is useful.
- Use kebab-case paths and keep existing numbering patterns (e.g., `ud04.01-...`) for new lessons; name entry files `README.md` to match current navigation.
- Leverage mkdocs-material features already enabled: admonitions (`!!! note`), `pymdown` superfences for code/mermaid, tables, and tab sets.

## Testing Guidelines
- Always run `mkdocs build --strict` before pushing to catch missing assets, bad anchors, or nav errors.
- If you touch navigation, confirm ordering in `mkdocs.yml` and validate that search/tabbed navigation still renders via `mkdocs serve`.
- For diagrams, preview mermaid blocks locally to ensure syntax renders in Material.

## Commit & Pull Request Guidelines
- Follow the repo’s history: short imperative messages, optionally prefixed with the tracking key used here (`GITBOOK-##`) or a brief Spanish summary.
- PRs should outline scope (topics touched), note new media locations, and list manual checks (`mkdocs build --strict`, `mkdocs serve` preview). Include screenshots/PDF snippets when layout or assets change.
- Link related issues and keep commits focused; prefer multiple small commits over a single catch-all.

## Security & Configuration Tips
- Never commit secrets, API keys, or unredacted hostnames/IPs; use placeholders in examples.
- Keep `site_url`, contact data, and external script URLs in `mkdocs.yml` accurate when modifying configuration.
- Large media should stay optimized; avoid adding heavy binaries outside each space's `assets/`.
