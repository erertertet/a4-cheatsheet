# A4 Cheatsheet

A Codex skill for laying out illustrated Markdown notes in A4 HTML and exporting them to PDF with Chrome or Chromium.

## Requirements

- Codex and Git.
- A GitHub account with read access to this private repository.
- Python 3.10 or later and an installed Chrome or Chromium browser for PDF export.

## Install

Clone the repository into your personal Codex skills directory. [Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

### Windows (PowerShell)

```powershell
$skillDirectory = Join-Path $HOME '.agents/skills'
New-Item -ItemType Directory -Force -Path $skillDirectory | Out-Null
git clone https://github.com/erertertet/a4-cheatsheet.git (Join-Path $skillDirectory 'a4-cheatsheet')
```

### macOS and Linux

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/erertertet/a4-cheatsheet.git "$HOME/.agents/skills/a4-cheatsheet"
```

## Use the skill

Type `$a4-cheatsheet` in Codex and describe what you want. If the skill does not appear, restart Codex. [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use)

```text
$a4-cheatsheet Turn notes.md into a two-page A4 PDF with embedded figures beside the relevant text.
```

## Export an existing HTML file

From the cloned repository, pass the paths to your HTML and PDF files. Use `python3` if that is your Python command. The HTML controls paper size and pagination.

```bash
python scripts/html-to-pdf.py /path/to/notes.html /path/to/notes.pdf
```

Use `--chrome-path` if the exporter needs the location of your browser executable. See [SKILL.md](SKILL.md) for the layout and verification workflow.

## Update

```bash
git -C "$HOME/.agents/skills/a4-cheatsheet" pull --ff-only
```
