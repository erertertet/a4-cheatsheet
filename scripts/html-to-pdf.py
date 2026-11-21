#!/usr/bin/env python3
"""Print a local HTML document to PDF with Chrome or Chromium."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


def find_browser(override):
    if override:
        path = Path(override).expanduser()
        if path.is_file():
            return path.resolve()
        executable = shutil.which(override)
        if executable:
            return Path(executable).resolve()
        raise ValueError(f"Chrome executable not found: {override}")

    candidates = []
    if sys.platform == "win32":
        for variable in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            if root := os.environ.get(variable):
                candidates.extend((
                    Path(root) / "Google" / "Chrome" / "Application" / "chrome.exe",
                    Path(root) / "Chromium" / "Application" / "chrome.exe",
                ))
        names = ("chrome.exe", "chromium.exe", "chrome-headless-shell.exe")
    elif sys.platform == "darwin":
        for applications in (Path("/Applications"), Path.home() / "Applications"):
            candidates.extend((
                applications / "Google Chrome.app" / "Contents" / "MacOS" / "Google Chrome",
                applications / "Chromium.app" / "Contents" / "MacOS" / "Chromium",
            ))
        names = ("google-chrome", "chromium", "chrome", "chrome-headless-shell")
    else:
        names = ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser", "chrome", "chrome-headless-shell")

    for candidate in candidates:
        if candidate.is_file():
            return candidate
    for name in names:
        if executable := shutil.which(name):
            return Path(executable).absolute()
    raise ValueError("Chrome or Chromium was not found. Pass its executable with --chrome-path.")


def print_pdf(source, destination, browser):
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Stage on the same filesystem so a failed print leaves an existing PDF intact.
    with TemporaryDirectory(prefix=".a4-cheatsheet-", dir=destination.parent, ignore_cleanup_errors=True) as temporary:
        work = Path(temporary)
        staged = work / "output.pdf"
        result = subprocess.run(
            [
                str(browser),
                "--headless",
                "--no-pdf-header-footer",
                f"--user-data-dir={work / 'profile'}",
                f"--print-to-pdf={staged}",
                source.as_uri(),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            check=False,
        )
        if result.returncode or not staged.is_file() or not staged.stat().st_size:
            log = "\n".join(result.stdout.splitlines()[-8:])
            message = f"Chrome did not produce a PDF (exit code {result.returncode})."
            raise RuntimeError(f"{message}\n{log}" if log else message)
        os.replace(staged, destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Local HTML file")
    parser.add_argument("output", type=Path, nargs="?", help="Output PDF (default: next to the HTML)")
    parser.add_argument("--chrome-path", help="Chrome or Chromium executable or command name")
    args = parser.parse_args()

    try:
        source = args.input.expanduser().resolve()
        if not source.is_file():
            raise ValueError(f"Local HTML file not found: {args.input}")
        destination = args.output.expanduser().resolve() if args.output else source.with_suffix(".pdf")
        if destination.suffix.lower() != ".pdf":
            raise ValueError(f"The output path must end in .pdf: {destination}")
        if destination == source:
            raise ValueError("The input and output paths must be different.")
        print_pdf(source, destination, find_browser(args.chrome_path))
    except subprocess.TimeoutExpired:
        parser.exit(1, "Error: Chrome printing timed out after 120 seconds.\n")
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    print(destination)


if __name__ == "__main__":
    main()
