# Architecture

Final root split:

```text
project/
├── .agentic/   # control
├── semantic/   # memory
└── workspace/  # execution
```

## .agentic

Agent-facing control layer. It owns `project.yaml`, templates, and optional audits/adapters. It creates and checks structure; it does not train models, decide semantic truth, or replace human-agent review.

## semantic

Markdown memory:

```text
semantic/
├── pulse.md
├── frame/      # current intent
├── field/      # current structure, contracts, mirrors
├── records/    # event folders
├── trace/      # reflux, decisions, failures
└── conflicts/  # unresolved breaks
```

## workspace

Execution layer. For code projects this usually contains `src/`, `configs/`, `scripts/`, `tests/`, `probes/`, `runs/`, `checkpoints/`. For writing or planning projects it may contain drafts, sources, prompts, plans, or generated artifacts.

## Duality

Stable object:

```text
workspace/src/foo.py <-> semantic/field/mirrors/workspace/src/foo.md
```

Event:

```text
one run/session/task <-> semantic/records/<class>/YYYY-MM-DD_<id>_<slug>/
```

Stable objects evolve. Events accumulate. Do not store event history in mirrors. Do not overwrite event records.

## Agent loop

```text
read pulse -> check frame/conflicts -> choose clarify/reflux/locate
locate stable object -> new-artifact
locate event -> new-event
audit -> report pending states; write conflict only if structurally broken
accepted evidence -> reflux into frame/field
```
