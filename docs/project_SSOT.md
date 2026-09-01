# Journey with AnandTech — Project SSOT

**Canonical project:** Journey with AnandTech — DevOps Zero to Production

**Document type:** Project-level source of truth

**Status:** Active

**Course-structure version:** 1.0

**Course-structure lock:** Locked by explicit user approval on 2026-09-02

---

## 1. Current Project State

| Field | Authoritative value |
|---|---|
| Active section | Section 00 — Computer and IT Prerequisites |
| Active unit | None; unit generation is not yet authorized |
| Current phase | Section SSOT discussion |
| Active-section lock | Draft; not locked |
| Approved Section 00 environment | Environment-independent explanation with safe, optional local inspection; no VM requirement |
| Required deliverable | Review and lock `sections/00_computer_it_prerequisites/SSOT.md` |
| Last accepted checkpoint | Course-wide section sequence and parallel workshop model locked |
| Packaging permission | Not granted |

The active task is section design. Learner-facing Unit 01 generation must not begin until the Section 00 SSOT is explicitly locked.

---

## 2. Locked Course Structure

The following section sequence is locked at the course-map level:

1. **Section 00 — Computer and IT Prerequisites**
2. **Section 01 — Evolution of Software Delivery**
3. **Section 02 — Software Development Life Cycle**
4. **Section 03 — VirtualBox and AnandTech Lab Platform**
5. **Section 04 — Linux Foundations**
6. **Section 05 — Development Insight for DevOps Engineers**
7. **Section 06 — Linux Networking**
8. **Section 07 — Shell Scripting and Automation**
9. **Section 08 — Git and Source Control**
10. **Section 09 — Remote Git Collaboration**
11. **Section 10 — SSH, SCP, SFTP, and Rsync**
12. **Section 11 — Web Servers, HTTP, TLS, and Nginx**
13. **Section 12 — CI/CD Foundations and Jenkins**
14. **Section 13 — Testing, Artifacts, and Automated Deployment**
15. **Section 14 — Monitoring, Logging, and Alerting**
16. **Section 15 — Containers, Docker, and Compose**
17. **Section 16 — Ansible and Configuration Automation**
18. **Section 17 — Infrastructure as Code and Cloud Foundations**
19. **Section 18 — AWS Foundations**
20. **Section 19 — Kubernetes and Orchestration**
21. **Section 20 — Observability, Reliability, and DevSecOps**
22. **Section 21 — Interview Preparation and Production Scenarios**
23. **Section 22 — Production CI/CD and AnandTech Capstone**

Course-map lock fixes the section identities, sequence, and broad purpose. It does not silently lock every unit topic, lab command, tool version, artifact detail, or package name. Those decisions belong to the relevant section SSOT.

---

## 3. Locked Course-Wide Design

- The main course is a technically rigorous, comic-like AnandTech journey.
- Anand begins as a new engineer and progressively becomes responsible for the production platform.
- Concepts and mental models come before commands.
- A parallel workshop track provides practical industrial milestone labs.
- Workshops support full, guided, and skip-safe continuity modes.
- Skipping a workshop does not claim practical mastery and does not block conceptual progress.
- Failure labs use symptom → evidence → hypothesis → test → root cause → recovery → verification → prevention.
- Questions, common misunderstandings, evidence interpretation, and production connections recur throughout the course.
- `course_calendar.md` maintains both the learner's real study dates and the stable AnandTech story chronology.
- Linux is the deepest foundational technical section.
- The AnandTech Todo application grows from one HTML page into the production capstone.
- Tools are installed and configured progressively in their owning sections.

---

## 4. Deferred Decisions

These decisions are intentionally deferred and do not block Section 00:

| Decision | Owning section | Current proposal | Lock state |
|---|---|---|---|
| Host-only IP allocation | Section 03 | Host `192.168.56.1`; `web01` `.11`; `cicd01` `.12`; `mon01` `.13` | Deferred |
| Bridged versus NAT fallback | Section 03 | Bridged primary with documented NAT fallback | Deferred |
| Terraform as the IaC implementation tool | Section 17 | Terraform | Deferred |

The owning section PLAN must discuss each decision before its SSOT is locked.

---

## 5. Laboratory Direction

The persistent workshop platform is planned for Section 03 and later:

- `web01`: Alpine Linux; Nginx and the web/application role.
- `cicd01`: Debian; Git and Jenkins role.
- `mon01`: Debian; Prometheus and Grafana role.
- Adapter 1: proposed bridged Internet/LAN access.
- Adapter 2: host-only management network.
- All VMs: persistent networking and SSH access from the host.

This direction is accepted at course-map level. Exact addressing, network stack, installation commands, versions, and recovery procedures remain Section 03 SSOT decisions.

---

## 6. Governance

1. `docs/PLAN.md` or the current planning workbook records mutable discussions and alternatives.
2. This project SSOT records locked course-wide state.
3. Each section has its own mutable `PLAN.md` and authoritative `SSOT.md`.
4. A section SSOT becomes authoritative only after explicit user lock.
5. Locked curriculum decisions are never changed silently.
6. Only the requested unit or batch may be generated.
7. A section ZIP requires a locked SSOT, complete validated content, and explicit packaging permission.
8. The next major section does not begin before acceptance of the active section unless the user explicitly allows parallel planning.

---

## 7. Current Authorization Boundary

Authorized now:

- Maintain the Section 00 PLAN.
- Draft, review, and revise the Section 00 SSOT.
- Identify missing or conflicting Section 00 decisions.

Not authorized now:

- Generate learner-facing Section 00 units.
- Build Section 00 workshop deliverables.
- Package any section.
- Begin Section 01 design.

---

## 8. Revision History

| Version | Date | Change | Approval |
|---|---|---|---|
| 1.0 | 2026-09-02 | Locked course-wide section sequence and workshop direction; activated Section 00 SSOT discussion | Explicit user selection: “Lock, start Section 00” |

