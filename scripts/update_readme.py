#!/usr/bin/env python3
"""Regenerate the "Open source" section of github.com/<you>/<you> from CONTRIBUTIONS.md.

Usage: python3 scripts/update_readme.py [--dry-run]
The section lives between <!-- OSS:START --> and <!-- OSS:END -->; on first run it is inserted
before the "### Stack" heading. Uses the gh CLI (contents API), no clone needed.
"""
import base64, json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = os.environ["PROFILE_REPO"]  # e.g. octocat/octocat
START, END = "<!-- OSS:START -->", "<!-- OSS:END -->"


def gh(*args, input=None):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True, input=input).stdout


def table_rows(md, heading):
    """Rows of the first markdown table after `heading` (or the first table if heading is None)."""
    if heading:
        md = md.split(heading, 1)[1]
    rows, started = [], False
    for line in md.splitlines():
        if line.startswith("|"):
            started = True
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not set("".join(cells)) <= set("-: "):
                rows.append(cells)
        elif started:
            break
    return rows[1:]  # drop header


def in_review(md):
    m = re.search(r"## In review.*?\n(.+?)\n", md, re.S)
    return m.group(1).strip() if m else ""


def build_section(md):
    merged = table_rows(md, None)
    lines = [START, "### Open source", "",
             "I contribute fixes, features, docs and reviews to open-source projects. My workflow is AI-augmented and built by me: "
             "every fix starts from a failing test, stays minimal, and follows each project's contribution and AI policies.", "",
             "**Merged**", "", "| Project | Contribution |", "|---|---|"]
    for date, repo, pr, what, kind in (r[:5] for r in merged):
        project = re.sub(r"\s*\(([\d.]+k)\)", r" ⭐ \1", repo)
        lines.append(f"| {project} | {pr} {what.split('. ')[0].rstrip('.')}. |")
    review = in_review(md)
    if review:
        prs = [p.strip() for p in review.split("·")]
        lines += ["", "**In review:** " + " · ".join(prs)]
    lines += ["", "<sub>Updated automatically from my contribution log.</sub>", END]
    return "\n".join(lines)


def main():
    md = (ROOT / "CONTRIBUTIONS.md").read_text()
    section = build_section(md)
    meta = json.loads(gh("api", f"repos/{REPO}/contents/README.md"))
    readme = base64.b64decode(meta["content"]).decode()
    if START in readme:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: section, readme, flags=re.S)
    elif "### Stack" in readme:
        new = readme.replace("### Stack", section + "\n\n---\n\n### Stack", 1)
    else:
        new = readme.rstrip() + "\n\n---\n\n" + section + "\n"
    if new == readme:
        print("README already up to date")
        return
    if "--dry-run" in sys.argv:
        print(section)
        return
    body = {"message": "Update open-source contributions", "content": base64.b64encode(new.encode()).decode(), "sha": meta["sha"]}
    gh("api", "-X", "PUT", f"repos/{REPO}/contents/README.md", "--input", "-", input=json.dumps(body))
    print("README updated")


if __name__ == "__main__":
    main()
