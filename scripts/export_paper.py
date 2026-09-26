#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAPER_FINAL_EXPORT — Markdown -> self-contained HTML (inline SVG + academic CSS).
Only transforms layout; does NOT alter any number, claim, formula, or model content.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "paper" / "paper_v2_submission_candidate.md"
FIG_DIR = ROOT / "reports" / "visual_evidence" / "final"


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_code_repl(m):
    return "<code>" + escape(m.group(1)) + "</code>"


def apply_inline(s: str) -> str:
    # inline code first (protect backticks)
    s = re.sub(r"`([^`]+)`", inline_code_repl, s)
    # bold
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # italic (single *)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def svg_inline(path: str) -> str:
    p = Path(path)
    # path relative to paper/ -> resolve against ROOT/paper
    base = ROOT / "paper"
    fp = (base / p).resolve()
    if not fp.exists():
        return f'<p class="figure-missing">[FIGURE MISSING: {p}]</p>'
    raw = fp.read_text(encoding="utf-8")
    # keep the raw <svg> element only
    m = re.search(r"<svg[\s\S]*?</svg>", raw)
    return m.group(0) if m else f'<p class="figure-missing">[SVG PARSE FAIL: {p}]</p>'


def md_to_html(md: str) -> str:
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    in_para = []

    def flush_para():
        if in_para:
            text = " ".join(in_para).strip()
            if text:
                out.append(f"<p>{apply_inline(text)}</p>")
            in_para.clear()

    while i < n:
        line = lines[i]

        # fenced code block
        if line.strip().startswith("```"):
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code = "\n".join(buf).strip("\n")
            out.append(f'<pre class="codeblock"><code>{escape(code)}</code></pre>')
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para()
            lvl = len(m.group(1))
            text = apply_inline(m.group(2).strip())
            out.append(f"<h{lvl}>{text}</h{lvl}>")
            i += 1
            continue

        # image
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line)
        if m:
            flush_para()
            alt = escape(m.group(1))
            src = m.group(2)
            if src.endswith(".svg"):
                out.append(f'<figure class="figure">{svg_inline(src)}</figure>')
            else:
                out.append(f'<p class="figure-missing">[UNSUPPORTED IMAGE: {src}]</p>')
            i += 1
            continue

        # table row
        if line.strip().startswith("|"):
            flush_para()
            table_rows = []
            while i < n and lines[i].strip().startswith("|"):
                table_rows.append(lines[i].strip())
                i += 1
            # drop separator row (|---|)
            body = [r for r in table_rows if not re.match(r"^\|[\s:\-|]+\|$", r)]
            if body:
                out.append('<table class="paper-table">')
                for ridx, r in enumerate(body):
                    cells = [c.strip() for c in r.strip("|").split("|")]
                    tag = "th" if ridx == 0 else "td"
                    out.append("<tr>" + "".join(
                        f"<{tag}>{apply_inline(c)}</{tag}>" for c in cells) + "</tr>")
                out.append("</table>")
            continue

        # blockquote
        if line.strip().startswith(">"):
            flush_para()
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "<br/>".join(apply_inline(b) for b in buf) + "</blockquote>")
            continue

        # horizontal rule
        if line.strip() == "---":
            flush_para()
            out.append("<hr/>")
            i += 1
            continue

        # list item
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            flush_para()
            ordered = bool(re.match(r"\d+\.", m.group(2)))
            tag = "ol" if ordered else "ul"
            items = []
            while i < n:
                m2 = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if not m2:
                    break
                items.append(apply_inline(m2.group(3).strip()))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{it}</li>" for it in items) + f"</{tag}>")
            continue

        # blank line
        if line.strip() == "":
            flush_para()
            i += 1
            continue

        # normal text -> accumulate paragraph
        in_para.append(line.strip())
        i += 1

    flush_para()
    return "\n".join(out)


CSS = """
:root { --ink:#1a1a1a; --muted:#555; --rule:#c9c9c9; }
* { box-sizing: border-box; }
@page { size: A4; margin: 22mm 20mm 20mm 20mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Noto Serif CJK SC","Source Han Serif SC","SimSun","宋体","Times New Roman",serif;
  color: var(--ink); font-size: 10.5pt; line-height: 1.65;
  max-width: 100%; margin: 0; text-align: justify;
}
h1 {
  font-family:"Noto Sans CJK SC","Source Han Sans SC","Microsoft YaHei","微软雅黑","SimHei",sans-serif;
  font-size: 17pt; font-weight: 700; line-height: 1.4; text-align: center;
  margin: 0 0 6pt 0;
}
h2 {
  font-family:"Noto Sans CJK SC","Microsoft YaHei","微软雅黑","SimHei",sans-serif;
  font-size: 13.5pt; font-weight: 700; margin: 18pt 0 7pt 0;
  border-bottom: 1.5px solid #333; padding-bottom: 3pt;
  page-break-after: avoid;
}
h3 {
  font-family:"Noto Sans CJK SC","Microsoft YaHei","微软雅黑","SimHei",sans-serif;
  font-size: 11.5pt; font-weight: 700; margin: 13pt 0 5pt 0;
  page-break-after: avoid;
}
h4,h5,h6 {
  font-family:"Noto Sans CJK SC","Microsoft YaHei","微软雅黑","SimHei",sans-serif;
  font-size: 10.5pt; font-weight: 700; margin: 10pt 0 4pt 0; page-break-after: avoid;
}
p { margin: 5pt 0; }
strong { font-weight: 700; }
em { font-style: italic; }
code {
  font-family:"Consolas","Courier New",monospace; font-size: 9pt;
  background:#f3f3f3; padding: 0 2pt; border-radius: 2pt;
}
pre.codeblock {
  font-family:"Consolas","Courier New",monospace; font-size: 9.2pt;
  background:#f7f7f7; border:1px solid #e2e2e2; border-radius:3pt;
  padding:7pt 9pt; white-space: pre-wrap; word-wrap: break-word;
  margin: 7pt 0; line-height:1.5; page-break-inside: avoid;
}
blockquote {
  margin: 8pt 0; padding: 6pt 12pt; border-left: 3px solid #888;
  background:#fafafa; color:#333; page-break-inside: avoid;
}
blockquote br + br { display: none; }
table.paper-table {
  border-collapse: collapse; width: 100%; margin: 7pt 0;
  font-size: 9pt; page-break-inside: avoid;
}
table.paper-table th, table.paper-table td {
  border: 0.6pt solid #999; padding: 3.5pt 5pt; text-align: left;
  vertical-align: top; word-break: break-word;
}
table.paper-table th { background:#efefef; font-weight:700; }
figure.figure { margin: 8pt 0; text-align: center; page-break-inside: avoid; }
figure.figure svg { width: 100%; height: auto; display: block; }
p.figure-missing { color:#c00; font-weight:700; }
hr { border:none; border-top:1px solid #ccc; margin: 12pt 0; }
ul, ol { margin: 5pt 0 5pt 1.2em; padding: 0; }
li { margin: 2.5pt 0; }
/* figure caption: the paragraph right after a figure is treated as caption in source */
/* keep urls wrapping */
a { word-break: break-all; }
"""


def main():
    md = SRC.read_text(encoding="utf-8")
    body = md_to_html(md)
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>数学建模论文 - 最终排版版</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
    out = ROOT / "build" / "paper_final.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"HTML written: {out} ({len(html)} chars)")


if __name__ == "__main__":
    main()
