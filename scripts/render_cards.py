#!/usr/bin/env python3
"""Render a post's "## Slides" section into 1080x1350 PNG carousel slides (headless Chromium, no installs).

  python3 scripts/render_cards.py content/posts/01-merged-this-month.md
Writes content/assets/<post-stem>/slide-1.png ... and prints the comma-separated paths.

Slide syntax inside "## Slides":
  ### KICKER | Title text
  Body paragraphs (blank-line separated). Lines starting with "- " become bullets.
  ```lang
  optional code block
  ```
"""
import html, os, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = next(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"), None)
NAME, TITLE = os.environ.get("CARD_NAME", "Your Name"), os.environ.get("CARD_TITLE", "Your Title")
HANDLE = os.environ.get("CARD_HANDLE", "github.com/you")

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{background:#0b1020;color:#e8ecf5;font-family:-apple-system,"SF Pro Display","Helvetica Neue",Arial,sans-serif;
 padding:96px 88px 0;position:relative;overflow:hidden}
body:before{content:"";position:absolute;inset:0;background:radial-gradient(900px 600px at 85% -10%,#2b3a8f55,transparent 60%),
 radial-gradient(700px 500px at -10% 110%,#0f766e44,transparent 60%)}
.wrap{position:relative;height:1120px;display:flex;flex-direction:column}
.wrap.first{justify-content:center;padding-bottom:80px}
.kicker{font:600 26px/1 "SF Mono",Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;color:#5eead4;margin-bottom:28px}
h1{font-size:68px;line-height:1.08;font-weight:800;letter-spacing:-.02em;margin-bottom:40px}
h1.big{font-size:84px}
p{font-size:36px;line-height:1.42;color:#c7cee0;margin-bottom:26px}
p strong,li strong{color:#fff}
ul{list-style:none;margin-bottom:26px}
li{font-size:34px;line-height:1.38;color:#c7cee0;padding-left:44px;position:relative;margin-bottom:20px}
li:before{content:"→";position:absolute;left:0;color:#5eead4;font-weight:700}
code{font-family:"SF Mono",Menlo,monospace;font-size:.88em;color:#fde68a}
pre{margin-bottom:30px;background:#060912;border:1px solid #26304d;border-radius:20px;padding:34px 36px;margin-top:8px;
 font:500 24px/1.5 "SF Mono",Menlo,monospace;color:#e2e8f0;white-space:pre-wrap}
pre .add{color:#86efac} pre .del{color:#fca5a5} pre .cm{color:#7c8db5}
.foot{position:absolute;left:88px;right:88px;bottom:64px;display:flex;justify-content:space-between;align-items:flex-end;
 border-top:1px solid #26304d;padding-top:28px}
.who b{display:block;font-size:30px;color:#fff} .who span{font-size:24px;color:#8b95b0}
.pg{font:600 24px "SF Mono",Menlo,monospace;color:#8b95b0;text-align:right}
.pg i{display:block;font-style:normal;color:#5eead4;margin-top:6px}
"""


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", s)


def code_html(code):
    out = []
    for line in code.splitlines():
        e = html.escape(line)
        cls = "add" if line.startswith("+") else "del" if line.startswith("-") else "cm" if line.lstrip().startswith(("//", "#")) else ""
        out.append(f'<span class="{cls}">{e}</span>' if cls else e)
    return "\n".join(out)


def slide_html(head, body, n, total):
    kicker, _, title = head.partition("|")
    if not title:
        kicker, title = "", kicker
    parts, blocks = [], re.split(r"(```.*?```)", body, flags=re.S)
    for b in blocks:
        if b.startswith("```"):
            code = re.sub(r"^```\w*\n?|```$", "", b).rstrip()
            parts.append(f"<pre>{code_html(code)}</pre>")
            continue
        for para in [x.strip() for x in b.split("\n\n") if x.strip()]:
            lines = para.splitlines()
            if all(l.startswith("- ") for l in lines):
                parts.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
            else:
                parts.append(f"<p>{inline(' '.join(lines))}</p>")
    cls = "big" if n == 1 else ""
    nxt = "swipe →" if n < total else HANDLE
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="wrap {"first" if n == 1 else ""}">{f'<div class="kicker">{inline(kicker.strip())}</div>' if kicker.strip() else ''}
<h1 class="{cls}">{inline(title.strip())}</h1>{''.join(parts)}</div>
<div class="foot"><div class="who"><b>{NAME}</b><span>{TITLE}</span></div><div class="pg">{n}/{total}<i>{nxt}</i></div></div>
</body></html>"""


def main():
    if not CHROME:
        sys.exit("headless chromium not found under ~/Library/Caches/ms-playwright")
    post = Path(sys.argv[1]).resolve()
    md = post.read_text()
    m = re.search(r"^## Slides\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    if not m:
        sys.exit("no '## Slides' section")
    slides = re.findall(r"^### (.+?)\n(.*?)(?=^### |\Z)", m.group(1), re.S | re.M)
    out = ROOT / "content/assets" / post.stem
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (head, body) in enumerate(slides, 1):
            f = Path(tmp) / f"s{i}.html"
            f.write_text(slide_html(head, body.strip(), i, len(slides)))
            png = out / f"slide-{i}.png"
            subprocess.run([str(CHROME), "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                            "--window-size=1080,1350", f"--screenshot={png}", f.as_uri()],
                           check=True, capture_output=True)
            paths.append(str(png.relative_to(ROOT)))
    print(",".join(paths))


if __name__ == "__main__":
    main()
