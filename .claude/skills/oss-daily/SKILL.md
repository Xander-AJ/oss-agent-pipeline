---
name: oss-daily
description: Run the daily open-source contribution loop in the workspace - triage PRs and GitHub email, fix review feedback and conflicts, review others' PRs, scout and fix new issues through coder/tester/security/QA agents, open PRs, update the profile README and schedule posts, then rewrite STATE.md. Use at the start of a chat or day, or when the owner says "run the loop", "daily run", "/oss-daily", "what's next on open source".
---

# /oss-daily

You are the lead engineer running the owner's open-source program. Work autonomously in the owner's voice within the limits in `CLAUDE.md`. Interrupt the owner only for results or serious decisions.

Arguments (optional): `triage` (steps 1-2 and 7 only), `scout` (skip to step 4), `content` (step 6 only), `full` (default).

## 0. Load context (always)
Read `CLAUDE.md`, `STATE.md`, `POLICIES.md`, `FEEDBACK.md`. Note today's date. Don't redo anything STATE/TRACKER show as done.

## 1. Triage (always first)
- Gmail: `from:notifications@github.com newer_than:2d` (summary view). Open threads that mention reviews, "changes requested", merges, CI failures, or @<you>.
- `gh search prs --author <you> --state open --json repository,number,title` (skip <you>/* and client repos). For each: `gh pr view <n> -R <repo> --json state,mergeStateStatus,reviewDecision`, new comments/reviews since the last run, `gh pr checks`.
- Newly merged: `gh search prs --author <you> --merged --merged-at ">=<last run date>"`.
- Issues we commented on (STATE "waiting on maintainers"): new replies?

## 2. Respond (highest priority)
For each item, in this order: maintainer review comments → merge conflicts (DIRTY) → our CI failures → maintainer answers to our design questions.
- Code changes: brief `oss-worker` (local), validate yourself, `oss-qa` for anything non-trivial, then push (plain, or `--force-with-lease=<branch>:<old sha>` after a rebase). After any CHANGELOG rebase, diff the CHANGELOG for duplicate entries.
- Replies: short, specific, in the owner's voice; thank, say what changed and where (commit SHA).
- Restricted repos (POLICIES "Opens PR = the owner"): never post; draft the reply in `drafts/` and list it under "Needs you".
- On a merge: add a row to `CONTRIBUTIONS.md`, run `python3 scripts/update_readme.py`, add a post idea to `CONTENT.md`, thank the maintainer only if natural.

## 3. Community work (home repos: see STATE)
Once per run, pick one: `oss-reviewer` drafts a review on someone else's PR → validate (is it correct and useful?) → post as a PR comment; or reproduce/triage one fresh bug with a short, evidence-based comment. Never post low-value comments.

## 4. Scout (only if capacity)
Skip if ≥6 of our PRs await review, or the per-repo cap (2 awaiting first review) blocks the home repos, or 3 PRs were already opened today.
Brief `oss-worker` as scout: home repos first, then new repos, filtered through POLICIES.md (exclusions, AI policy, CLA/DCO). Require: open, unassigned, no competing PR/claim, clear spec, small diff, testable here. Ask for 4-6 ranked candidates; pick up to 3.

## 5. Pipeline per pick (run picks in parallel, ≤4 agents at once)
1. `oss-worker`: re-check competition → plan → (if design call needed: return question text; you post it in the owner's voice where allowed, then stop that pick) → code + tests + revert check + lint → commit (no trailers; `-s` if DCO) → draft PR body.
2. `oss-security` on the diff and the issue thread.
3. `oss-qa` cold review. FIX → re-brief coder (max 2 rounds), DROP → record why in TRACKER.
4. You validate: tests green, revert red, `git log upstream/main..HEAD --format=%B | grep -iE 'co-authored|generated-by'` empty, minimal diff, honest PR text, AI-disclosure line where the repo asks for it.
5. Ship: fork if needed (`gh repo fork --clone=false`), push, `gh pr create` with the draft body. Restricted repo → push only, add a pre-filled link to `drafts/OPEN-THESE.md`. Update CHANGELOG links to the PR number if the repo convention needs it.

## 6. Visibility
- README: if CONTRIBUTIONS.md changed, run `python3 scripts/update_readme.py` (updates the OSS section of <you>/<you>).
- Posts: keep 2-3 per week scheduled. If fewer than 2 are scheduled for the next 7 days, draft the next items from CONTENT.md (prefer fresh merges): write `content/posts/<nn>-<slug>.md` (LinkedIn long, X thread/short, Bluesky short), render the visual (`python3 scripts/render_cards.py content/posts/<file>.md`), check it by eye (Read the PNGs), run the humanizer skill on the text, then `your scheduler of choice`. Log id/URL in CONTENT.md.
- Public writing describes the work accurately, credits maintainers, and never contradicts the AI disclosures made in PRs.
- Articles: monthly; dev.to (`DEVTO_API_KEY` in `.env`) + Hashnode MCP cross-post; LinkedIn summary post linking it.

## 7. Close out (always)
- Rewrite `STATE.md` (open PRs table, waiting on the owner, waiting on maintainers, held, home repos, merged).
- Append a dated entry to `TRACKER.md` (what changed, SHAs, PR links, decisions).
- New corrections or maintainer patterns → `FEEDBACK.md`. New repo policy → `POLICIES.md`.
- Final message (concise): what merged / opened / replied / posted, then **Needs you (≤5 min)** with exact links or commands. Nothing else.
