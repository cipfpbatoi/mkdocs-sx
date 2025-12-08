# Repository Guidelines

## Project Structure & Module Organization
- Core content lives in topic folders like `awsacademy/`, `dhcp/`, `dns/`, `ftp/`, `http/`, `interconexio-de-xarxes/`, and `ssh-vnc-rdp/`; each carries `README.md`, `SUMMARY.md`, and subfolders `pindoles-formatives/`, `practiques/`, plus `.gitbook/assets/` for images.
- MkDocs config in `mkdocs.yml` (Material theme, Catalan locale) builds from the configured `docs_dir` and writes static output to `docs/` for GitHub Pages. Keep `requirements.txt` aligned with that stack.

## Build, Test, and Development Commands
- `python -m pip install -r requirements.txt` — install MkDocs, Material theme, and plugins (page-to-pdf, print-site).
- `mkdocs serve --strict` — live preview at http://127.0.0.1:8000 with broken-link and heading checks.
- `mkdocs build --strict` — production build to `docs/`; CI workflow uses the same command before deploying to Pages.

## Coding Style & Naming Conventions
- Write Markdown in concise Catalan/Spanish; prefer active voice and short sections. Start pages with YAML front matter when a `description` is useful.
- Use kebab-case paths and keep existing numbering patterns (e.g., `ud04.01-...`) for new lessons; name entry files `README.md` to match current navigation.
- Place media under the nearest `.gitbook/assets/` and reference with relative links; avoid embedding binaries elsewhere.
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
- Large media should stay optimized; avoid adding heavy binaries outside `.gitbook/assets/`.
