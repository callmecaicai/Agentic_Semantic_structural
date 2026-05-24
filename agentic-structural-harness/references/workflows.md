# Workflows

This file describes how an agent should use the harness during real work. Use it when the short `SKILL.md` is not enough to decide the next move.

---

## Entry Workflow

Every session starts with orientation, not action.

Read:

```text
semantic/pulse.md
semantic/frame/current_task.md
semantic/conflicts/
.agentic/project.yaml
```

Then produce or update the five-line pulse:

```text
任务: <current real problem and success condition>
位置: <object/path being worked on>
最近: <latest relevant trace, or none>
冲突: <open relevant conflict, or none>
动作: <clarify | locate | reflux> 在 <frame | field | trace>
```

If you cannot fill a line, you are missing context. Read before editing.

---

## Clarify Workflow

Use clarify when the task cannot yet support action.

Update `semantic/frame/current_task.md` with:

```text
Object
Goal
Success Criteria
Worst Acceptable Outcome
Constraints
Out of Scope
Related paths
```

Do not create artifacts while the object or success condition is still unclear.

Exit condition:

```text
an agent can tell what to change, what not to change, and how success will be recognized
```

---

## Locate Stable Object

Use when a reusable object enters the project:

```text
code module
dataset adapter
prompt block
paper section
workflow node
training unit
planning block
```

Command:

```bash
python agentic-structural-harness/scripts/harness.py new-artifact --root <project-root> <artifact-path>
```

Example:

```bash
python agentic-structural-harness/scripts/harness.py new-artifact --root det workspace/src/models/backbones/resnet.py
```

Then edit the generated mirror:

```text
Rule
Input
Output
Invariant
Assumption
Risk
Verify
Related
```

Run:

```bash
python agentic-structural-harness/scripts/harness.py audit --root <project-root>
```

If audit detects drift, do not silently repair. Either update the mirror, update the artifact, or leave a conflict.

---

## Locate Event Instance

Use when something happened once:

```text
training run
evaluation run
agent task
reading session
writing pass
planning review
system execution
```

Command:

```bash
python agentic-structural-harness/scripts/harness.py new-event --root <project-root> <event-class> --id <id> --slug <slug>
```

Example:

```bash
python agentic-structural-harness/scripts/harness.py new-event --root det experiment --id exp001 --slug dataset_a_frcnn --trigger workspace/scripts/train.py
```

Fill the record:

```text
index.md    what happened and why
input.md    artifacts, configs, context, assumptions
process.md  trigger, command, steps, deviations
output.md   results, logs, artifacts
analysis.md interpretation, limits, risks
reflux.md   verdict and updates
```

The event record is not a log dump. Link logs, but explain meaning.

Exit condition:

```text
future agent can understand what happened, what evidence was produced, and whether it changed understanding
```

---

## Reflux Workflow

Use reflux when evidence should update understanding.

Read:

```text
semantic/records/<class>/<event>/analysis.md
semantic/records/<class>/<event>/output.md
semantic/records/<class>/<event>/reflux.md
```

Choose verdict:

```text
accepted   -> update frame/field and record source
pending    -> create/keep conflict or pending item
rejected   -> explain why evidence does not update understanding
superseded -> point to later evidence
```

If accepted, update the relevant current-understanding file:

```text
semantic/field/baseline_board.md
semantic/field/contracts/*.md
semantic/frame/current_task.md
semantic/trace/reflux_journal.md
```

Do not let raw evidence directly rewrite the frame. Reflux is the bridge.

---

## Audit Workflow

Run audit after structural changes:

```bash
python agentic-structural-harness/scripts/harness.py audit --root <project-root>
```

Audit checks:

```text
uncovered-artifact
orphan-doc
no-front-matter
no-audit-hash
artifact-vs-doc
incomplete-record
evidence-not-refluxed
```

Use:

```bash
python agentic-structural-harness/scripts/harness.py audit --root <project-root> --no-conflicts
```

for a dry report.

Audit does not prove semantic correctness. It proves that the declared structural relationships are present and inspectable.

---

## Conflict Workflow

A conflict means:

```text
two things that should agree do not agree
```

Examples:

```text
artifact exists but mirror is missing
mirror points to missing artifact
artifact hash changed but mirror was not reviewed
event folder lacks required files
analysis says accepted but field was not updated
frame goal contradicts evidence
```

Conflict file should state:

```text
What conflicts
Why it matters
Resolve by
Resolution
```

The agent may propose resolution, but should not silently choose which side is true unless the user explicitly granted that authority.

---

## Decision Workflow

Use a decision record when a structural choice changes future work.

Examples:

```text
change adapter schema
change evaluation protocol
choose baseline model family
change event record format
promote repeated pattern into stable object
deprecate an old path
```

Decision should record:

```text
context
decision
alternatives
consequences
what would refute it
related frame/field/trace
```

Decisions freeze. If wrong later, write a new decision and mark the old one superseded.

---

## Adapter Workflow

Create or modify an adapter when a domain repeats a stable pattern.

Adapter work usually means editing `.agentic/project.yaml`:

```yaml
stable_objects:
  - name: detector
    artifact_glob: workspace/src/models/detectors/*.py
    mirror_pattern: semantic/field/mirrors/models/detectors/{stem}.md

events:
  - name: experiment
    record_pattern: semantic/records/experiments/{date}_{event_id}_{slug}
```

After changing schema:

```text
1. create a decision record
2. update templates if needed
3. run audit
4. resolve new conflicts
```

Do not hard-code one project's temporary structure into a general adapter.

---

## Baseline Search Workflow

For research engineering, baseline search is a canonical use case.

Each run creates:

```text
semantic/records/experiments/YYYY-MM-DD_exp001_dataset_a_frcnn/
```

Only accepted reflux updates:

```text
semantic/field/baseline_board.md
```

The board is current understanding. Event records are historical evidence.

This prevents a single noisy run from becoming truth too early.

---

## Minimal Agent Rule

When unsure:

```text
do not invent structure in prose
create or inspect schema
create the semantic object
audit it
record unresolved breaks
reflux only after evidence has been interpreted
```
