---
name: structural-project-kernel
description: Abstract first-principles project methodology for AI-assisted work that needs persistent Markdown semantic management and artifact/code/project progression. Use when Codex must clarify intent, locate artifacts in a semantic structure, create mirror docs for stable artifacts, create semantic record folders for event instances, reflux evidence into understanding, maintain artifact-document coupling, record conflicts and decisions, or adapt the same meta-rules to life planning, paper reading, paper writing, research, coding, training plans, or any long-running project.
---

# Structural Project Kernel

This skill is a domain-neutral routing kernel for sustained AI collaboration.

Its first principle: every ongoing project is a relation between current intent, structural understanding, historical evidence, and unresolved conflict. Do not let any one of these impersonate another.

Its harness principle: stable executable objects need stable mirror documents; one-time executable events need incremental semantic record folders.

---

## First Read

When entering a project using this skill:

1. Read [pulse.md](pulse.md).
2. Read [docs/frame/current_task.md](docs/frame/current_task.md) and [docs/frame/success_criteria.md](docs/frame/success_criteria.md).
3. Check [docs/conflicts/](docs/conflicts/) for open conflicts.
4. Read only the kernel rule or domain adapter needed for the next action.
5. Output and update the five-line pulse before acting.

Pulse format is defined in [kernel/pulse_protocol.md](kernel/pulse_protocol.md):

```text
任务: <当前任务的真问题、成功标准>
位置: <在哪个对象、哪条路径上工作>
最近: <最近一条相关 trace,无则 none>
冲突: <未解决的相关 conflict,无则 none>
动作: <clarify | locate | reflux> 在 <frame | field | trace>
```

---

## Kernel Rules

The kernel is the source of truth. Domain adapters instantiate it; they do not replace it.

| Rule | File | Role |
|---|---|---|
| A | [kernel/three_actions.md](kernel/three_actions.md) | clarify / locate / reflux x frame / field / trace |
| B | [kernel/three_contexts.md](kernel/three_contexts.md) | separate constitutional, process, and evidence contexts |
| C | [kernel/path_authority.md](kernel/path_authority.md) | make every path declare identity, authority, lifecycle, writer, reader |
| D | [kernel/coupling_principle.md](kernel/coupling_principle.md) | bind artifacts to mirror documents, anchors, audit, and verification |
| E | [kernel/conflict_mechanism.md](kernel/conflict_mechanism.md) | record inconsistency explicitly; do not silently repair it |
| F | [kernel/reflux_mechanism.md](kernel/reflux_mechanism.md) | upgrade evidence into understanding through reflux |
| G | [kernel/frozen_vs_evolving.md](kernel/frozen_vs_evolving.md) | freeze evidence, evolve understanding, record transitions |
| H | [kernel/pulse_protocol.md](kernel/pulse_protocol.md) | start every handoff with a five-line pulse |
| I | [kernel/templates_as_schema.md](kernel/templates_as_schema.md) | treat templates as schemas, not decoration |
| J | [kernel/semantic_duality.md](kernel/semantic_duality.md) | bind stable artifacts to mirror docs and event instances to record folders |

Templates live in [kernel/templates/](kernel/templates/).

---

## Action Routing

Choose the next action by priority:

1. **clarify** if the task object, goal, success criteria, or unacceptable failure are unclear.
2. **reflux** if evidence exists but has not been integrated into frame or field.
3. **locate** if the intent is clear and the structure is ready to receive a new or changed object.

Do not construct on top of unclear intent. Do not add structure on top of unintegrated evidence.

---

## Three Layers

| Layer | Carries | Typical files |
|---|---|---|
| **frame** | current intent, goal, success criteria, constraints | [docs/frame/](docs/frame/) |
| **field** | current structural understanding, path authority, contracts | kernel rules + project/domain field docs |
| **trace** | evidence, decisions, failures, reflux history | [docs/trace/](docs/trace/) |
| **conflicts** | explicit unresolved inconsistency | [docs/conflicts/](docs/conflicts/) |

`conflicts` is not a fourth layer. It is the place where any failed relation between layers is held until adjudicated.

---

## Semantic Duality

Any artifact that will be repeatedly changed must have a mirror document. Any event that actually happened must have a semantic record folder.

The kernel defines two paired structures:

```text
stable artifact <-> mirror document
event instance  <-> semantic record folder
```

The first pair is specified by [kernel/coupling_principle.md](kernel/coupling_principle.md). The full dual structure is specified by [kernel/semantic_duality.md](kernel/semantic_duality.md).

The concrete mapping is owned by a domain adapter. For available adapters, see [domains/README.md](domains/README.md). The current concrete adapter is [domains/deep_learning/](domains/deep_learning/).

---

## Domain Adapters

Load a domain adapter only when the current project type requires it.

Examples:

- life training planning -> create or use a training-plan adapter
- paper reading -> create or use a paper-reading adapter
- paper writing -> create or use a writing adapter
- project management -> create or use a planning adapter
- deep learning engineering -> use [domains/deep_learning/](domains/deep_learning/)

If no adapter exists, operate at the kernel level and create only the minimal adapter pieces that have become stable through repeated use.

---

## Exit Conditions

- **clarify complete**: object, goal, success criteria, worst acceptable outcome, and scope are explicit.
- **locate complete**: stable objects have mirror documents; event instances have semantic record folders; anchors, verification bridge, and path authority entry exist if needed.
- **reflux complete**: the evidence has an entry in [docs/trace/reflux_journal.md](docs/trace/reflux_journal.md); accepted entries update frame/field, pending entries become conflicts.

---

## Highest Rules

1. Keep the kernel first-principled and domain-neutral.
2. Put domain details in `domains/<adapter>/`, never in the kernel unless they are examples.
3. Never silently repair a disagreement between intent, artifact, document, and evidence.
4. Evidence freezes; understanding evolves; decisions explain the transition.
5. If a path cannot declare what it is, what authority it has, and who may write it, it should not exist yet.
6. Stable objects do not accumulate history inside themselves; event records do not overwrite history.
