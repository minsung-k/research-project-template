Read these files in order, then summarize back to me what you understand
about the current state before doing anything:

1. `CLAUDE.md` (or `AGENTS.md` if you are Codex) — project rules.
2. `RESEARCH_LOG.md` — most recent 2–3 entries.
3. `.agent/HANDOFF.md` — the in-progress task from the previous agent.
4. If `HANDOFF.md` names an active research-process phase or points at
   files in `notes/`, read those artifacts too (e.g. `notes/problem.md`,
   `notes/phase1_commitments.md`, `notes/litreview.md`,
   `notes/methods_*.md`, `notes/method_v1.md`, etc.).
5. `git log -10 --oneline` and `git status` — recent commits and
   uncommitted changes.

Then summarize:
- What the project is and where we are in the research process.
- What the previous agent was doing and what the immediate next step is.
- Any open questions or decisions you saw flagged for me.
- Anything in the handoff or notes that looks stale, contradictory, or
  unclear — call it out, don't paper over it.

Don't start working until you've shown me your understanding and I've
confirmed it. If your summary disagrees with what the prior agent
recorded, say so explicitly — that's useful, not a problem.
