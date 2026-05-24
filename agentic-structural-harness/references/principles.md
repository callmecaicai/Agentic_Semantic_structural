# Principles

This harness is a structural method for long-running agentic projects. It assumes the useful unit of collaboration is not a single prompt, a single code edit, or a single document. The useful unit is a project that can be re-entered many times by different agents without losing its intent, structure, evidence, or unresolved conflicts.

The harness is built around one first principle:

```text
executable structure and semantic structure must be separate, paired, and auditable
```

Code, scripts, prompts, plans, drafts, and configs do the work. Markdown explains what the work means, what changed, what is trusted, and what remains unresolved. The two systems must not collapse into each other.

---

## The Three Layers

Every project has three semantic layers and one conflict area:

```text
frame     = current intent
field     = current structure
trace     = historical evidence and interpretation
conflicts = unresolved inconsistency
```

`frame` answers: What are we doing now? What counts as success? What is out of scope? What failure is unacceptable?

`field` answers: What objects exist? What are their roles? Which paths carry authority? What contracts hold between components?

`trace` answers: What happened? What evidence exists? What did we decide? What failures should not be forgotten?

`conflicts` answers: What should agree but currently does not?

The layers must stay separate. Evidence is not a rule. A draft is not a fact. Intent is not implementation. A conflict is not a failure of cleanliness; it is a captured site of judgment.

---

## The Three Actions

Agents should not simply "continue working." They should choose one action:

```text
clarify -> locate -> reflux
```

Priority is:

```text
clarify > reflux > locate
```

`clarify` is used when the frame is not stable enough to act. It defines the object, goal, success criteria, unacceptable failure, constraints, and scope.

`locate` is used when something must enter the structure. It gives a stable object or event a path, schema, document, and audit relationship.

`reflux` is used when evidence has accumulated and must update understanding. It decides whether evidence is accepted, pending, rejected, or superseded.

This order matters. If the task is unclear, new structure is noise. If evidence is unintegrated, more construction compounds drift. Locate only after intent and evidence have been sufficiently handled.

---

## Semantic Duality

The core of the harness is a two-part duality:

```text
stable object  <-> fixed mirror document
event instance <-> semantic record folder
```

Stable objects are things that persist and get reused:

```text
code module
prompt block
dataset adapter
paper section
workflow node
planning unit
training block
configuration family
```

Each stable object gets one mirror document. The mirror evolves with the object. It records identity, inputs, outputs, assumptions, invariants, risks, verification, and related decisions.

Event instances are things that happened once:

```text
training run
evaluation run
agent task
reading session
writing pass
planning review
system execution
```

Each event gets a new semantic record folder. The folder is append-like and historical. It records input, process, output, analysis, and reflux. It must not be overwritten by a later event.

Stable objects do not store event history. Event records do not become current structure by themselves.

---

## Why Good Code Wants Good Semantics

Well-engineered code is already semantic. It separates components, interfaces, configs, registries, builders, tests, probes, runs, and artifacts. A poor codebase hides semantics in long files and incidental coupling. A good codebase exposes structure.

This harness takes advantage of that. It does not fight code structure; it mirrors it.

When a project is sufficiently modular, the Markdown system can attach to it cleanly:

```text
workspace/src/models/backbones/resnet.py
  <-> semantic/field/mirrors/workspace/src/models/backbones/resnet.md
```

When a project records executions cleanly, the Markdown system can interpret them cleanly:

```text
workspace/runs/exp001/
  <-> semantic/records/experiments/YYYY-MM-DD_exp001_baseline/
```

The goal is not documentation for its own sake. The goal is agentic continuity: a future agent can enter, read little, act correctly, and leave behind usable structure.

---

## Path Authority

Paths are semantic carriers, not storage bins. Every important path class must answer:

```text
identity:    what family of object is this?
authority:   does it express intent, structure, evidence, reference, or tool state?
lifecycle:   does it evolve, append, freeze, or stay temporary?
writer:      who or what may modify it?
reader:      who reads it first and why?
```

Event paths must also answer:

```text
trigger:     what caused this event?
record:      where are input, process, output, analysis, reflux?
```

Avoid names such as `misc`, `notes`, `temp`, `new`, `old`, and `final`. These names hide authority and lifecycle. If a path cannot explain what kind of truth it carries, it is not ready to exist.

---

## Schema, Audit, Conflict

Path meaning must be externalized. It cannot live only in an agent's memory.

The closed loop is:

```text
path expresses meaning
schema declares meaning
harness creates objects from schema
audit checks reality against schema
conflict records breaks
reflux upgrades evidence into understanding
```

