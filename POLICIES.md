# Repo policies

Check this before scouting, coding, or posting anywhere. Add a row whenever you read a new repo's CONTRIBUTING / AGENTS.md / AI policy. Last verified dates matter: policies change.

Legend — **Opens PR**: `Claude` = Claude may open + reply in the owner's voice; `the owner` = push branch + draft, the owner opens and handles discussion.

## Active / worked repos
| Repo | Opens PR | AI rule | CLA / DCO | Notes |
|---|---|---|---|---|
| QwenLM/qwen-code | Claude | No ban. AGENTS.md hard-blocks large production diffs; `packages/core/**`, `config/**` are backbone (needs 100% confidence + maintainer call). | None | Home repo. Review bot is noisy (multi-round). wenshao is the human reviewer. |
| besu-eth/besu | Claude | No ban found | DCO (`-s`) | Home repo. CHANGELOG under `## Unreleased`; breaking changes under Breaking Changes; link PR number. Conflicts on CHANGELOG are constant → rebase + force-with-lease. |
| dessalines/thumb-key | Claude | None | None | Few open issues; no unit-test infra. |
| paradedb/paradedb | Claude | "Use of AI Tools": allowed, no slop, must understand code | **CLA** (the owner) | `/take` to claim. Cherry-pick label check is maintainer-only. |
| ratatui/ratatui | Claude | Welcomes AI; **attribution required in PR body** | None | |
| perses/perses (+ perses/shared) | Claude | AGENTS.md AI contributor guide; disclosure encouraged (#4552) | DCO | UI code lives in perses/shared (issues disabled there). |
| authlib/authlib | Claude | None found | None | Reviews welcome. |
| kubeflow/pipelines | Claude | None found | DCO | SDK needs venv/pip (blocked in auto mode). |
| trufflesecurity/trufflehog | Claude | None found | **CLA** (the owner) | |
| chrisbanes/haze | Claude | AGENTS.md (Gradle `--no-scan`, screenshot rules) | None | Single maintainer. |
| sustainable-computing-io/kepler | Claude | LF Generative AI policy | DCO | |
| caddyserver/caddy | **the owner** | Agents may not open PRs; human-written comments; disclose model | **CLA** | Branch naming: no slashes. Claim issue first. |
| rust-lang/rust-analyzer | **the owner** | AI_POLICY: agents must not open PRs; text in own words | None | |
| pandas-dev/pandas | **the owner** | AGENTS.md: agents never take GitHub actions; disclose tool/model/effort | None | |
| typescript-eslint/typescript-eslint | **the owner** | PR description in own words; no force-push after opening | None | |
| quarto-dev/quarto-cli | **the owner** | Human must review + test before opening; autonomous agent PRs bannable | None | |
| grpc/grpc-java | **the owner** | All communication human-authored; no agents publishing | LF EasyCLA | |
| ducaale/xh | — | — | — | Owner silently closed 3 same-approach PRs on #473. Skip that issue. |

## Excluded (do not contribute)
| Repo | Reason |
|---|---|
| alacritty, comrak, tealdeer, shadcn-svelte, syncthing, wasmtime (Bytecode Alliance), go-task, bottom, feishin, matcha, servo | Ban LLM-generated contributions |
| pytest, traefik, mudler/LocalAI, otel collector-contrib | Require AI trailers (Co-authored-by / Assisted-by) — conflicts with no-trailer rule |
| langchain-ai/langgraph, langchainjs, modelcontextprotocol/python-sdk, pydantic-ai | Auto-close PRs from authors not assigned to the issue |
| openai/openai-agents-python | PR creation restricted to collaborators |
| agent-substrate/substrate | Human-only DCO, no AI commit messages |
| spiceai | Requires runtime evidence from running `spiced` |
| lazygit | Discourages PRs |
| mem0 | Mandatory CLA + crowded |

## Scouting lessons
- Fresh labelled issues in big repos get a PR or claim within hours (~70% of candidates already taken). Re-check right before coding.
- Staff-filed batches (dolt, questdb) get fixed in-house. Skip.
- Prefer repos where we already have a fork and a maintainer relationship.
