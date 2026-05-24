---
exp_id: expNNN
short_name: <one_phrase>
status: planned | running | done | frozen
started: YYYY-MM-DD
ended: YYYY-MM-DD
config: configs/experiments/expNNN_*.yaml
wandb_group: <group name>
wandb_runs:
  - <run_id_1>
  - <run_id_2>
related_frame: docs/frame/current_task.md (at exp start)
---

# expNNN: <short_name>

## Question
<这次实验回答什么问题。一句话。>

## Hypothesis
<事前预期的结果。>

## Setup
- baseline: <ref to which config or run>
- variable: <这次变了什么>
- controlled: <这次固定了什么>
- data: <dataset + split + version>

## Runs
- <run_id_1>: <一句话描述,例如 "baseline">
- <run_id_2>: <例如 "with new decoder">

## Result
<观察到的事实。指标、曲线、可视化要点。>

## Interpretation
<事实说明了什么。>

## Verdict
- 验证了假设 | 反驳了假设 | 不确定
- 影响:<是否需要回流到 frame 或 field;若需要则在 docs/trace/reflux_journal.md 留条目>

## Follow-up
- <下一步实验或决策>
