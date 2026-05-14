# .agent/

Project-specific agent assets. Populate over time, not on day one.

```
.agent/
├── CODEX_BOOTSTRAP.md   # Codex-specific entry point
├── HANDOFF.md           # live state of in-flight work (overwritten each switch)
├── IMPLEMENTATION.md    # cluster paths + runtime rules + code conventions
├── REORIENT_PROMPT.md   # copy-paste prompt for incoming agent on switch
├── SWITCH.md            # user-facing switch protocol
├── skills/              # Claude Code custom skills (when you build them)
├── subagents/           # Claude Code subagent definitions
└── prompts/             # Reusable prompt fragments (works for both agents)
```

Don't build skills or subagents until you've used the agents for ~2 weeks
and noticed where you're repeating yourself. Premature skills are busywork.

Likely first candidates:

- `hpc-job-writer` (skill): generate sbatch scripts following our conventions.
- `run-analyzer` (subagent): summarize a finished run dir on /scratch.
- `derivation-checker` (subagent): independently work out a math derivation.
- `sapelo-doctor` (skill): diagnose stuck/failed/killed jobs via sacct/seff.
