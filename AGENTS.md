# AGENTS.md

Instructions for OpenAI Codex working in this project.

## Single source of truth

**Read `CLAUDE.md`** in this repo first. All project conventions, hard rules, code style, run pattern, and current focus are there. This file only adds Codex-specific notes.

## Codex-specific notes

- Codex's role here is **secondary**: cross-checking math derivations and reviewing diffs from the primary agent. The user runs Codex when they want a second opinion, not for general daily coding.
- When asked to verify a derivation or independently derive something, do it from scratch — do not look at how the primary agent solved it. If the user provided the primary's answer, treat it as a hypothesis to test, not as ground truth.
- Disagreement with the primary agent is the useful output. State the disagreement clearly: where, why, which step, what assumption.

## Hard rules

Same as `CLAUDE.md`. Notably:
- No `sbatch`, `scancel`, `git push --force`, no `pip install` without saying so, no `rm` outside this repo, no API keys in files.
- This is GACRC Sapelo2. Code in `/home`, run output in `/scratch`, archives in `/project`. Read paths from env vars, never hardcode.

## Differences from `CLAUDE.md` to be aware of

- The Anthropic-specific tooling references in `CLAUDE.md` (skills, subagents in `.agent/`) are for Claude Code only. Codex has its own equivalents (profiles / prompts) which live alongside in `.agent/prompts/` if used.
- Cloud-mode Codex tasks should be avoided for this project — runs need to happen on GACRC where the data is.
