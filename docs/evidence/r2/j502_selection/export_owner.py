#!/usr/bin/env python3
"""Export the report's owner briefing to one A4 page; requires PyMuPDF."""
import html
from pathlib import Path
import re

import pymupdf


def inline(text):
    text = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def main():
    directory = Path(__file__).resolve().parent
    source = (directory.parent / "J502_SELECTION.md").read_text()
    briefing = source.split("## OWNER EXPLANATION — one-page briefing\n", 1)[1]
    briefing = briefing.split("\n---\n", 1)[0].strip()
    blocks = ["<h1>J502 / Pi harness: owner explanation</h1>",
              "<p class='status'>2026-09-30 · NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED</p>"]
    for block in briefing.split("\n\n"):
        if block.startswith("|"):
            rows = block.splitlines()
            table = ["<table>"]
            for index, row in enumerate(rows):
                if index == 1:  # Markdown alignment row
                    continue
                tag = "th" if index == 0 else "td"
                cells = row.strip("|").split("|")
                table.append("<tr>" + "".join(f"<{tag}>{inline(c.strip())}</{tag}>" for c in cells) + "</tr>")
            blocks.append("".join(table) + "</table>")
        else:
            blocks.append("<p>" + inline(" ".join(block.splitlines())) + "</p>")
    blocks.append("<p class='footer'>Detailed sources, calculations and owner decisions: docs/evidence/r2/J502_SELECTION.md</p>")
    css = """
    body { font-family: sans-serif; font-size: 10pt; line-height: 1.18; color: #17202a; }
    h1 { font-size: 17pt; margin: 0 0 9pt; }
    p { margin: 8pt 0; }
    .status { font-size: 9pt; font-weight: bold; color: #8c241c; }
    table { border-collapse: collapse; width: 100%; font-size: 9pt; }
    td, th { border: 0.5pt solid #9ba6b0; padding: 5pt; text-align: left; }
    th { background-color: #e9eef2; }
    .footer { font-size: 8pt; color: #53616c; margin-top: 12pt; }
    """
    story = pymupdf.Story(html="".join(blocks), user_css=css)
    output = directory / "OWNER_EXPLANATION.pdf"
    paper = pymupdf.paper_rect("a4")
    writer = pymupdf.DocumentWriter(str(output))
    device = writer.begin_page(paper)
    more, _ = story.place(paper + (38, 34, -38, -34))
    story.draw(device)
    writer.end_page()
    writer.close()
    if more:
        raise RuntimeError("Owner explanation exceeds one page; revise content or formatting")
    with pymupdf.open(output) as document:
        assert len(document) == 1
        text = document[0].get_text()
        for token in ("4.785", "4.776", "4.747", "4.738", "NOT FOR FABRICATION", "No Pi was powered"):
            assert token in text, token
        document[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save("/private/tmp/j502-owner-review.png")
    print("PASS: one-page owner PDF; key voltages and engineering warning present")


if __name__ == "__main__":
    main()
