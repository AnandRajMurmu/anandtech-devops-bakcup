# Agent Workflow Contract

`state.json` is the Manager-owned operational record. It is not a curriculum authority and cannot override an SSOT.

## State progression

| Phase | Who can act | Exit condition |
|---|---|---|
| `ssot_draft` | SSOT Maker | Draft is reviewable |
| `awaiting_ssot_lock` | Owner or SSOT Maker | Owner enters exact lock confirmation |
| `ready_for_generation` | Manager | Lock digest validates |
| `generating` | Manager, Worker, Reviewer | Every unit is approved or a blocker is raised |
| `blocked` | Owner/Manager | Blocker is resolved and run is explicitly resumed |
| `awaiting_owner_confirmation` | Owner | Owner enters exact section acceptance |
| `accepted` | Owner/Manager | The next section is explicitly activated |

## Lock protocol

The owner command must contain the exact confirmation `LOCK SECTION NN`. The Manager validates required SSOT sections, changes the draft marker to Locked, parses the unit register, and records the exact file SHA-256. Any later SSOT change invalidates generation until it is reviewed and locked again.

## Unit loop

The Manager sends one unit to the Worker, persists the returned files only within that unit directory, and sends the saved content to the Reviewer. A BLOCKED decision must contain actionable findings and returns to the same Worker. An APPROVED decision must have no blocking findings. The default maximum is five repair cycles.

Review reports are machine-readable JSON at `reviews/<section_slug>/unitNN_review.json`.

## Slack events

The Manager emits:

- one event after each unit is approved;
- one event after all section units are approved and owner confirmation is required.

Event keys are stored in `state.json` to prevent duplicate messages. Without a configured webhook, events remain `pending_configuration`; the workflow continues because notification delivery is not curriculum approval.

Run `anandtech-agents retry-notifications` after configuring or recovering Slack. Successfully sent events remain idempotent and are not duplicated.

Use an incoming webhook bound to the desired channel and provide it through `ANANDTECH_SLACK_WEBHOOK_URL`. Never store the webhook in the repository.

## Recovery

- If an LLM request fails, rerun the same command; completed approved units are skipped.
- If a unit exceeds the revision limit, inspect its last review report, resolve the blocker or adjust the approved boundary through the SSOT process, then resume explicitly.
- If a locked SSOT changes, do not edit the digest manually. Return the section to draft review and create a new explicit lock.
- Git remains the audit and recovery layer for content; use a feature branch and review changes before merging.
