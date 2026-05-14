# AGENTS.md

Instructions for OpenAI Codex working in this project.

## Single source of truth

**Read `CLAUDE.md`** in this repo first — research methodology, universal hard rules, math conventions, coding posture, session protocol, and current focus.

When reviewing or writing code (Phase 5 work), also read `.agent/IMPLEMENTATION.md` — cluster paths, runtime hard rules, run commands, code conventions. For methodology / framing / literature / brainstorm / spec work (no code), you don't need it.

This file only adds Codex-specific notes on top of those two.

## Codex-specific notes

- Codex's role here is **secondary**: cross-checking math derivations and reviewing diffs from the primary agent. The user runs Codex when they want a second opinion, not for general daily coding.
- When asked to verify a derivation or independently derive something, do it from scratch — do not look at how the primary agent solved it. If the user provided the primary's answer, treat it as a hypothesis to test, not as ground truth.
- Disagreement with the primary agent is the useful output. State the disagreement clearly: where, why, which step, what assumption.

## Per-phase agent pattern

The per-phase dual-vs-single convention lives in `CLAUDE.md` under
"Research methodology." Highlights for Codex specifically:

- **Phase 1** is single-agent. If the user runs Phase 1 with Claude, do
  not produce a parallel `problem_codex.md` — it's not the workflow.
- **Phases 2, 3, 6** are dual-independent. Codex produces its own file
  with the `_codex.md` suffix; do not read the Claude sibling.
- **Phase 4** is single-driver + reviewer. If Claude wrote the spec,
  Codex enters second-reviewer mode and writes `notes/method_v1_review.md`
  — a review, not a counter-spec. If Codex is the driver instead, Claude
  reviews.
- **Phase 5** is Claude-primary; Codex reviews diffs.

## Phase-boundary checking protocol

When the user says a research-process phase is done (for example, "Phase 1
done", "phase 2 done", or "check Phase 3"), Codex should proactively switch
into second-reviewer mode:

1. Read `CLAUDE.md`, `RESEARCH_LOG.md`, the relevant `notes/` artifact for
   that phase, and any handoff file if present.
2. Tell the user the checking plan before doing substantive review.
3. Review independently and skeptically. Do not optimize for agreement with
   Claude's framing or method.
4. Report: what the phase artifact claims, what assumptions are load-bearing,
   what could fail, where Codex disagrees with Claude or the artifact, and
   whether the project is ready to move to the next phase.
5. Do not edit canonical phase artifacts unless the user explicitly asks.

## Handoff between agents

The user switches between Claude Code and Codex frequently when usage
limits are hit. Limits often hit without warning, so **keep
`.agent/HANDOFF.md` current proactively** — update it after each
meaningful step (file written, decision made, next-step identified),
not only at user-warned switch time.

- `.agent/HANDOFF.md` content: current task, status, where to resume
  (file paths, line numbers, or specific `notes/` artifacts), open
  questions for the user, files touched this session.
- HANDOFF.md is overwritten on each switch — not appended.
- Lasting lessons go in `RESEARCH_LOG.md`, not HANDOFF.md.
- The user-facing switch protocol lives in `.agent/SWITCH.md`. The
  copy-paste reorient prompt for the incoming agent lives in
  `.agent/REORIENT_PROMPT.md`. `.agent/CODEX_BOOTSTRAP.md` is the
  Codex-specific entry point.
- When taking over from Claude as the primary, follow the reorient
  prompt: read project rules, recent log, handoff, phase artifacts,
  git state, then summarize back before acting. Disagreement with
  what the prior agent recorded is useful — call it out.
- When summoned for an independent cross-check (math derivation,
  Phase 3 brainstorm, Phase artifact review), do NOT use the resume
  flow — see "Phase-boundary checking protocol" above and the
  second-reviewer notes above.

## Hard rules

Universal rules (apply in every phase) live in `CLAUDE.md`: `git push --force`, `rm` outside repo, API keys, `RESEARCH_LOG.md` read-only, `notes/dryrun_*/` no-read.

Cluster / runtime rules (apply when reviewing or writing code) live in `.agent/IMPLEMENTATION.md`: `sbatch`/`scancel`, `module purge`, `pip install`, `tar`/`gzip` on xfer node, GPU type pinning.

## Differences from `CLAUDE.md` to be aware of

- Claude-specific tooling (`.agent/skills/`, `.agent/subagents/`) is for Claude Code only. Codex has its own equivalents (profiles / prompts) which live alongside in `.agent/prompts/` if used.
- Cloud-mode Codex tasks should be avoided for this project — runs need to happen on GACRC where the data is.
