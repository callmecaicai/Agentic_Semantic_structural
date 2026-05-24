---
name: agentic-structural-harness
description: "Final agent-friendly semantic harness toolkit for sustained AI-assisted projects. Use when Codex must initialize or maintain a project split into .agentic control, semantic memory, and workspace execution layers; create stable artifact mirror docs; create event record folders; audit path/schema consistency; write conflicts; and reflux evidence into project understanding."
---

# Agentic Structural Harness

Use this when a project needs an agentic collaboration surface for humans and AI agents.
It is not a full automation framework. It provides paths, templates, and light checks so agents can re-enter a project, understand it quickly, and leave usable semantic records.

Root shape:

```text
project/
├── .agentic/   # control: config, templates, audits
├── semantic/   # memory: frame, field, records, trace, conflicts
└── workspace/  # execution: code, configs, scripts, tests, runs
```

Duality:

```text
stable object  <-> fixed mirror document
event instance <-> semantic record folder
```

Do not silently repair drift. Audit records structural breaks; user and agent judgment resolves semantic meaning.

---

## Start

Initialize a target project:

```bash
python agentic-structural-harness/scripts/harness.py init --root <project-root>
```

If already initialized, first read:

```text
semantic/pulse.md
semantic/frame/current_task.md
semantic/conflicts/
.agentic/project.yaml
```

Choose:

```text
clarify > reflux > locate
```

- `clarify`: object, goal, success, or failure boundary is unclear.
- `reflux`: evidence exists but has not updated understanding.
- `locate`: place a stable artifact or event into the harness.

---

## CLI

```bash
python agentic-structural-harness/scripts/harness.py pulse --root <project-root>
python agentic-structural-harness/scripts/harness.py new-artifact --root <project-root> workspace/src/foo.py
python agentic-structural-harness/scripts/harness.py accept-mirror --root <project-root> workspace/src/foo.py
python agentic-structural-harness/scripts/harness.py new-event --root <project-root> experiment --id exp001 --slug baseline
python agentic-structural-harness/scripts/harness.py audit --root <project-root>
python agentic-structural-harness/scripts/harness.py reflux-check --root <project-root>
```

The CLI creates common structure, checks obvious path/schema breaks, and records conflicts only for structural breaks. It does not train models, write business logic, decide semantic truth, or replace agent investigation.

---

## Layers

`.agentic/` declares the control schema:

```text
artifact_glob -> mirror_pattern
event_class   -> record_pattern + required files
```

`semantic/` carries Markdown memory:

```text
pulse / frame / field / records / trace / conflicts
```

`workspace/` carries executable artifacts and raw evidence:

```text
src / configs / scripts / tests / probes / runs / checkpoints
```

---

## Stable Artifact

Use for anything repeatedly referenced, modified, composed, or verified: code module, prompt block, dataset adapter, paper section, workflow node, plan unit.

```bash
python agentic-structural-harness/scripts/harness.py new-artifact --root <project-root> workspace/src/models/backbones/resnet.py
```

Creates:

```text
workspace/src/models/backbones/resnet.py
  <-> semantic/field/mirrors/workspace/src/models/backbones/resnet.md
```

The mirror records identity, I/O, risks, verification, and audit hash. It evolves with the artifact; it does not store event history.

New mirrors start with `audit_hash: pending`. After a human or agent has reviewed the mirror against the artifact:

```bash
python agentic-structural-harness/scripts/harness.py accept-mirror --root <project-root> workspace/src/models/backbones/resnet.py
```

---

## Event Instance

Use for something that happened once: training run, evaluation run, agent task, reading session, writing pass, planning review.

```bash
python agentic-structural-harness/scripts/harness.py new-event --root <project-root> experiment --id exp001 --slug dataset_a_frcnn
```

Creates:

```text
semantic/records/experiments/YYYY-MM-DD_exp001_dataset_a_frcnn/
├── index.md
├── input.md
├── process.md
├── output.md
├── analysis.md
└── reflux.md
```

Event records never overwrite history.

---

## Audit

```bash
python agentic-structural-harness/scripts/harness.py audit --root <project-root>
```

Checks structural consistency:

```text
uncovered-artifact       artifact without mirror
orphan-doc               mirror without artifact
no-front-matter          missing front matter
no-audit-hash            missing audit_hash
artifact-vs-doc          hash drift
incomplete-record        event folder missing files
record-name-out-of-schema record folder not matching schema
pending-mirror-review    mirror exists but has not been reviewed
pending-reflux           event evidence has not been interpreted
```

Only structural breaks write conflict files. Pending review/reflux is reported without creating conflict noise. Use `--no-conflicts` to report without writing conflict files.

---

## References

Read only when needed:

- [references/architecture.md](references/architecture.md): `.agentic/semantic/workspace` architecture.
- [references/principles.md](references/principles.md): full structural principles and semantic duality.
- [references/workflows.md](references/workflows.md): clarify / locate / reflux / audit workflows.
- [references/detection-example.md](references/detection-example.md): medium-complexity object detection example.

---

## Highest Rules

1. Keep control, semantic, and execution layers separate.
2. Stable objects get fixed mirror docs.
3. Event instances get new semantic record folders.
4. Paths carry meaning; schema declares meaning; audit checks reality.
5. Evidence freezes; understanding evolves; decisions explain transitions.
6. Keep the harness lighter than the project. Let humans and agents make judgment.
7. Conflicts are explicit. Do not silently repair semantic drift.
