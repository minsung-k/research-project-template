# Codex bootstrap / resume

The switch-in prompt is the same for either agent. Use:

```bash
cat .agent/REORIENT_PROMPT.md
```

and paste the contents into Codex as the first message.

The reorient prompt tells Codex to read `AGENTS.md` first (which points
at `CLAUDE.md` for project rules), `RESEARCH_LOG.md`, `HANDOFF.md`, any
phase artifacts in `notes/`, and `git` state — then summarize before
acting.

## When Codex is the secondary (cross-check), not the primary

If you are summoning Codex for an independent second opinion — verifying
a derivation, Phase 3 brainstorm, reviewing a Phase artifact — do NOT
use the resume flow. Instead:

- Do not paste Claude's prior output. Independence is the point.
- Use the appropriate phase prompt from
  `~/projects/research-process/prompts/` (e.g. `phase3_brainstorm.md`),
  or hand Codex the bare problem/derivation and ask for a fresh derivation.
- See `AGENTS.md` for the second-reviewer protocol.
