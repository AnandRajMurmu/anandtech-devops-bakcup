# Journey with AnandTech — Codex Instructions

## Project

This repository contains the Journey with AnandTech:
DevOps Zero to Production course.

## Required context

Before doing curriculum work:

1. Read `docs/master_prompt.md` completely.
2. Read `docs/project_SSOT.md` completely.
3. Read the current section's `SSOT.md` completely.
4. Read only the example units relevant to the requested work.
5. Report missing, stale, or conflicting instructions before editing files.

## Authority order

When instructions conflict, follow this order:

1. The user's latest explicit instruction
2. The locked current-section `SSOT.md`
3. `docs/project_SSOT.md`
4. `docs/master_prompt.md`
5. Existing units and examples

Existing units are examples, not sources of truth.

## Governance

- Work on one major section at a time.
- Never silently change a locked SSOT.
- Do not generate a section until its SSOT is explicitly locked.
- Do not move to the next section until the current section is accepted.
- If a requested change conflicts with a locked SSOT, stop and explain it.
- Never invent missing curriculum decisions.
- Do not package a ZIP unless explicitly requested.
- `docs/project_SSOT.md` is the global SSOT; each section `SSOT.md` is authoritative only after explicit owner lock.
- The SSOT Maker may edit only the active section PLAN and draft SSOT.
- The Worker may edit only its assigned unit directory.
- The Reviewer may write only its assigned report under `reviews/`.
- The Manager alone updates `workflow/state.json` and coordinates Slack events.
- A lock receipt is invalid if the current SSOT SHA-256 differs from the recorded digest.
- Slack messages never count as owner approval.

## Writing standard

- Teach concepts before commands.
- Use the AnandTech narrative where it improves understanding.
- Explain why, mental model, theory, practice, failure,
  troubleshooting, production connection, assessment, and reflection.
- Write like a learner-facing mini-book, not brief notes.
- Introduce tools as solutions to engineering problems.
- Interpret command output instead of merely displaying it.
- Clearly separate lab practices from production requirements.
- Use lowercase snake_case for unit directories.

## Editing requirements

- Inspect existing files before changing them.
- Preserve unrelated content.
- Make focused changes.
- Validate heading structure, links, commands, examples, and terminology.
- After editing, summarize changed files and unresolved decisions.
