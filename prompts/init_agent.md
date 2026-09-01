Initialize the **Journey with AnandTech — DevOps Zero to Production** project.

## Phase 1 — Load governing context

Before planning, generating, reviewing, or modifying anything:

1. Read `AGENTS.md` completely.
2. Locate and read `master_prompt.md` completely.

   * Check the repository root first.
   * If it is not there, check `docs/master_prompt.md`.
3. Locate and read `project_SSOT.md` completely, if it exists.
4. Determine the active course section from the project SSOT or repository state.
5. Locate and read the active section’s `SSOT.md` completely.
6. Inspect the active section’s directory structure.
7. Read only the accepted previous units and relevant examples needed to understand continuity and quality expectations.
8. Do not treat example units or existing drafts as sources of truth.
9. Do not modify, create, rename, delete, package, or regenerate files during this loading phase.

## Authority order

When instructions conflict, use this order:

1. My latest explicit instruction
2. The locked active-section `SSOT.md`
3. `project_SSOT.md`
4. `master_prompt.md`
5. Accepted earlier units
6. Draft units and examples
7. General assumptions

Do not silently resolve conflicts between locked sources.

## Required initialization report

After loading the files, report:

### 1. Files loaded

List every governing file loaded using its repository-relative path.

### 2. Current project state

Identify:

* canonical project name;
* active section;
* active unit, if defined;
* current workflow phase;
* section lock status;
* approved lab environment;
* required deliverable;
* last accepted checkpoint.

### 3. Authority verification

State which file is authoritative for:

* course-wide standards;
* active-section scope;
* unit order;
* lab environment;
* artifacts;
* assessments;
* packaging.

### 4. Conflicts and stale instructions

Report any conflict involving:

* active section or unit;
* locked versus draft status;
* VM or lab requirements;
* unit ordering;
* technology choices;
* naming conventions;
* required artifacts;
* packaging permission.

Quote only the minimum text needed to identify each conflict.

### 5. Missing information

List anything required before safe authoring can begin.

Do not invent missing decisions.

### 6. Recommended next action

Recommend exactly one next action, such as:

* draft or revise the active-section SSOT;
* request explicit SSOT lock;
* generate one authorized unit;
* review an existing unit;
* validate the section;
* package an accepted section.

## Stop condition

Stop after presenting the initialization report.

Do not edit any files until I give the next instruction.