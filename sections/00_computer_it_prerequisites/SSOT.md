# Section 00 — Computer and IT Prerequisites — SSOT

**Document type:** Section-level source of truth

**Lock status:** Draft

**Section version:** 0.1

**Package name after separate packaging authorization:** `00_computer_it_prerequisites.zip`

## Section Purpose

Give an absolute beginner the computing mental models needed to reason about software and infrastructure before professional DevOps tooling appears. The learner should finish able to trace a simple user action through hardware, operating system, process, memory, storage, identity, network, and application layers, then investigate a bounded failure using evidence.

## Learner Starting Point

The learner can use an ordinary computer but may not know Linux, networking, programming, cloud, virtualization, or professional operations. No terminal experience, administrative access, VM, cloud account, or paid service is required.

## Section Learning Outcomes

By the end of the section, the learner can:

1. trace how instructions and data move through a computer;
2. explain the operating system's role between applications and hardware;
3. distinguish programs, processes, and threads;
4. reason about memory allocation, virtual memory, and memory pressure;
5. distinguish storage devices, partitions, filesystems, paths, and mounts;
6. distinguish identity, authentication, authorization, ownership, and permissions;
7. trace a client request through interface, IP, route, DNS, port, and service;
8. map frontend, backend, API, database, configuration, logs, and state;
9. explain terminals, shells, commands, arguments, streams, pipes, and redirection;
10. investigate a failure using symptom → evidence → hypothesis → test → recovery → verification → prevention.

## Unit Register

### Unit 01 — How a Computer Actually Works

**Directory:** `unit01_how_a_computer_actually_works`

Build the execution mental model: instructions, CPU, cores, clock, registers/cache intuition, RAM, persistent storage, buses, and input/output. Trace opening a small application. Exclude electronics design, assembly programming, CPU microarchitecture depth, and benchmarking. The learner produces a labeled execution-flow sketch and explains one bottleneck without equating clock speed with total performance.

### Unit 02 — Operating Systems: The Layer Between Software and Hardware

**Directory:** `unit02_operating_systems`

Explain kernel and user space, system calls at an intuitive level, hardware abstraction, scheduling, memory/device/filesystem management, applications, services, and failure boundaries. Compare operating-system families only to clarify shared responsibilities. Exclude installation, bootloader internals, Linux administration, and kernel development. The learner traces how an application requests a protected resource.

### Unit 03 — Programs, Processes, and Threads

**Directory:** `unit03_programs_processes_and_threads`

Distinguish a stored executable from a running process; introduce PID, state, isolation, parent/child relationships, exit codes, threads, concurrency, and safe observation. Exclude detailed schedulers, signals administration, containers, and performance tuning. The learner interprets a small process snapshot and explains why closing a window, ending a process, and deleting a program are different actions.

### Unit 04 — Memory: What Your Application Actually Uses

**Directory:** `unit04_memory`

Teach bytes, addresses, allocation, stack/heap intuition, virtual memory, paging, swap, caching boundaries, memory pressure, leaks, and out-of-memory failure. Analogies must state their limits. Exclude allocator implementation, kernel tuning, garbage-collector internals, and capacity engineering. The learner diagnoses a bounded memory-pressure scenario from supplied evidence.

### Unit 05 — Storage and Filesystems

**Directory:** `unit05_storage_and_filesystems`

Separate volatile memory from persistent storage; explain devices, partitions, filesystems, files/directories, paths, metadata, mounts, free space, permissions interaction, deletion, and data-loss boundaries. Exclude disk administration commands, RAID implementation, distributed storage, and filesystem repair. The learner maps a path to the layers that make its data persistent and explains why “deleted” and “securely erased” differ.

### Unit 06 — Users, Identity, and Permissions

**Directory:** `unit06_users_identity_and_permissions`

Explain users, groups, service identities, ownership, authentication, authorization, permissions, sessions, privilege, least privilege, and auditability. Use safe scenarios rather than real credentials. Exclude Linux permission-command mastery, IAM products, directory-service administration, and cryptographic protocol depth. The learner decides which identity needs which minimum access and justifies it.

### Unit 07 — Networking Fundamentals

**Directory:** `unit07_networking_fundamentals`

