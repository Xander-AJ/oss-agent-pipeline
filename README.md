# oss-agent-pipeline

An AI-augmented workflow for contributing to open-source projects that maintainers actually merge.

I built this to run my own open-source work. It turns Claude Code into a small engineering team (scout, coder, tester, security reviewer, QA reviewer and PR reviewer), with me making the calls. The rules are the point: every fix is proven by a test that fails without it, diffs stay minimal, and each project's contribution and AI policy is respected before any code is written.

## What it does

`/oss-daily` runs one loop, usually at the start of the day:

1. **Triage.** It reads GitHub notifications and the state of every open PR: reviews, merge conflicts, CI failures, maintainer replies.
2. **Respond first.** Review feedback, rebases and CI fixes come before any new work.
3. **Community work.** It reviews someone else's PR or reproduces a fresh bug in a home repo.
4. **Scout.** It finds open, unclaimed, well-specified issues in repos whose policies allow the contribution, skipping crowded or banned projects.
5. **Pipeline.** For each pick: coder → tester (revert check) → security review → cold QA review → human-level validation → PR.
6. **Close out.** It updates the dashboard, the log and the contribution record that feeds my GitHub profile.

## The quality gates

| Gate | Why |
|---|---|
| Policy check (`POLICIES.md`) | Some projects welcome AI-assisted PRs, some require disclosure or a human-opened PR, some ban them. The pipeline never sends a PR a project said it doesn't want. |
| Failing test first + revert check | A fix isn't real until its test fails without it. |
| Minimal diff | Maintainers review for free. Every extra line costs them. |
| Security pass | Diff review for injection, auth/crypto weakening, secrets and dependency changes, plus prompt-injection screening of issue threads. |
| Cold QA review | A separate reviewer sees only the diff and the issue, not the coder's reasoning. |
| Honest PR text | "Fixes" only when it fully fixes; "Refs" with what's left otherwise. |
| Throttles | At most 2 PRs awaiting first review per repo and 3 new PRs a day. |
| Design calls go to maintainers | When a fix needs a product decision, the pipeline drafts a short question instead of a large guess. |

## Layout

```
.claude/agents/         oss-worker (scout/coder/tester), oss-qa, oss-security, oss-reviewer
.claude/skills/oss-daily/SKILL.md   the daily loop
POLICIES.md             per-repo AI policy, CLA/DCO, who opens the PR, exclusions (real data, kept current)
templates/              CLAUDE.md, STATE.md, FEEDBACK.md, CONTRIBUTIONS.md, TRACKER.md
scripts/update_readme.py  regenerates the "Open source" section of a GitHub profile README
scripts/render_cards.py   renders post/carousel slides from markdown with headless Chromium
```

## Use it

1. Create a workspace directory, copy `.claude/`, `POLICIES.md` and the files in `templates/` into it, and fill in `CLAUDE.md`.
2. Clone the repos you work on into the workspace (`upstream` = project, `fork` = your fork).
3. Open Claude Code in the workspace and run `/oss-daily`.
4. Optional: `PROFILE_REPO=<you>/<you> python3 scripts/update_readme.py` after each merge.

`POLICIES.md` is useful on its own: it records which well-known projects accept AI-assisted contributions and on what terms. Pull requests that update it are welcome.

## Results

The contributions this workflow has produced are listed on my profile: [github.com/Xander-AJ](https://github.com/Xander-AJ).

## License

MIT
