# Switching agents mid-task

When one agent hits its usage limit and you want to continue with the
other (Claude ↔ Codex), follow this.

## Three steps

1. **Before the switch** (or at the user-warning, if you have one): tell
   the active agent to update `.agent/HANDOFF.md` and commit any stable
   file edits. If the limit already hit cold, skip — `HANDOFF.md` should
   already be current because the agent updates it after each meaningful
   step.

2. **Open the other agent.** Codex if you were on Claude; Claude if you
   were on Codex.

3. **Paste this verbatim** as the first message:

   ```bash
   cat .agent/REORIENT_PROMPT.md
   ```

   into the new agent's terminal/chat — or actually `cat` it on your
   side and paste the contents. The prompt tells the new agent which
   files to read and to summarize back before doing anything.

4. **Wait for the summary, confirm it.** Don't let the new agent start
   working until you've confirmed it picked up the right context.

## What survives a switch

| Lives on disk (survives)            | Lives only in conversation (lost) |
|-------------------------------------|-----------------------------------|
| `notes/phase*.md` artifacts         | In-flight discussion not yet written |
| `RESEARCH_LOG.md` entries           | Working hypotheses not yet committed |
| `.agent/HANDOFF.md`                 | TODOs you only stated in chat    |
| Code in `src/`, configs, sbatch     | Mental model the agent built up  |

`HANDOFF.md` exists to evacuate the right column to the left column.
Keep it current.

## Mid-phase switches

The research-process phases (`~/projects/research-process/PHASES.md`)
each produce an artifact in `notes/`. The artifact survives a switch.
What's risky is the mid-phase mental state.

- **Phase 2 (lit triage):** artifact is `notes/litreview.md`. Append
  findings as you go, not at the end. Partial `litreview.md` +
  `HANDOFF.md`'s "where to resume" line is enough to continue.
- **Phase 3 (brainstorm):** each agent writes `notes/methods_<agent>.md`
  independently. Switching mid-Phase 3 is unusual because the design is
  two-agent-independent. If it happens, the new agent finishes the file
  the prior agent was on, and notes "completed by the other agent at
  <date>" inline.
- **Phase 4 (method spec):** one deep file (`notes/method_v1.md`).
  Append-as-you-go.
- **Phase 5 (implementation):** code is the artifact. `HANDOFF.md`
  carries the file/line where the next agent picks up.
- **Phase 6 (kill or continue):** one short file
  (`notes/decision_<date>.md`) — short enough to write in one sitting,
  switching is rarely needed.

## Don't

- Don't manually summarize the previous agent's conversation for the
  new one. The reorient prompt + on-disk artifacts are the contract.
  Manual summaries leak through your priors.
- Don't let the new agent start before it shows you what it understood.
  Sycophancy + missing context = silent drift.
- Don't manually merge two agents' parallel outputs without diffing
  them. In Phase 3 (and any other parallel-work setting), disagreement
  is signal, not noise.
- Don't paste both agents' previous outputs into the new agent unless
  you've decided you want them to be biased by the prior. For
  cross-checks (math derivations, Phase 3), the whole point is
  independence.
