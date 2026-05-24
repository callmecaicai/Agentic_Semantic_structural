---
name: structural-kernel-lite
description: "Compact first-principles semantic harness for sustained AI-assisted projects. Use when Codex must keep Markdown semantic management and executable artifacts aligned: clarify intent, locate stable artifacts with mirror docs, create event record folders, reflux evidence, audit path/schema consistency, and record conflicts without silently repairing drift."
---

# Structural Kernel Lite

This is a compact project kernel for agentic work that must persist across sessions. It treats a project as four relations:

```text
frame     = current intent
field     = current structure
trace     = historical evidence and interpretation
conflicts = unresolved breaks between the above
```

Never let one impersonate another. Evidence is not a rule. A draft is not a fact. An intention is not an implemented structure.

---

## Start Protocol

On entry, read or write a five-line pulse:

```text
任务: <real current problem and success condition>
位置: <object/path being worked on>
最近: <latest relevant trace, or none>
冲突: <open relevant conflict, or none>
动作: <clarify | locate | reflux> 在 <frame | field | trace>
```

If any line cannot be filled, read frame/trace/conflicts before acting.

---

## Three Actions

Choose one action. Priority is `clarify > reflux > locate`.

### clarify

Use when the task object, goal, success criteria, scope, or unacceptable failure is unclear.

Exit only when these are explicit:

```text
object / goal / success / worst acceptable outcome / out of scope
```

### locate

Use when placing a new or changed object into the project structure.

Locate means: give it a semantic path, declare its authority, connect it to docs, and define how drift is checked.

### reflux

Use when evidence exists but has not been integrated.

Reflux means: record what happened, explain what it changes, and update frame/field only when accepted. Pending reflux is a conflict.

---

## Semantic Duality

The harness has two paired structures.

```text
stable object  <-> fixed mirror document
event instance <-> semantic record folder
```

### Stable object

A stable object is anything repeatedly referenced, changed, composed, or verified: code module, prompt block, paper section, workflow node, training unit, plan block, dataset adapter.

Rule:

```text
artifact path -> mirror doc path
```

The mirror doc records identity, input/output, assumptions, risks, verification, and audit hash. It evolves with the object. It does not accumulate run history.

### Event instance

An event is something that happened once: training run, agent task, reading session, writing pass, planning review, system execution.

Rule:

```text
event -> new semantic record folder
```

Each event creates a new folder. It never overwrites history.

Minimal folder:

```text
YYYY-MM-DD_<event_id>_<slug>/
  index.md
  input.md
  process.md
  output.md
  analysis.md
  reflux.md
```

Adapters may rename or extend files, but must preserve: overview, input, process, output, analysis, reflux.

---

## Path Authority

Paths are semantic objects, not storage bins. Any new path class must answer:

```text
identity:       what object family is this?
authority:      current intent, current structure, evidence, reference, or tool?
lifecycle:      evolves, appends, freezes, or is temporary?
write power:    user, agent, system, or external source?
main reader:    who reads it first and why?
```

For event folders also answer:

```text
trigger: what caused this event?
record: where are input/process/output/analysis/reflux?
```

Avoid vague names: `notes/`, `misc/`, `temp/`, `final/`, `new/`, `old/`.

---

## Schema, Audit, Conflict

Paths express meaning but cannot enforce meaning by themselves.

Use this loop:

```text
path expresses semantics
schema declares semantics
new-artifact/new-event creates objects from schema
audit checks reality against schema
conflict records breaks
reflux upgrades evidence into understanding
```

Audit should check at least:

```text
artifact without mirror doc       -> uncovered-artifact
mirror doc without artifact       -> orphan-doc
missing front-matter              -> no-front-matter
missing verifier                  -> missing-verifier
hash drift                        -> artifact-vs-doc
event happened but no folder      -> unrecorded-event
folder missing required files     -> incomplete-record
record links broken artifact/log  -> record-broken-reference
pending reflux too long           -> evidence-not-refluxed
```

Audit must not silently fix semantic drift. It writes conflicts. User or explicit decision resolves them.

---

## Minimal Templates

### Mirror doc

```yaml
---
covers:
  - <artifact path>
verified_by:
  - <test/probe/check path>
last_audited: YYYY-MM-DD
audit_hash: <hash>
---
```

Body:

```text
Rule / Input / Output / Invariant / Assumption / Risk / Verify / Related
```

### Event record

`index.md` states what happened and why.  
`input.md` lists artifacts, configs, context, assumptions.  
`process.md` records trigger, command/action, deviations.  
`output.md` links results, logs, deliverables.  
`analysis.md` says what this suggests and what it does not prove.  
`reflux.md` gives verdict: accepted, pending, rejected, superseded.

### Conflict

```yaml
---
type: <conflict type>
discovered: YYYY-MM-DD
discovered_by: <user | agent | audit>
target_artifact: <path or empty>
target_doc: <path or empty>
status: open | resolved
---
```

Body:

```text
What conflicts / Why it matters / Resolve by / Resolution
```

---

## Operating Loop

Use this loop for every task:

```text
1. pulse
2. choose clarify/reflux/locate
3. if clarify: update frame
4. if locate stable object: create/update mirror doc
5. if locate event: create semantic record folder
6. audit path/schema consistency
7. write conflicts for breaks
8. reflux accepted evidence into frame/field
9. record decisions when structure changes
```

Do not add abstractions early. Create a domain adapter only after a pattern repeats.

An adapter may define:

```text
artifact globs
mirror path patterns
event folder patterns
required files
front-matter fields
audit rules
templates
```

---

## Highest Rules

1. Keep frame, field, trace, and conflicts separate.
2. Stable objects get fixed mirror docs.
3. Event instances get new semantic record folders.
4. Stable objects do not store event history.
5. Event records do not overwrite history.
6. Paths carry meaning; schema declares it; audit checks it.
7. Evidence freezes; understanding evolves; decisions explain transitions.
8. Never silently repair disagreements between artifact, document, intent, and evidence.
