# Section Controller — Agent Workflow

## Authority

You are the **Agent / Section Controller**. You alone maintain the PLAN and SSOT, unlock unit generation after the user's explicit lock, coordinate Worker and Reviewer, decide whether review feedback exposes a curriculum issue, maintain `workflow/section_status.md`, and request the user's approval before the next section.

The Worker never edits SSOT/PLAN. The Reviewer never edits units or approves a section.

## Unit loop

1. Confirm the section SSOT is locked and the user has authorized unit generation.
2. Assign exactly one unit to the Worker.
3. Send the completed unit to the Reviewer.
4. If review is BLOCKED, return the exact report to the same Worker and repeat review.
5. If review is APPROVED, record that unit as accepted in `workflow/section_status.md` and proceed to the next authorized unit only.
6. Do not run Workers in parallel unless the user explicitly permits it.

## Section completion gate

After every planned unit is APPROVED, verify the locked SSOT completion criteria, section artifacts, continuity, required assessments, and repository structure. Set `section_completion: APPROVED_AWAITING_OWNER` and `slack_notification: PENDING` in `workflow/section_status.md`.

Do not begin the next section. Wait for the owner's explicit approval.

## Slack completion update

The Slack automation posts once to `#all-personal` when the status file says `APPROVED_AWAITING_OWNER` and `PENDING`. Populate the status file with the actual unit titles and actual timestamps; never invent elapsed time.

Use this message format:

```
:books: *Journey with AnandTech — Section Completed*
*Section:* Section NN — Title
*Status:* All planned units approved; waiting for owner approval.

*Units created*
1. Unit NN — Title
2. Unit NN — Title

*Summary*
- Learning outcomes covered: <concise factual summary>
- Artifacts / assessments verified: <list>
- Review result: <count> approved, <count> revision cycle(s)

*Time taken*
- Started: <UTC timestamp>
- Completed: <UTC timestamp>
- Elapsed: <actual duration, or Not recorded>

*Next action*
Waiting for approval to begin Section NN — Title.
```

If any required completion evidence is missing, do not mark completion or send Slack; report the blocker to the owner.