Build a request-path model using interfaces, links, IP addresses, subnets at an intuitive level, routes, gateways, DNS, ports, protocols, firewalls, clients, and servers. Interpret a simple success/failure evidence set. Exclude subnet calculation drills, packet-capture mastery, network-device configuration, and cloud networking. The learner traces a browser request and identifies the next observation at each boundary.

### Unit 08 — Applications and Services

**Directory:** `unit08_applications_and_services`

Map frontend, backend, API, database, dependencies, configuration, environment, logs, state, startup, health, and user-visible behavior. Explain why a running process does not prove a healthy service. Exclude application programming, database administration, web-server configuration, and deployment automation. The learner produces a dependency map for the AnandTech Todo application and interprets a partial-failure scenario.

### Unit 09 — Terminal and Command-Line Foundations

**Directory:** `unit09_terminal_and_command_line_foundations`

Explain terminal versus shell, prompt, command, executable, arguments, options, current directory, paths, standard input/output/error, exit status, pipes, redirection, quoting intuition, help, history, and safe observation-before-change. Provide platform-labeled examples without requiring one universal shell. Exclude shell scripting, Linux command breadth, remote shells, and privileged administration. The learner reads and safely adapts a short command pipeline.

### Unit 10 — Troubleshooting and Production Thinking

**Directory:** `unit10_troubleshooting_and_production_thinking`

Integrate the section using symptoms, knowns/unknowns, boundaries, low-risk evidence, hypotheses, discriminating tests, root cause, mitigation, recovery, user-perspective verification, documentation, prevention, blast radius, rollback, and ownership. Use an AnandTech scenario spanning process, memory, storage, identity, network, and application layers. Exclude advanced incident command, observability platforms, and production changes. The learner completes `first_investigation_notes.md` from an evidence pack.

## Scope Boundaries

Included: foundational mental models, safe observation, supplied evidence, platform-aware examples, controlled reasoning exercises, and production implications.

Excluded or deferred: VM creation, operating-system installation, Linux administration depth, programming, Git, remote access, web-server configuration, CI/CD, cloud accounts, containers, orchestration, and production infrastructure changes. Each belongs to a later locked section.

## Prerequisites and Dependencies

Only ordinary computer use is required. Units are sequential because each reuses the layers introduced before it. Optional observation exercises must include supplied evidence or a paper alternative so platform access never blocks conceptual completion.

## Terminology and Narrative Progression

Use AnandTech as a fictional organization and Anand as the learner-engineer. The story begins with Anand preparing for the role, progresses through understanding each system layer, and ends with his first structured investigation. Define every new term on first use and distinguish similarly named concepts explicitly.

## Environment and Lab Assumptions

- No VM requirement.
- No administrative/root requirement.
- No destructive exercise.
- Optional local observations may support Windows, macOS, or Linux, but every required objective must have a platform-independent alternative.
- Every command example must name its supported shell/OS, describe expected evidence rather than promise exact output, and state whether it changes system state.
- No network account or Internet access is required for completion.

## Artifacts and Assessments

Each unit adds a concise evidence note, diagram, decision record, or interpretation exercise to the learner journal. Unit 10 produces the cumulative `first_investigation_notes.md` containing symptom, scope, evidence, hypotheses, discriminating test, root cause or narrowed fault domain, recovery, verification, and prevention.

Assessments progress from recognition and explanation to interpretation, application, and diagnosis. Every unit includes knowledge checks, non-trivial MCQs with explanations, at least one evidence-interpretation task, a practical or paper exercise, and observable completion criteria. Unit 10 provides the section integration assessment.

## Security, Safety, and Production Expectations

Teach least privilege, secret hygiene, safe targets, observation before mutation, controlled changes, rollback, verification, and honest evidence. Clearly distinguish a simplified learner exercise from production controls such as approvals, audit trails, monitoring, redundancy, recovery testing, and ownership.

## Completion Criteria

The section is complete only when all ten units exist, every required artifact exists, all units pass SSOT, technical, learning, safety, and editorial review, links and headings validate, the cumulative investigation artifact is usable, and the owner explicitly accepts the section. Reading alone does not demonstrate completion.

Packaging requires a separate explicit owner request after all completion evidence passes.

## Revision History

| Version | Date | Change | Approval |
|---|---|---|---|
| 0.1 | 2026-09-03 | Drafted the complete ten-unit Section 00 contract from the accepted structure and planning workbook | Awaiting explicit owner lock |

