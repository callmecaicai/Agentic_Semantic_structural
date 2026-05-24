---
covers:
  - src/<path>/<file>.py
implements_contract: domains/deep_learning/pipeline_contracts.md#<section-anchor>
verified_by:
  - tests/<test_file>.py
last_audited: YYYY-MM-DD
audit_hash: 0000000
---

# <ModuleName> Contract

## Rule
<这个模块做什么,一段话>

## Input
- <字段>: <shape / dtype / range>
- ...

## Output
- <字段>: <shape / dtype / range>
- ...

## Invariant
- <必须始终成立的不变量>
- ...

## Assumption
- <对上游的假设>
- ...

## Risk
- <最危险的失败模式>
- ...

## Verify with
- tests/<...>
- probes/<...>

## Related
- run: <W&B run id 或 runs/<id>>(若有相关实验)
- decision: docs/trace/decisions/<...>(若有相关决策)
- experiment: docs/experiments/<...>(若有相关实验文档)
