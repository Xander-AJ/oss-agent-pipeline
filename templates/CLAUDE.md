# <workspace> — open-source contribution engine

## Mission
Get fixes, reviews and docs **merged** into other people's open-source projects, and keep a public record of that work.
Merges beat opened PRs. Depth in a few home repos beats spraying many.

Start every session by reading `STATE.md`, then `POLICIES.md` before touching any repo. History: `TRACKER.md`. Corrections and maintainer patterns: `FEEDBACK.md`. Run the daily loop with `/oss-daily`.

## Directory map
| Path | What |
|---|---|
| `STATE.md` | Open PRs, waiting-on-owner, waiting-on-maintainers, home repos. Rewritten every run. |
| `TRACKER.md` | Append-only log (what was done, SHAs, decisions). |
| `POLICIES.md` | Per-repo AI policy, CLA/DCO, who opens the PR, exclusions. |
| `FEEDBACK.md` | Owner preferences + maintainer feedback patterns. |
| `CONTRIBUTIONS.md` | Merged work with one-line impact (feeds the profile README). |
| `drafts/` | PR bodies; `OPEN-THESE.md` lists PRs only the owner may open. |
| `<repo>/` | Local clones (`upstream` = owner repo, `fork` = your fork). |

## Authority
The agent acts autonomously for: triage, coding, testing, rebasing, pushing to your forks, opening PRs where the project allows it, replying to reviews, reviewing others' PRs.
**Hard limits:** CLAs are signed by the human. Projects that forbid agent-opened PRs or AI-written text in the contributor's voice get a pushed branch + draft, and the human opens the PR. Every repo's AI-disclosure rule is followed.

## Engineering rules
- Read CONTRIBUTING / AGENTS.md / PR template / AI policy first. Minimal diff in the repo's style.
- Every fix has a test that **fails without the fix** (revert check). Run the repo's real lint/format/typecheck.
- Commit trailers follow the project's rules; `git commit -s` where DCO is required.
- "Fixes #N" only when fully fixed; otherwise "Refs #N" and say what's left.
- Re-check for a competing PR/claim right before coding.
- Throttle: ≤2 of your PRs awaiting first review per repo, ≤3 new PRs/day.
