# CLAUDE.md

Instructions for Claude Code working in this project.
Companion file `AGENTS.md` (for Codex) points at this one.

---

## Research methodology

Phase definitions, rules, and prompts live in `~/projects/research-process/`
(`PHASES.md`, `prompts/`). Outputs go in `notes/` here.

Project-specific operationalization on top of `PHASES.md`:
- Phase 0 (direction survey, optional) → typically Claude-only; output
  `notes/phase0_directions.md`. Use when the framing space is wide and you
  want a menu of viable designs before committing.
- Phase 1 (framing) → single-agent. Output `notes/problem.md` +
  `notes/phase1_commitments.md`.
- Phases 2 / 3 / 6 dual-independent → name files `_claude.md` / `_codex.md`,
  user reconciles into the canonical artifact.
- Phase 4 single-driver + reviewer → driver writes `notes/method_v1.md`;
  the other agent writes `notes/method_v1_review.md` (a review, not a
  counter-spec).
- Phase 5 (implementation) → Claude primary coder, Codex reviews diffs.
  Cluster paths, runtime hard rules, run commands, and code conventions
  live in `.agent/IMPLEMENTATION.md` — read it whenever you write or run
  code, propose sbatch, do EDA on disk data, or install dependencies.

## What this project is

<!-- EDIT: 3–5 sentences. What's the research question? What's the approach? What's the success criterion? -->

This project applies deep learning to <PROBLEM DOMAIN>. The core question is <QUESTION>. We're testing <APPROACH>. Success looks like <METRIC / DELIVERABLE>.

## Universal hard rules — do not violate

These apply in every phase. Phase-5-specific rules (sbatch, modules, pip,
tar, gpu pinning) live in `.agent/IMPLEMENTATION.md`.

1. **Never run `git push --force`.** Write the command, let the user run it.
2. **Never `rm` anything outside this repo.** `/scratch` and `/project` paths are never to be deleted by the agent.
3. **Never put API keys, tokens, or passwords in code, configs, or this repo.** Read them from env vars (`os.environ`). If a key seems missing, ask the user.
4. **Do not edit `RESEARCH_LOG.md` except to read it.** That's the user's journal.
5. **Do not read `notes/dryrun_*/` directories.** These are frozen archives of prior research-process cycles, kept for the user's reference. Reading them anchors current work to superseded framings and defeats the point of the restart. The user does any cross-cycle comparison manually; agents do not.

## Math + derivations

When the user asks for a derivation or to verify math:
- Show the steps, don't summarize. Flag hidden assumptions.
- If sign / index / sum-bound conventions are ambiguous, state which one you're using before solving.
- For physics terms (continuum mechanics, FEM, control), use the user's notation if given; otherwise default to standard textbook notation and say so.
- If you're unsure, say "I'm not sure" — don't guess.
- For load-bearing derivations (a new loss, a custom autograd, a numerical scheme), suggest the user run the same prompt past the secondary agent (Codex) for an independent derivation. Disagreement is a real signal.

## Coding posture

**Simplicity first.** Minimum code that solves the problem. No speculative features, no abstractions for single-use code, no flexibility that wasn't asked for, no error handling for impossible scenarios. If 200 lines could be 50, rewrite it. Senior-engineer test: would they call this overcomplicated? If yes, simplify.

**Surgical changes.** Touch only what the task requires. Don't "improve" adjacent code, comments, or formatting. Don't refactor working code or rewrite to your preferred style — match what's there. Remove only the imports / variables / functions that *your* changes orphaned; leave pre-existing dead code alone (mention it, don't delete it). Test: every changed line should trace directly to the user's request.

**Goal-driven execution.** Convert the task into verifiable goals before starting. For multi-step work, state a plan with a verify step per item:
```
1. [step] → verify: [check]
2. [step] → verify: [check]
```
For research code, "verify" is usually a sanity check (loss decreases, shapes match, one batch trains end-to-end, gradients are finite) rather than a unit test. Weak criteria ("make it work") cost a reorientation round-trip; strong criteria let the loop close without checking in.

## Working pattern

Every session, at the start:
1. Read this file.
2. Read `RESEARCH_LOG.md` (most recent entries) to learn the current state.
3. Read `.agent/HANDOFF.md` to learn the in-flight task.
4. Run `git status` and `git log -5 --oneline` to see what changed since last session.
5. Ask the user what to focus on.

## Handoff between agents

The user switches between Claude Code and Codex frequently when usage limits are hit. Limits often hit without warning, so **keep `.agent/HANDOFF.md` current proactively** — update it after each meaningful step (file written, decision made, next-step identified), not only at user-warned switch time.

- `.agent/HANDOFF.md` content: current task, status (done / in-progress / blocked), where to resume (file paths, line numbers, or specific `notes/` artifacts), open questions for the user, files touched this session.
- HANDOFF.md is overwritten on each switch — not appended.
- Lasting lessons go in `RESEARCH_LOG.md`, not HANDOFF.md.
- The user-facing switch protocol lives in `.agent/SWITCH.md`. The copy-paste reorient prompt for the incoming agent lives in `.agent/REORIENT_PROMPT.md`.
- If the user signals a phase boundary (e.g. "Phase 1 done"), the phase artifact in `notes/` is the durable record; HANDOFF.md just points at it.

## Parallel work with the other agent

The user runs Claude Code and Codex side-by-side sometimes. When you see a prompt that says "save your output to a specific filename" or "don't read the other agent's output," that's a parallel-work signal. Respect it — write only to the named file, don't peek at the sibling file. The user wants independent outputs to compare.

Disagreement with the other agent is the goal in these cases. State your reasoning clearly so a diff is meaningful.

## Current focus

<!-- EDIT WEEKLY. One short paragraph: what we're trying right now, what's on hold, what's broken / don't touch. -->

Setting up the project skeleton. First milestone is replacing placeholders in `src/foo/` with the real dataset loader and model.
