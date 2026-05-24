---
adr_id: 001
title: extract_kernel_and_domain_adapters
date: 2026-05-24
status: accepted
superseded_by:
---

# ADR 001: extract_kernel_and_domain_adapters

## Context

上一版 skill 把"第一性的抽象元规则"和"深度学习实验工程"混在同一层。这样会让后续生活训练、论文阅读、论文写作、计划管理等项目被 DL 路径、W&B、pipeline、src/contracts 等具体形态提前污染。

用户要求回到抽象,只保留基于 Markdown 的语义管理机制和基于工件推进机制的元结构。

## Decision

将结构拆成两层:

- [../../../kernel/](../../../kernel/):九条领域无关的元规则。
- [../../../domains/](../../../domains/):每个具体项目类型的 adapter。

当前只保留一个具体 adapter:[../../../domains/deep_learning/](../../../domains/deep_learning/)。

## Alternatives considered

- 继续在 `docs/field/` 内混合抽象规则与 DL 规则:不选,会继续扩大具体领域对 kernel 的污染。
- 只改写 `SKILL.md`,不移动文件:不选,路径结构本身仍会误导 agent。
- 为生活训练/论文/计划管理立即创建 adapter:不选,这些 adapter 尚未通过重复使用显现稳定 schema。

## Consequences

- 立即影响:入口 [../../../SKILL.md](../../../SKILL.md) 只负责路由和读取 kernel;DL 细则集中在 `domains/deep_learning/`。
- 长期影响:新增领域时只需创建 adapter,不需要改 kernel。
- 风险:kernel 仍可能因为示例太多而再次具体化;后续应把稳定示例继续下放到 adapter。

## What would refute this decision

如果多个非 DL 项目使用后发现 kernel 缺少共同必要规则,而这些规则不能通过 adapter 表达,则需要修订 kernel。

## Related

- frame: [../../frame/current_task.md](../../frame/current_task.md)
- 涉及工件: [../../../SKILL.md](../../../SKILL.md)
- 涉及文档: [../../../kernel/](../../../kernel/), [../../../domains/](../../../domains/)
- 涉及 reflux: [../reflux_journal.md](../reflux_journal.md)