`schema` is the declared rule. In this toolkit it lives in `.agentic/project.yaml`.

`audit` is the reality check. It compares workspace artifacts, semantic mirrors, event records, front matter, hashes, and required files.

`conflict` is the case file. It records mismatch without deciding which side is right.

The harness should create and detect. It should not silently repair. Silent repair destroys judgment.

---

## Context Types

Project information has at least three authority types:

```text
constitutional = current rules and structure
process        = active work and interpretation
evidence       = historical fact or raw result
```

Examples:

```text
semantic/frame/current_task.md        constitutional/process
semantic/field/contracts/*.md         constitutional
semantic/records/*/output.md          evidence
semantic/records/*/analysis.md        process interpretation
workspace/runs/                       raw evidence
semantic/trace/decisions/             frozen decisions
semantic/conflicts/                   open judgment
```

Do not cite an experiment output as a universal rule. Do not cite a planning note as evidence. Do not treat a desired goal as implemented structure.

---

## Frozen vs Evolving

Evidence freezes. Understanding evolves.

Frozen objects:

```text
raw logs
run outputs
completed event records
accepted decisions
past frame snapshots
external reference snapshots
```

Evolving objects:

```text
current task
path table
contracts
baseline board
stable object mirrors
reflux journal entries until verdict
```

Transitions require trace. If understanding changes because of evidence, record the reflux. If a structural choice changes, record a decision. If something disagrees, record a conflict.

---

## Templates as Schema

Templates are not decoration. They are schema made readable.

Mirror documents must expose machine-readable front matter:

```yaml
covers:
  - <artifact path>
verified_by:
  - <test/probe/check path>
last_audited: YYYY-MM-DD
audit_hash: <hash>
```

Event records must preserve the semantic slots:

```text
index    = what happened and why
input    = artifacts, config, context, assumptions
process  = trigger, steps, deviations
output   = results, logs, generated artifacts
analysis = interpretation and limits
reflux   = verdict and understanding change
```

Conflict records must preserve:

```text
what conflicts
why it matters
resolve by
resolution
```

If a template field repeatedly matters, promote it into schema. If a template grows too specific, move the specificity into an adapter.

---

## Adapter Principle

The kernel should stay domain-neutral. Adapters instantiate it.

A domain adapter declares:

```text
artifact globs
mirror path patterns
event classes
record folder patterns
required files
front-matter fields
audit rules
templates
```

Deep learning, paper reading, paper writing, training planning, and project management should not all share the same concrete paths. They should share the same harness logic.

Do not create an adapter too early. Create one when a pattern repeats and the fields become stable.

---

## Practical Judgment

The harness should stay lighter than the project it serves. Do not turn every observation into a new schema and do not turn every schema into code. Use three levels of commitment:

```text
free text    = the pattern is still forming
template     = the pattern repeats and needs stable fields
script/audit = the pattern is fragile, frequent, or easy to forget
```

A good agent should prefer the weakest level that preserves continuity. If a one-off event needs explanation, write an event record. If the same event shape repeats, stabilize the template. If agents repeatedly forget to create or check it, add harness support.

The same applies to stable objects. A new component may begin with a short mirror. If its interface becomes central, expand the mirror and verifier. If many such components appear, encode their path rule in `.agentic/project.yaml`.

This prevents two failures:

```text
under-structure: meaning lives only in the current agent's context
over-structure: the project becomes ceremony and stops moving
```

The correct structure is the minimum structure that makes the next handoff reliable.

---

## Control, Semantic, Workspace

The final practical split is:

```text
.agentic/   control layer
semantic/   semantic layer
workspace/  execution layer
```

`.agentic/` is for the harness and agents. It is like `.git` or `.github`: a control surface.

`semantic/` is for Markdown memory. It is not "docs" in the ordinary sense. It is the project's state of understanding.

`workspace/` is for execution. It may contain code, drafts, prompts, plans, configs, scripts, runs, generated files, or tests.

This split keeps control logic from polluting meaning, meaning from polluting code, and code from pretending to explain itself fully.

---

## Highest Rules

1. Keep control, semantic, and execution layers separate.
2. Keep frame, field, trace, and conflicts separate.
3. Stable objects get fixed mirror docs.
4. Event instances get new semantic record folders.
5. Paths carry meaning; schema declares meaning; audit checks reality.
6. Evidence freezes; understanding evolves; decisions explain transitions.
7. Conflicts are explicit. Do not silently repair semantic drift.
