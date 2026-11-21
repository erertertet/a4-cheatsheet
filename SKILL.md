---
name: a4-cheatsheet
description: Create or revise illustrated Markdown study notes, manually lay them out in self-contained A4 HTML, and print or verify a page-limited PDF with local Chrome. Use for cheatsheets with embedded figures or for the HTML-to-A4-PDF step of that workflow.
---

# A4 Cheatsheet

For an existing HTML file with print styling in place, start at Export and verify.

1. Establish the output language, source scope, page target, and whether titles, section headings, or hyperlinks belong in the handout. Preserve those choices in revisions. If the user wants to review the Markdown first, deliver the Markdown and its figures at that checkpoint.
2. Keep the Markdown as the editable source. Use relative image references with descriptive alt text. Put each figure beside the concept it explains. Use labelled schematics or small plots for structure, relationships, and worked examples.
3. Compose the HTML by hand. Place the content and figures deliberately in page and column blocks. Embed image bytes in data URLs and keep print CSS inline so the HTML opens offline. For formulas, use static MathML or another fully rendered offline representation. When the user wants the full note in the PDF, carry across every paragraph, formula, and figure.
4. Print with the bundled [Chrome exporter](scripts/html-to-pdf.py). Inspect the resulting PDF and revise the HTML to meet the page target.

## Fit the page

Set the paper size and margins in CSS. For a tightly packed two-page portrait sheet, start with two columns per page, 8–10 mm margins, and body type around 9–10 pt. Adjust for the content and print legibility. Explicit page breaks make the page assignment predictable.

```css
@page { size: A4 portrait; margin: 8mm 9mm; }
@media print {
  :root { print-color-adjust: exact; }
  .sheet + .sheet { break-before: page; }
}
```

Use larger figures for dense plots and compact insets for simple explanatory diagrams. Balance the columns by moving whole topic blocks or worked examples. If there is overflow, reclaim gaps and rebalance content before reducing type. Keep labels legible at actual print size. If the full content and page target conflict with readability after reflow, state the trade-off and ask which constraint to relax.

## Export and verify

Use Python 3.10 or later and an installed Chrome or Chromium browser on Windows, macOS, or Linux. Resolve the exporter path relative to this skill.

```bash
python "<skill-folder>/scripts/html-to-pdf.py" "./notes.html" "./output/pdf/notes.pdf"
```

Use `python3` if that is the Python command on your system. The output path is optional and defaults to a sibling PDF. Pass `--chrome-path` to select a browser executable. The script uses the Python standard library, launches the browser in headless mode with an isolated temporary profile, and checks that printing produced a file. Pagination stays in the HTML.

Font availability can change pagination across operating systems. Check the actual PDF page count and paper size with `pdfinfo` or a PDF reader. Render and inspect every page at readable size with `pdftoppm` or an equivalent renderer. Check image placement, figure labels, equations, and clipping. Verify that all requested content made it into the export and that removed elements, such as links or headings, are absent. Repeat after changing the layout. Deliver the PDF and the editable source files requested by the user.

The original neuroscience handout fit 1,581 words, 64 formulas, and 16 figures on two portrait A4 pages using a two-column layout with smaller diagrams beside their explanatory text.
